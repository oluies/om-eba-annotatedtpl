package dpm

import scala.scalajs.js

/** The half of the assistant that can be checked without a GPU.
  *
  * The model itself cannot run in a headless browser - Playwright's Chromium has no
  * WebGPU at all - so the prompt it is given and the answer it comes back with are
  * tested here, and the page is tested for saying so plainly when WebGPU is missing.
  */
class AssistantSuite extends munit.FunSuite:

  test("the prompt lists every question the page can answer") {
    val prompt = Assistant.prompt()
    Questions.all.foreach(question => assert(prompt.contains(question.id), s"${question.id} is not in the prompt"))
    Questions.all.flatMap(_.slots).foreach(slot => assert(prompt.contains(s""""${slot.name}"""")))
  }

  test("the prompt is built from the catalogue, so a new question is one it knows") {
    val invented = Question("invented", "Does this reach the prompt?", Nil, _ => "SELECT 1", _ => "nowhere")
    assert(Assistant.prompt(List(invented)).contains("invented"))
  }

  test("a filled-in answer becomes a question and its slots") {
    val answer = """{"question": "sums", "slots": {"table": "F_12.01.a", "module": "FINREP9"}}"""
    Assistant.parse(answer) match
      case Right((question, slots)) =>
        assertEquals(question.id, "sums")
        assertEquals(slots, Map("table" -> "F_12.01.a", "module" -> "FINREP9"))
      case Left(problem) => fail(problem)
  }

  test("prose around the JSON is tolerated, because small models wrap it") {
    val answer = """Sure! Here you go:
      |```json
      |{"question": "rule", "slots": {"rule_code": "v0174_m"}}
      |```""".stripMargin
    assert(Assistant.parse(answer).isRight)
  }

  test("a question that does not exist is refused, not rounded to the nearest one") {
    Assistant.parse("""{"question": "sumz", "slots": {}}""") match
      case Left(problem) => assert(problem.contains("does not exist"), problem)
      case Right(_) => fail("an invented id must not resolve")
  }

  test("a slot the question does not have is refused") {
    val answer = """{"question": "rule", "slots": {"rule_code": "v0174_m", "framework": "FINREP"}}"""
    Assistant.parse(answer) match
      case Left(problem) => assert(problem.contains("framework"), problem)
      case Right(_) => fail("an invented slot must not be silently dropped")
  }

  test("no question fitting is an answer, and says so") {
    Assistant.parse("""{"question": null}""") match
      case Left(problem) => assert(problem.contains("no question that fits"), problem)
      case Right(_) => fail("null must not resolve to a question")
  }

  test("an answer with no JSON at all is reported rather than guessed at") {
    assert(Assistant.parse("I think you want the sums question.").isLeft)
  }

  test("an empty slot is dropped, so the question's own example fills it") {
    val answer = """{"question": "sums", "slots": {"table": "F_12.01.a", "module": ""}}"""
    assertEquals(Assistant.parse(answer).map(_._2), Right(Map("table" -> "F_12.01.a")))
  }

  test("every model offered says what it costs to download") {
    Assistant.models.foreach((id, shown) => assert(shown.contains("MB") || shown.contains("GB"), id))
  }

  test("the schema is a string, names every question id, and allows no other slot") {
    val schema = Assistant.schema()
    assert(schema.contains("\"question\""))
    Questions.all.foreach(question => assert(schema.contains(s""""${question.id}""""), question.id))
    Questions.all.flatMap(_.slots).map(_.name).distinct.foreach(name => assert(schema.contains(s""""$name"""")))
    assert(schema.contains("\"additionalProperties\": false"))
    assert(js.JSON.parse(schema) != null, "it has to parse as JSON, because the engine parses it")
  }

  test("the prompt shows worked examples, because a refusal is the easiest instruction to follow") {
    val prompt = Assistant.prompt()
    assert(prompt.contains("Q: "), "no worked example")
    assert(prompt.contains("""A: {"question": """"), "the example does not show the shape")
    // Not the whole sentence: stripMargin keeps the wrap, so the phrase spans a newline.
    assert(prompt.contains("about something else entirely"))
  }

  test("step one's grammar offers the ids and nothing else") {
    val schema = Assistant.questionSchema()
    Questions.all.foreach(question => assert(schema.contains(s""""${question.id}""""), question.id))
    assert(!schema.contains("slots"), "the first step does not ask for slots")
  }

  test("step two's grammar is one question's own slots") {
    val sums = Questions.byId("sums")
    val schema = Assistant.slotSchema(sums)
    sums.slots.foreach(slot => assert(schema.contains(s""""${slot.name}""""), slot.name))
    assert(!schema.contains("\"dimension\""), "a slot of another question must not be allowed")
    assert(schema.contains("\"additionalProperties\": false"))
  }

  test("step two's answer is checked against that question") {
    val rule = Questions.byId("rule")
    assertEquals(Assistant.pickSlots("""{"slots": {"rule_code": "v0174_m"}}""", rule), Right(Map("rule_code" -> "v0174_m")))
    assert(Assistant.pickSlots("""{"slots": {"framework": "FINREP"}}""", rule).isLeft, "a foreign slot is refused")
  }

  test("step two tolerates the slots being sent unwrapped, which small models do") {
    val rule = Questions.byId("rule")
    assertEquals(Assistant.pickSlots("""{"rule_code": "v0174_m"}""", rule), Right(Map("rule_code" -> "v0174_m")))
  }

  test("a question's other wordings reach the prompt") {
    val prompt = Assistant.prompt()
    assert(prompt.contains("also asked as:"))
    assert(prompt.contains("totals, subtotals"), "the sums question's hints are missing")
  }
