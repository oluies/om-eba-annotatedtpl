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

  /** The row cap from the URL, so a link that was worth sending because it has 900 rows
    * arrives with 900 rather than with 200 and a note saying there are more.
    */
  private def limitFromLocation(): Int =
    Option(new dom.URLSearchParams(dom.window.location.search).get("rows"))
      .flatMap(_.toIntOption)
      .map(asked => asked.max(1).min(Questions.mostRows))
      .getOrElse(Questions.limit)

  private def toLocation(question: Question, filled: Map[String, String]): Unit =
    val params = new dom.URLSearchParams()
    params.set("q", question.id)
    if rowLimit.now() != Questions.limit then params.set("rows", rowLimit.now().toString)
    if Data.release.nonEmpty then params.set("release", Data.release)
    question.slots.foreach(slot => params.set(slot.name, filled.getOrElse(slot.name, slot.example)))
    dom.window.history.replaceState((), "", s"?${params.toString}")

  /** A link into the code that does what the paragraph just described.
    *
    * `main` rather than a tag: the published page and the branch it was built from are
    * the same thing here, and a reader following a link wants the file as it is now.
    */
  private val repo = "https://github.com/oluies/om-eba-annotatedtpl"

  private def srcLink(path: String, shown: String) = a(href := s"$repo/blob/main/$path", shown)

  private val engine = Var[Option[Connection]](None)
  private val assistant = Var[Option[Engine]](None)
  private val assistantModel = Var(Assistant.models.head._1)
  private val assistantStatus = Var("")
  private val inOwnWords = Var("")
  private val rowLimit = Var(Questions.limit)
  private val releases = Var(List.empty[String])
  private val choices = Var(Map.empty[String, List[String]])
  private val about = Var(Option.empty[Data.About])
  private val status = Var("")
  private val running = Var(false)
  private val answer = Var(Option.empty[Answer])
  private val question = Var(fromLocation()._1)
  private val slots = Var(fromLocation()._2)

  final case class Answer(
      columns: List[String],
      rows: List[List[String]],
      millis: Long,
      sql: String,
      source: String,
      limit: Int,
  )

  def main(args: Array[String]): Unit =
    // The release comes from the URL when there is one, so a shared link answers under
    // the release it was asked under rather than under whatever is newest today.
    val asked = Option(new dom.URLSearchParams(dom.window.location.search).get("release"))
    Data.published().foreach: found =>
      releases.set(found)
      found.lastOption.foreach: newest =>
        Data.use(asked.filter(found.contains).getOrElse(newest))
        Data.about(Data.release).foreach(found => about.set(Some(found)))
    rowLimit.set(limitFromLocation())
    val mount = dom.document.getElementById("app")
    // index.html says "loading…" so a reader looking at a blank page knows the bundle is
    // still coming. Laminar appends, so without this the word stays above the page.
    mount.textContent = ""
    renderOnDomContentLoaded(mount, page)

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
              _ = Files.use(db)
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
    // The five files are fetched together and the statements run in order. Registering is
    // what has to be serial - one connection, one statement at a time - and the network is
    // not: folding over `localise` fetched 464 kB one file after another, so the slowest
    // link paid for all five in sequence.
    scala.concurrent.Future
      .traverse(Data.cached)(name => Files.localise(Data.preload(name)))
      .flatMap: statements =>
        statements.foldLeft(scala.concurrent.Future.successful(())): (before, statement) =>
          before.flatMap(_ => con.query(statement).toFuture.map(_ => ()))
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
          Files
            .localise(forSlot(filled))
            .flatMap(con.query(_).toFuture)
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
    val rows = rowLimit.now()
    val sql = current.sql(filled, rows)
    toLocation(current, current.slots.map(slot => slot.name -> filled(slot.name)).toMap)
    running.set(true)
    status.set("")
    val started = System.currentTimeMillis()
    val result = for
      con <- connection()
      // The statement shown under the answer keeps the URL; this is the copy DuckDB runs.
      statement <- Files.localise(sql)
      table <- con.query(statement).toFuture
    yield table
    result.onComplete:
      case Success(table) =>
        val answered = table.toArray().toList.map(row => js.Object.entries(row.toJSON()).toList)
        val columns = answered.headOption.map(_.map(entry => entry._1.toString)).getOrElse(Nil)
        answer.set(
          Some(
            Answer(
              columns = columns,
              // A datapoint id is an int64 and arrives as a BigInt, which has no JSON
              // representation at all - toString is the only honest conversion.
              rows = answered.map(_.map(entry => Option(entry._2).map(_.toString).getOrElse(""))),
              millis = System.currentTimeMillis() - started,
              sql = sql,
              source = current.source(filled),
              limit = rows,
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

  /** What stands where the answer will be, before anything has been asked.
    *
    * The page opened on a row of controls and then a screenful of nothing, which tells a
    * reader neither what it can answer nor that the answer appears here. These are three
    * questions worth asking, as buttons that fill the blanks and ask. Nothing is loaded
    * until one is pressed - that is why this is a set of starting points and not an
    * answer rendered at startup, which would cost every visitor the 8 MB engine.
    */
  private def starters: HtmlElement =
    val examples = List(
      (
        "Which cells does C_01.00 have?",
        "cells",
        Map("framework" -> "COREP", "table" -> "C_01.00", "module" -> "COREP_OF"),
      ),
      ("What does v0174_m check, and is it still switched on?", "rule", Map("rule_code" -> "v0174_m")),
      (
        "Which rules reach F_02.00?",
        "rules",
        Map("framework" -> "FINREP", "table" -> "F_02.00", "module" -> "FINREP9"),
      ),
    )
    div(
      cls := "starters",
      p(
        cls := "what",
        s"${Questions.all.size} questions, each one a statement that is known to be right and whose only ",
        "variables are the blanks above. Start with one of these:",
      ),
      div(
        cls := "examples",
        examples.map: (asked, id, filled) =>
          button(
            tpe := "button",
            asked,
            // The Ask button is disabled while a query runs and these were not, although
            // they stay on screen for the whole of the first one - there is no answer yet.
            // Two clicks during the 8 MB engine load started two queries, and the slower
            // one landed last: C_01.00's cells under a question that reads `rule`, which
            // is the page disagreeing with itself that the dropdown above guards against.
            disabled <-- running.signal,
            onClick --> { _ =>
              question.set(Questions.byId(id))
              slots.set(filled)
              // What the dropdown does for the same reason: `module` has no options query,
              // so another question's module list would survive into this one's datalist.
              choices.set(Map.empty)
              ask()
            },
          ),
      ),
      p(
        cls := "elsewhere",
        "Or read a template rather than query it: ",
        a(href := "templates/", "a page per template"),
        " — every cell, the official Swedish and German beside the English, what has changed ",
        "since the first release, and which rules check it.",
      ),
    )

  private def page: HtmlElement =
    div(
      cls := "page",
      h1("The EBA data point model, in your browser"),
      p(
        cls := "lede",
        "Pick a question and fill it in. Every answer shows the SQL that produced it, and the ",
        "file it read. No server: the parquet is fetched into DuckDB-WASM and queried in ",
        "your browser.",
      ),
      Appearance.control,
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
            // Bound rather than set once: a link carries its question, and a dropdown
            // reading "Which cells does a template have?" over an answer about
            // deactivated rules is a page disagreeing with itself.
            value <-- question.signal.map(_.id),
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
        child <-- question.signal.map: current =>
          if !current.limited then emptyNode
          else
            label(
              "Rows",
              input(
                cls := "rows",
                tpe := "number",
                minAttr := "1",
                maxAttr := Questions.mostRows.toString,
                stepAttr := "100",
                value <-- rowLimit.signal.map(_.toString),
                // Clamped rather than refused: a reader who means "all of it" types a
                // large number, and the honest answer is the most the page will render,
                // not an error about a field.
                onInput.mapToValue --> { text =>
                  text.toIntOption.foreach(asked => rowLimit.set(asked.max(1).min(Questions.mostRows)))
                },
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
      child <-- answer.signal.map:
        case None => starters
        case Some(_) => emptyNode
      ,
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
          "than silent. ",
          a(href := "#what-it-does", "What it does, and why so little"),
          ".",
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
              if result.rows.size == result.limit then
                span(cls := "limit", s" — the query's limit of ${result.limit}; raise Rows, or narrow the question")
              else emptyNode,
            ),
            table(
              thead(tr(result.columns.map(th(_)))),
              tbody(result.rows.map(row => tr(row.map(td(_))))),
            ),
            detailsTag(summaryTag("the SQL that answered it"), pre(code(result.sql))),
          )
      ,
      detailsTag(
        cls := "about",
        idAttr := "what-it-does",
        summaryTag("What does this assistant do?"),
        p(
          "It chooses. The page has ",
          b(s"${Questions.all.size} questions"),
          ", each one a SQL statement that is known to be right and whose only variables are ",
          "the blanks you fill; the model's whole job is to say which of them you asked and ",
          "what goes in the blanks. It never writes SQL, and there is no generated SQL to ",
          "check, because none is generated. ",
          srcLink("web/src/dpm/Questions.scala", "Questions.scala"),
          " is that catalogue, statements and all.",
        ),
        p(
          "It does it in two steps. First: which question - answered against a JSON schema ",
          "whose enum is exactly those ids, so a twelfth cannot be invented. Then, with the ",
          "question settled: that question's own slots, against a schema that admits no ",
          "other names. One step let a 0.5B model pick ",
          em("what does a validation code mean"),
          " and then fill in a template and a framework, which the catalogue had to refuse. ",
          "Temperature is zero, there are no tool calls, no retries and no second guess. ",
          srcLink("web/src/dpm/Assistant.scala", "Assistant.scala"),
          " holds the prompts, the schemas and the parsing - all pure, so they are tested ",
          "without a GPU in ",
          srcLink("web/test/dpm/AssistantSuite.scala", "AssistantSuite.scala"),
          "; ",
          srcLink("web/src/dpm/Main.scala", "Main.scala"),
          " is the two calls and what happens to the answers.",
        ),
        p(
          "Both answers are then checked against the catalogue again, and an id or a slot ",
          "name that is not in it is refused rather than bent into the nearest one: guessing ",
          s"which of ${Questions.all.size} questions was meant is how a reader gets a confident answer to ",
          "something they did not ask. What it settled on is printed before the answer, and ",
          "the statement it ran is under it.",
        ),
        p(
          "Why so little is left to the model: a 360M model can pick one of ",
          s"${Questions.all.size} ",
          "and copy F_12.01.a out of your sentence. What it cannot do is write correct SQL ",
          "over this schema, where F04041_r0070_c0015 looks exactly as plausible as a real ",
          "cell code, where qGDF is a real property that is the wrong one, and where a near ",
          "miss in a dimension's wording matches nothing rather than erroring. The dropdowns ",
          "exist for the same reason - a member is \"Credit institutions\", trailing space ",
          "and all.",
        ),
        p(
          "It runs in your browser, on WebGPU, through ",
          a(href := "https://github.com/mlc-ai/web-llm", "MLC WebLLM"),
          ", and is downloaded only once you ask for it. Nothing you type leaves the tab, ",
          "and neither does anything you query: the data is parquet read over HTTP range ",
          "requests by DuckDB-WASM, built by ",
          srcLink("source/gen_wasm_data.py", "gen_wasm_data.py"),
          " and read through ",
          srcLink("web/src/dpm/DuckDb.scala", "DuckDb.scala"),
          ". The whole page is ",
          a(href := repo, "oluies/om-eba-annotatedtpl"),
          ", MIT.",
        ),
      ),
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
        ". Visits are counted by ",
        a(href := "https://www.goatcounter.com/help/privacy", "GoatCounter"),
        ": no cookies, no cross-site identifier, and nothing from the question you asked ",
        "beyond which of the eleven it was.",
      ),
    )
