//> using scala 3.9.0
//> using platform js
//> using jsModuleKind es
//> using jsModuleSplitStyleStr fewestmodules
//> using dep com.raquo::laminar::17.2.1

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
    question.slots.foreach(slot => params.set(slot.name, filled.getOrElse(slot.name, slot.example)))
    dom.window.history.replaceState((), "", s"?${params.toString}")

  private val engine = Var[Option[Connection]](None)
  private val status = Var("")
  private val running = Var(false)
  private val answer = Var(Option.empty[Answer])
  private val question = Var(fromLocation()._1)
  private val slots = Var(fromLocation()._2)

  final case class Answer(columns: List[String], rows: List[List[String]], millis: Long, sql: String, source: String)

  def main(args: Array[String]): Unit =
    renderOnDomContentLoaded(dom.document.getElementById("app"), page)

  /** One connection, opened on demand and kept. */
  private def connection(): scala.concurrent.Future[Connection] =
    engine.now() match
      case Some(con) => scala.concurrent.Future.successful(con)
      case None =>
        status.set("loading the engine (8 MB, once)…")
        for
          bundle <- DuckDbModule.selectBundle(DuckDbModule.getJsDelivrBundles()).toFuture
          worker = makeWorker(bundle.mainWorker)
          db = new DuckDbModule.AsyncDuckDB(new DuckDbModule.VoidLogger(), worker)
          _ <- db.instantiate(bundle.mainModule, bundle.pthreadWorker).toFuture
          con <- db.connect().toFuture
        yield
          engine.set(Some(con))
          status.set("")
          con

  /** The worker has to come from this origin, so it is a blob that imports the CDN one -
    * a cross-origin script cannot be a worker directly.
    */
  private def makeWorker(url: String): dom.Worker =
    val blob = new dom.Blob(
      js.Array(s"""importScripts("$url");"""),
      new dom.BlobPropertyBag { `type` = "text/javascript" },
    )
    new dom.Worker(dom.URL.createObjectURL(blob))

  private def ask(): Unit =
    val current = question.now()
    val filled = slots.now().withDefault(name => current.slots.find(_.name == name).map(_.example).getOrElse(""))
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
      case Failure(problem) =>
        // The message the engine gives is the useful part - a missing partition reads as
        // "No files found that match the pattern", which names the framework that is wrong.
        status.set(problem.getMessage)
        answer.set(None)
        running.set(false)

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
        label(
          "Question",
          select(
            onChange.mapToValue --> { id =>
              question.set(Questions.byId(id))
              slots.set(Map.empty)
              answer.set(None)
            },
            Questions.all.map(q => option(value := q.id, q.ask)),
          ),
        ),
        children <-- question.signal.map: current =>
          current.slots.map: slot =>
            label(
              slot.label,
              input(
                placeholder := slot.placeholder,
                value <-- slots.signal.map(_.getOrElse(slot.name, slot.example)),
                onInput.mapToValue --> (text => slots.update(_ + (slot.name -> text))),
              ),
            )
        ,
        button(
          "Ask",
          disabled <-- running.signal,
          onClick --> (_ => ask()),
        ),
      ),
      p(cls := "status", child.text <-- status.signal),
      child <-- answer.signal.map:
        case None => emptyNode
        case Some(result) =>
          div(
            cls := "answer",
            p(
              cls := "meta",
              s"${result.rows.size} row(s) in ${result.millis} ms, read from ${result.source}",
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
    )
