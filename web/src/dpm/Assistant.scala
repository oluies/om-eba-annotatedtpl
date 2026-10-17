package dpm

import scala.scalajs.js
import scala.scalajs.js.annotation.JSImport

/** A small model in the browser, asked to pick a question and fill its slots.
  *
  * It never writes SQL. The page has eleven statements that are known to be right, and
  * the model's whole job is to choose one and fill in its blanks - `{"question": "sums",
  * "slots": {"table": "F_12.01.a", "module": "FINREP9"}}`. A 360M model can do that; what
  * it cannot do is write correct SQL over a schema where `F04041_r0070_c0015` looks
  * exactly as plausible as a real cell code, and where a near miss in a dimension's
  * wording matches nothing rather than erroring.
  *
  * Everything here except the engine call is pure, so the prompt and the parsing are
  * tested without a GPU - which matters, because the model itself cannot run in a
  * headless browser and will not run on most phones.
  */
object Assistant:

  /** The models offered, smallest first, with what the download costs. */
  val models: List[(String, String)] = List(
    "SmolLM2-360M-Instruct-q4f16_1-MLC" -> "SmolLM2 360M (~376 MB)",
    "Qwen2.5-0.5B-Instruct-q4f16_1-MLC" -> "Qwen2.5 0.5B (~945 MB)",
    "Qwen2.5-1.5B-Instruct-q4f16_1-MLC" -> "Qwen2.5 1.5B (~1.6 GB)",
  )

  /** What the model is told. Pure, and built from the catalogue rather than written out,
    * so a question added to `Questions` is one the assistant knows about.
    */
  def prompt(questions: List[Question] = Questions.all): String =
    val catalogue = questions
      .map: question =>
        val slots = question.slots.map(slot => s"""    "${slot.name}": e.g. "${slot.example}"""").mkString("\n")
        s"""  ${question.id}: ${question.ask}\n$slots"""
      .mkString("\n")
    s"""You turn a question about the EBA data point model into one of these, and nothing else.
       |
       |$catalogue
       |
       |Answer with JSON only: {"question": "<id>", "slots": {"<name>": "<value>"}}.
       |Use the ids and slot names exactly as written above. Copy codes from the question as
       |they are written - F_12.01.a, v0174_m, dp152217, qCDF. If no question fits, answer
       |{"question": null}.""".stripMargin

  /** The model's answer, checked against the catalogue.
    *
    * A model that invents a question id or a slot name is refused rather than coerced
    * into the nearest one: guessing which of eleven questions was meant is how a reader
    * gets a confident answer to something they did not ask.
    */
  def parse(answer: String, questions: List[Question] = Questions.all): Either[String, (Question, Map[String, String])] =
    val json = answer.dropWhile(_ != '{').reverse.dropWhile(_ != '}').reverse
    if json.isEmpty then Left(s"the assistant answered with no JSON: ${answer.take(120)}")
    else
      try
        val parsed = js.JSON.parse(json)
        val id = Option(parsed.question).map(_.toString).filter(_ != "null").getOrElse("")
        questions.find(_.id == id) match
          case None if id.isEmpty => Left("the assistant found no question that fits. Pick one above.")
          case None => Left(s"the assistant picked a question that does not exist: $id")
          case Some(question) =>
            val filledIn = Option(parsed.slots)
              .filter(slots => !js.isUndefined(slots) && slots != null)
              .map(slots => js.Object.entries(slots.asInstanceOf[js.Object]).toList)
              .getOrElse(Nil)
              .map(entry => entry._1.toString -> Option(entry._2).map(_.toString).getOrElse(""))
              .toMap
            val known = question.slots.map(_.name).toSet
            val unknown = filledIn.keySet -- known
            if unknown.nonEmpty then Left(s"the assistant filled in something this question has no slot for: ${unknown.toList.sorted.mkString(", ")}")
            else Right(question -> filledIn.filter((_, value) => value.nonEmpty))
      catch case problem: Throwable => Left(s"the assistant's answer was not JSON: ${problem.getMessage}")

  /** Whether this browser can actually run a model, which `navigator.gpu` alone does not
    * answer.
    *
    * Chromium exposes the object and then returns null from `requestAdapter()` when there
    * is no GPU to drive - headless is exactly that case. Asking for the adapter is the
    * only honest check, and it is cheap; the alternative is sending someone off to
    * download 376 MB that cannot run.
    */
  def gpuReady(): scala.concurrent.Future[Boolean] =
    import scala.concurrent.ExecutionContext.Implicits.global
    import scala.scalajs.js.Thenable.Implicits.*
    if js.typeOf(js.Dynamic.global.navigator.selectDynamic("gpu")) == "undefined" then
      scala.concurrent.Future.successful(false)
    else
      js.Dynamic.global.navigator.gpu
        .requestAdapter()
        .asInstanceOf[js.Promise[js.Any]]
        .toFuture
        .map(adapter => adapter != null && !js.isUndefined(adapter))
        .recover { case _ => false }

@js.native
trait Completions extends js.Object:
  def create(request: js.Object): js.Promise[js.Dynamic] = js.native

@js.native
trait Chat extends js.Object:
  val completions: Completions = js.native

@js.native
trait Engine extends js.Object:
  val chat: Chat = js.native

@js.native
@JSImport("https://esm.run/@mlc-ai/web-llm", JSImport.Namespace)
object WebLlm extends js.Object:
  def CreateMLCEngine(model: String, options: js.Object): js.Promise[Engine] = js.native
