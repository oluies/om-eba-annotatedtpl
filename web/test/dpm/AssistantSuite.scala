package dpm

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
