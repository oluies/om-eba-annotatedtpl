package dpm

/** The rewrite that keeps DuckDB off HTTP.
  *
  * The reason for it is a hazard nothing here can see: Pages serves the parquet gzipped,
  * so the content-length is the compressed length while a byte range comes from the
  * uncompressed file, and httpfs reads the footer at the wrong offset. These are the parts
  * of the answer that are pure - which files a statement names, and what it becomes.
  */
class FilesSuite extends munit.FunSuite:

  val partition = "https://oluies.github.io/om-eba-annotatedtpl/data/4.4/cells/framework=FINREP/data_0.parquet"
  val rules = "https://oluies.github.io/om-eba-annotatedtpl/data/4.4/rules.parquet"

  test("a statement naming no file is left alone"):
    val sql = "SELECT DISTINCT framework AS value FROM modules ORDER BY 1"
    assertEquals(Files.reads(sql), Nil)
    assertEquals(Files.rewritten(sql, Map.empty), sql)

  test("every file a statement names is found, once"):
    val sql = s"SELECT * FROM '$partition' a JOIN '$rules' b USING (operation_vid) WHERE a.x = '$partition'"
    assertEquals(Files.reads(sql), List(partition, rules))

  test("the name keeps the extension, because DuckDB picks its reader from it"):
    assert(Files.named(partition).endsWith(".parquet"), Files.named(partition))
    assert(Files.named("https://example.org/its_labels.csv").endsWith(".csv"))

  test("the name carries nothing a SQL string would end early"):
    val name = Files.named(partition)
    assert(!name.contains("'"), name)
    assert(!name.contains("/"), name)
    assert(!name.contains("="), name)

  test("two files of the same name in different releases stay apart"):
    val other = partition.replace("4.4", "4.3")
    assertNotEquals(Files.named(partition), Files.named(other))

  test("the statement DuckDB runs names the registered bytes and not the URL"):
    val sql = s"SELECT * FROM '$partition' WHERE table_code = 'F_04.01'"
    val ran = Files.rewritten(sql, Map(partition -> Files.named(partition)))
    assert(!ran.contains("https://"), ran)
    assert(ran.contains(Files.named(partition)), ran)
    assert(ran.contains("'F_04.01'"), "the rewrite touched something that is not a file")
