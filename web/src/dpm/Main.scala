package dpm

import com.raquo.laminar.api.L.{*, given}
import org.scalajs.dom
import scala.concurrent.ExecutionContext.Implicits.global
import scala.scalajs.js
import scala.scalajs.js.Thenable.Implicits.*
import scala.util.{Failure, Success}

/** The query page: pick a question, fill its slots, see the answer and the SQL.
  *
  * The engine is loaded on the first question rather than on page load. It is 8.1 MB
  * gzipped - heavier than all the data put together, which is 3.05 MB for everything DPM
  * 4.4 ships - so paying for it before anyone has asked anything is the one thing that
  * would make the page feel slow.
  */
object Main:

  /** A question and its slots live in the URL, so an answer can be sent to someone.
    * Read once at startup; written on every ask with replaceState, which leaves the
    * back button meaning what it meant before the page was opened.
    */
  private def fromLocation(): (Question, Map[String, String]) =
    val params = new dom.URLSearchParams(dom.window.location.search)
    val question = Questions.byId(Option(params.get("q")).getOrElse(""))
    val filled = question.slots.flatMap(slot => Option(params.get(slot.name)).map(slot.name -> _)).toMap
    (question, filled)

  private def toLocation(question: Question, filled: Map[String, String]): Unit =
    val params = new dom.URLSearchParams()
    params.set("q", question.id)
    if Data.release.nonEmpty then params.set("release", Data.release)
    question.slots.foreach(slot => params.set(slot.name, filled.getOrElse(slot.name, slot.example)))
    dom.window.history.replaceState((), "", s"?${params.toString}")

  private val engine = Var[Option[Connection]](None)
  private val assistant = Var[Option[Engine]](None)
  private val assistantModel = Var(Assistant.models.head._1)
  private val assistantStatus = Var("")
  private val inOwnWords = Var("")
  private val releases = Var(List.empty[String])
  private val choices = Var(Map.empty[String, List[String]])
  private val about = Var(Option.empty[Data.About])
  private val status = Var("")
  private val running = Var(false)
  private val answer = Var(Option.empty[Answer])
  private val question = Var(fromLocation()._1)
  private val slots = Var(fromLocation()._2)

  final case class Answer(columns: List[String], rows: List[List[String]], millis: Long, sql: String, source: String)

  def main(args: Array[String]): Unit =
    // The release comes from the URL when there is one, so a shared link answers under
    // the release it was asked under rather than under whatever is newest today.
    val asked = Option(new dom.URLSearchParams(dom.window.location.search).get("release"))
    Data.published().foreach: found =>
      releases.set(found)
      found.lastOption.foreach: newest =>
        Data.use(asked.filter(found.contains).getOrElse(newest))
        Data.about(Data.release).foreach(found => about.set(Some(found)))
    renderOnDomContentLoaded(dom.document.getElementById("app"), page)

  /** One connection, opened on demand and kept, with the small tables read in.
    *
    * Reopened when the release changes rather than reused: the tables are the release,
    * and keeping them while the paths move underneath is how a page answers under one
    * release and labels it another.
    */
  private def connection(): scala.concurrent.Future[Connection] =
    opening match
      case Some((release, pending)) if release == Data.release => pending
      case _ =>
        val pending = engine.now() match
          case Some(con) =>
            status.set(s"reading DPM ${Data.release}…")
            preload(con).map { ready => status.set(""); ready }
          case None =>
            status.set("loading the engine (8 MB, once)…")
            for
              bundle <- DuckDbModule.selectBundle(DuckDbModule.getJsDelivrBundles()).toFuture
              worker = makeWorker(bundle.mainWorker)
              db = new DuckDbModule.AsyncDuckDB(new DuckDbModule.VoidLogger(), worker)
              _ <- db.instantiate(bundle.mainModule, bundle.pthreadWorker).toFuture
              con <- db.connect().toFuture
              ready <- preload(con)
            yield
              engine.set(Some(ready))
              status.set("")
              ready
        opening = Some(Data.release -> pending)
        pending

  /** The release being opened for, and the work in flight.
    *
    * The future rather than the connection, because every keystroke in a slot asks for
    * the connection to fill its list: with only the finished connection remembered, two
    * callers before the first finished both read the five tables in again. That was
    * 3.7 MB of the 5.2 a session cost - headers read nine times over.
    */
  private var opening: Option[(String, scala.concurrent.Future[Connection])] = None

  /** Read the small tables in, for whichever release is current. 450 kB once, against
    * every question re-reading the files it names - measured, not assumed.
    */
  private def preload(con: Connection): scala.concurrent.Future[Connection] =
    Data.cached
      .foldLeft(scala.concurrent.Future.successful(())): (before, name) =>
        before.flatMap(_ => con.query(Data.preload(name)).toFuture.map(_ => ()))
      .map(_ => con)

  /** The worker has to come from this origin, so it is a blob that imports the CDN one -
    * a cross-origin script cannot be a worker directly.
    */
  private def makeWorker(url: String): dom.Worker =
    val blob = new dom.Blob(
      js.Array(s"""importScripts("$url");"""),
      new dom.BlobPropertyBag { `type` = "text/javascript" },
    )
    new dom.Worker(dom.URL.createObjectURL(blob))

  /** Fill the lists behind this question's slots.
    *
    * Run in order, because they depend on each other: the templates depend on the
    * framework, the members on the dimension. A slot whose query fails - usually because
    * the slot it depends on is empty or misspelt - simply has no list, and the field
    * stays typeable.
    */
  private def loadChoices(): Unit =
    val current = question.now()
    val filled = filledSlots(current)
    val wanted = current.slots.flatMap(slot => slot.options.map(slot.name -> _))
    connection().foreach: con =>
      wanted.foldLeft(scala.concurrent.Future.successful(())): (before, slot) =>
        val (name, forSlot) = slot
        before.flatMap: _ =>
          con
            .query(forSlot(filled))
            .toFuture
            .map: table =>
              // entries, not values: the Scala.js facade has the first and not the
              // second, and the query returns one column called value either way.
              val values = table
                .toArray()
                .toList
                .flatMap(row => js.Object.entries(row.toJSON()).headOption)
                .flatMap(entry => Option(entry._2))
                .map(_.toString)
              choices.update(_ + (name -> values))
            .recover { case _ => choices.update(_ - name) }

  /** The slots as they stand, with each question's own example standing in for a blank. */
  private def filledSlots(current: Question): String => String =
    slots.now().withDefault(name => current.slots.find(_.name == name).map(_.example).getOrElse(""))

  private def ask(): Unit =
    val current = question.now()
    val filled = filledSlots(current)
    val sql = current.sql(filled)
    toLocation(current, current.slots.map(slot => slot.name -> filled(slot.name)).toMap)
    running.set(true)
    status.set("")
    val started = System.currentTimeMillis()
    val result = for
      con <- connection()
      table <- con.query(sql).toFuture
    yield table
    result.onComplete:
      case Success(table) =>
        val rows = table.toArray().toList.map(row => js.Object.entries(row.toJSON()).toList)
        val columns = rows.headOption.map(_.map(entry => entry._1.toString)).getOrElse(Nil)
        answer.set(
          Some(
            Answer(
              columns = columns,
              // A datapoint id is an int64 and arrives as a BigInt, which has no JSON
              // representation at all - toString is the only honest conversion.
              rows = rows.map(_.map(entry => Option(entry._2).map(_.toString).getOrElse(""))),
              millis = System.currentTimeMillis() - started,
              sql = sql,
              source = current.source(filled),
            )
          )
        )
        running.set(false)
        loadChoices()
      case Failure(problem) =>
        // The message the engine gives is the useful part - a missing partition reads as
        // "No files found that match the pattern", which names the framework that is wrong.
        status.set(problem.getMessage)
        answer.set(None)
        running.set(false)

  /** Load the model, once, and only when asked. It is 376 MB at the smallest, so a page
    * that fetched it on load would cost every reader a download most of them do not want.
    */
  private def loadAssistant(): scala.concurrent.Future[Engine] =
    assistant.now() match
      case Some(ready) => scala.concurrent.Future.successful(ready)
      case None =>
        val progress = (report: js.Dynamic) => assistantStatus.set(s"loading the assistant… ${report.text}")
        val options = js.Dynamic.literal("initProgressCallback" -> progress).asInstanceOf[js.Object]
        WebLlm.CreateMLCEngine(assistantModel.now(), options).toFuture.map: ready =>
          assistant.set(Some(ready))
          assistantStatus.set("")
          ready

  /** Ask the model which question was meant, then run that question's own SQL.
    *
    * The model never sees the schema and never writes a statement: it picks an id and
    * fills slots, and anything it invents is refused rather than rounded to the nearest
    * question.
    */
  private def askInOwnWords(): Unit =
    val words = inOwnWords.now().trim
    if words.isEmpty then ()
    else
      assistantStatus.set("checking whether this browser can run a model…")
      // Two calls, because one schema cannot say "these slots, for that question" - it is
      // fixed before the model answers. A single call let 0.5B pick `rule` and fill in
      // `framework` and `table`, which the catalogue then had to refuse; asking for the
      // id, then for that question's own slots, makes each step one a small model can get
      // right.
      def request(instruction: String, schema: String) = js.Dynamic
        .literal(
          "messages" -> js.Array(
            js.Dynamic.literal("role" -> "system", "content" -> instruction),
            js.Dynamic.literal("role" -> "user", "content" -> words),
          ),
          "temperature" -> 0,
          // The schema has to be a string, and has to be there: without it the engine
          // fails with "Cannot pass non-string to std::string" rather than ignoring it.
          "response_format" -> js.Dynamic.literal("type" -> "json_object", "schema" -> schema),
        )
        .asInstanceOf[js.Object]

      def say(engine: Engine, instruction: String, schema: String): scala.concurrent.Future[String] =
        engine.chat.completions
          .create(request(instruction, schema))
          .toFuture
          .map(completion => completion.choices.asInstanceOf[js.Array[js.Dynamic]](0).message.content.toString)
      val chosen = for
        able <- Assistant.gpuReady()
        _ =
          if !able then
            throw js.JavaScriptException(
              "This browser cannot run a model: WebGPU has no adapter here. The questions "
                + "above work without one - that is what they are for."
            )
        ready <- loadAssistant()
        first <- say(ready, Assistant.prompt(), Assistant.questionSchema())
        picked = Assistant.pickQuestion(first)
        second <- picked match
          case Right(found) => say(ready, Assistant.slotPrompt(found), Assistant.slotSchema(found)).map(Some(_))
          case Left(_) => scala.concurrent.Future.successful(None)
      yield (picked, second)
      chosen.onComplete:
        case Success((Left(problem), _)) => assistantStatus.set(problem)
        case Success((Right(picked), filledIn)) =>
          Assistant.pickSlots(filledIn.getOrElse(""), picked) match
            case Left(problem) => assistantStatus.set(s"${picked.ask} — but $problem")
            case Right(filled) =>
              assistantStatus.set(s"the assistant read that as: ${picked.ask}")
              question.set(picked)
              slots.set(filled)
              ask()
        case Failure(problem) =>
          // js.JavaScriptException carries the message as the thrown value, not as
          // getMessage, which would otherwise read as "JavaScriptException".
          assistantStatus.set(problem match
            case js.JavaScriptException(value) => value.toString
            case other => other.getMessage)

  private def page: HtmlElement =
    div(
      cls := "page",
      h1("The EBA data point model, in your browser"),
      p(
        cls := "lede",
        "Pick a question and fill it in. Every answer shows the SQL that produced it, and the ",
        "file it read. No server: DuckDB-WASM queries parquet over HTTP range requests.",
      ),
      div(
        cls := "controls",
        child <-- releases.signal.map: found =>
          if found.sizeIs < 2 then emptyNode
          else
            label(
              "DPM release",
              select(
                onChange.mapToValue --> { release =>
                  Data.use(release)
                  answer.set(None)
                  status.set("")
                  about.set(None)
                  Data.about(release).foreach(found => about.set(Some(found)))
                },
                found.map(release => option(value := release, selected := release == Data.release, release)),
              ),
            )
        ,
        label(
          "Question",
          select(
            onChange.mapToValue --> { id =>
              question.set(Questions.byId(id))
              slots.set(Map.empty)
              answer.set(None)
              choices.set(Map.empty)
              loadChoices()
            },
            Questions.all.map(q => option(value := q.id, q.ask)),
          ),
        ),
        children <-- question.signal.map: current =>
          current.slots.map: slot =>
            label(
              slot.label,
              // An input with a datalist rather than a select: the lists run to hundreds
              // - 1052 templates, every member of a dimension - so they have to be
              // typeable and searchable, and a code pasted from a report has to go
              // straight in whether or not it is on the list.
              input(
                placeholder := slot.placeholder,
                listId := s"choices-${slot.name}",
                value <-- slots.signal.map(_.getOrElse(slot.name, slot.example)),
                onInput.mapToValue --> { text =>
                  slots.update(_ + (slot.name -> text))
                  loadChoices()
                },
                // On focus rather than on load: filling the lists needs the engine, and
                // the engine is 8 MB. Reaching for a field is the first sign that someone
                // means to ask something, which is when paying for it is right.
                onFocus --> (_ => loadChoices()),
              ),
              dataList(
                idAttr := s"choices-${slot.name}",
                children <-- choices.signal.map(_.getOrElse(slot.name, Nil).map(choice => option(value := choice))),
              ),
            )
        ,
        button(
          "Ask",
          disabled <-- running.signal,
          onClick --> (_ => ask()),
        ),
      ),
      child <-- about.signal.map:
        case Some(found) if found.draft =>
          p(
            cls := "draft",
            s"DPM ${Data.release} is a draft technical package: the EBA is still changing it, ",
            "so an answer from it is a draft answer too.",
          )
        case _ => emptyNode
      ,
      p(cls := "status", child.text <-- status.signal),
      detailsTag(
        cls := "assistant",
        summaryTag("…or ask in your own words (needs a model, 376 MB, loaded only if you ask)"),
        div(
          cls := "controls",
          label(
            "Model",
            select(
              // Dropping the engine as well as the name: it is loaded once and kept, so
              // choosing another model without this changes the label and nothing else.
              onChange.mapToValue --> { id =>
                assistantModel.set(id)
                assistant.set(None)
                assistantStatus.set("")
              },
              Assistant.models.map((id, shown) => option(value := id, shown)),
            ),
          ),
          label(
            "Question",
            input(
              cls := "words",
              placeholder := "which rows add up to which in F 12.01.a under FINREP9?",
              value <-- inOwnWords.signal,
              onInput.mapToValue --> (text => inOwnWords.set(text)),
              onKeyPress.filter(_.key == "Enter") --> (_ => askInOwnWords()),
            ),
          ),
          button("Ask the assistant", onClick --> (_ => askInOwnWords())),
        ),
        p(
          cls := "note",
          "It picks one of the questions above and fills it in - it never writes SQL. ",
          "What it chose is shown before the answer, so a wrong reading is visible rather ",
          "than silent.",
        ),
        p(cls := "status", child.text <-- assistantStatus.signal),
      ),
      child <-- answer.signal.map:
        case None => emptyNode
        case Some(result) =>
          div(
            cls := "answer",
            p(
              cls := "meta",
              s"${result.rows.size} row(s) in ${result.millis} ms, read from ${result.source}"
                + (if result.source.contains("/") then "" else s" (read into the engine once for DPM ${Data.release})"),
              // A table that stops at the limit without saying so reads as the whole
              // answer, which is the one way this page could mislead on its own.
              if result.rows.size == Questions.limit then
                span(cls := "limit", s" — the query's limit of ${Questions.limit}; narrow it to see the rest")
              else emptyNode,
            ),
            table(
              thead(tr(result.columns.map(th(_)))),
              tbody(result.rows.take(200).map(row => tr(row.map(td(_))))),
            ),
            detailsTag(summaryTag("the SQL that answered it"), pre(code(result.sql))),
          )
      ,
      footerTag(
        cls := "source",
        // The permission is conditional on this, so it is part of the page rather than
        // a line in a repository the reader of a published copy will never see.
        "Derived from the EBA DPM 2.0 database. Reproduction of EBA material is authorised ",
        "provided the source is acknowledged (",
        a(href := "https://www.eba.europa.eu/legal-notice", "eba.europa.eu/legal-notice"),
        "). This page is not published by the EBA and is not endorsed by it; for the ",
        "database itself, and for anything a report is filed against, go to ",
        a(href := "https://www.eba.europa.eu/risk-and-data-analysis/reporting/dpm-data-dictionary", "the EBA"),
        ".",
      ),
    )
