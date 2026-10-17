package dpm

/** The questions the page can answer, as data.
  *
  * A question is a template and the slots a reader fills, never free SQL. The whole pack
  * exists because `F04041_r0070_c0015` looks exactly as plausible as a real cell code and
  * `qGDF` resolves to a real property that is the wrong one; a page that lets a model - or
  * a hurried human - write its own SQL over this schema invites the same mistake back in.
  *
  * `sql` takes the filled slots and returns a statement whose only variables are the
  * slots. The page shows it next to the answer, because a number without the query that
  * produced it is a number nobody can check.
  */
final case class Slot(name: String, label: String, placeholder: String, example: String)

final case class Question(
    id: String,
    ask: String,
    slots: List[Slot],
    sql: (String => String) => String,
    reads: String => String,
):
  /** Where the answer comes from, for the line under the results. */
  def source(filled: String => String): String = reads(filled("framework"))

object Questions:
  /** Parquet is split by framework, so a question names the partition it reads. One
    * question reads one partition: 176 kB for FINREP rather than 3.3 MB for all of them.
    */
  private def partition(table: String)(framework: String): String =
    Data.url(s"$table/framework=$framework/data_0.parquet")

  private def whole(table: String)(framework: String): String = Data.url(s"$table.parquet")

  private val framework = Slot("framework", "Framework", "FINREP, COREP, DORA…", "FINREP")
  private val template = Slot("table", "Template", "F_12.01.a", "F_12.01.a")

  val all: List[Question] = List(
    Question(
      id = "cells",
      ask = "Which cells does a template have?",
      slots = List(framework, template, Slot("module", "Module", "FINREP9", "FINREP9")),
      sql = filled => s"""
        |SELECT row_code, row_label, column_code, column_label, datapoint, cell_code
        |FROM   '${partition("cells")(filled("framework"))}'
        |WHERE  table_code = '${filled("table")}' AND module = '${filled("module")}'
        |ORDER  BY row_code, column_code
        |LIMIT  200""".stripMargin.trim,
      reads = partition("cells"),
    ),
    Question(
      id = "dimensions",
      ask = "What does a template break down by?",
      slots = List(framework, template),
      sql = filled => s"""
        |SELECT   dimension, count(DISTINCT member) AS members,
        |         string_agg(DISTINCT member, ', ' ORDER BY member) AS wording
        |FROM     '${partition("cell_members")(filled("framework"))}'
        |WHERE    table_code = '${filled("table")}'
        |GROUP BY dimension
        |ORDER BY dimension""".stripMargin.trim,
      reads = partition("cell_members"),
    ),
    Question(
      id = "rule",
      ask = "What does a validation code mean?",
      slots = List(Slot("rule_code", "Rule code", "v0174_m", "v0174_m")),
      // The engine's occurrence number is stripped here as the lookup strips it: v3775_s_62
      // is the 62nd application of v3775_s, and the model has the rule, never the occurrence.
      sql = filled => s"""
        |SELECT module, taxonomy_version, dpm_release, severity, active,
        |       from_submission_date, expression
        |FROM   '${whole("rules")("")}'
        |WHERE  rule_code = regexp_replace('${filled("rule_code")}', '_[0-9]+$$', '')
        |ORDER  BY module, taxonomy_version""".stripMargin.trim,
      reads = whole("rules"),
    ),
    Question(
      id = "keys",
      ask = "What are a template's key dimensions?",
      slots = List(framework, template),
      sql = filled => s"""
        |SELECT code, label, property_code, property
        |FROM   '${whole("headers")("")}'
        |WHERE  table_code = '${filled("table")}' AND is_key
        |ORDER  BY code""".stripMargin.trim,
      reads = whole("headers"),
    ),
    Question(
      id = "modules",
      ask = "Which module versions is a framework reported under?",
      slots = List(framework),
      sql = filled => s"""
        |SELECT module, taxonomy_version, dpm_release, from_reference_date,
        |       to_reference_date, do_not_use
        |FROM   '${whole("modules")("")}'
        |WHERE  framework = '${filled("framework")}'
        |ORDER  BY module, taxonomy_version""".stripMargin.trim,
      reads = whole("modules"),
    ),
  )

  def byId(id: String): Question = all.find(_.id == id).getOrElse(all.head)
