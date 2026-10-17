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
  private val module = Slot("module", "Module", "FINREP9", "FINREP9")

  /** Enough rows to read, few enough to render. The page says when it is reached, because
    * a table that stops at 200 without saying so reads as the whole answer.
    */
  val limit = 200

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
        |LIMIT  $limit""".stripMargin.trim,
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
      id = "aggregate",
      ask = "Which cells make up an aggregate? (one dimension, one member)",
      slots = List(
        framework,
        Slot("table", "Template", "F_04.04.1", "F_04.04.1"),
        Slot("dimension", "Dimension", "Counterparty sector", "Counterparty sector"),
        Slot("member", "Member", "Credit institutions", "Credit institutions"),
      ),
      // The wording has to come from the dimensions question: a near miss matches
      // nothing, and "Credit institutions " with a trailing space is a real item in the
      // model next to a clean one. trim on both sides is what the lookup does too.
      sql = filled => s"""
        |SELECT   m.table_code, m.datapoint, c.row_code, c.row_label, c.column_code, c.column_label
        |FROM     '${partition("cell_members")(filled("framework"))}' m
        |JOIN     '${partition("cells")(filled("framework"))}' c USING (table_code, datapoint)
        |WHERE    m.table_code = '${filled("table")}'
        |     AND trim(lower(m.dimension)) = trim(lower('${filled("dimension")}'))
        |     AND trim(lower(m.member)) = trim(lower('${filled("member")}'))
        |GROUP BY ALL
        |ORDER BY c.row_code, c.column_code
        |LIMIT    $limit""".stripMargin.trim,
      reads = partition("cell_members"),
    ),
    Question(
      id = "sums",
      ask = "Which rows add up to which?",
      // 1780 edges for every framework and every module version: 17 kB, so no partition.
      slots = List(template, module),
      sql = filled => s"""
        |SELECT total_row, addend_rows, columns, sheets, rule_code, severity
        |FROM   '${whole("sums")("")}'
        |WHERE  table_code = '${filled("table")}' AND module = '${filled("module")}'
        |ORDER  BY total_row, rule_code""".stripMargin.trim,
      reads = whole("sums"),
    ),
    Question(
      id = "rules",
      ask = "Which validation rules reach a template?",
      slots = List(framework, Slot("table", "Template", "C_01.00", "C_01.00"), Slot("module", "Module", "COREP_OF", "COREP_OF")),
      // MATERIALIZED, not just a CTE: DuckDB inlines a plain one, so naming the
      // partition twice reads it twice - 1.9 MB for COREP where the file is 0.5.
      sql = filled => s"""
        |WITH cells AS MATERIALIZED (SELECT * FROM '${partition("rule_cells")(filled("framework"))}'),
        |     here AS (SELECT DISTINCT operation_vid FROM cells WHERE table_code = '${filled("table")}')
        |SELECT   r.rule_code, r.severity, r.active, r.taxonomy_version, r.dpm_release,
        |         list_sort(list(DISTINCT rc.row_code)) AS rows_here,
        |         count(DISTINCT rc.table_code) AS templates_named
        |FROM     '${whole("rules")("")}' r
        |JOIN     here USING (operation_vid)
        |JOIN     cells rc USING (operation_vid)
        |WHERE    r.module = '${filled("module")}'
        |GROUP BY ALL
        |ORDER BY r.rule_code
        |LIMIT    $limit""".stripMargin.trim,
      reads = partition("rule_cells"),
    ),
    Question(
      id = "datapoint",
      ask = "What is this reported datapoint id?",
      slots = List(framework, Slot("datapoint", "Datapoint", "152217 or dp152217", "152217")),
      // A report writes dp<N>; the model stores the number. Strip the prefix here rather
      // than ask the reader to.
      sql = filled => s"""
        |SELECT DISTINCT table_code, module, taxonomy_version, cell_code, row_label, column_label
        |FROM   '${partition("cells")(filled("framework"))}'
        |WHERE  datapoint = TRY_CAST(regexp_replace('${filled("datapoint")}', '^[dD][pP]?', '') AS BIGINT)
        |ORDER  BY module, taxonomy_version""".stripMargin.trim,
      reads = partition("cells"),
    ),
    Question(
      id = "property",
      ask = "What does a report's column header mean?",
      slots = List(Slot("code", "Header", "qCDF, qBBE, ei1452", "qCDF")),
      sql = filled => s"""
        |SELECT p.code, p.property, h.table_code, h.label AS used_as
        |FROM   '${whole("properties")("")}' p
        |LEFT JOIN '${whole("headers")("")}' h ON h.property_code = p.code AND h.is_key
        |WHERE  p.code = '${filled("code")}'
        |ORDER  BY h.table_code""".stripMargin.trim,
      reads = whole("properties"),
    ),
    Question(
      id = "deactivated",
      ask = "Which rules has the EBA switched off?",
      slots = List(module),
      // active is false for a rule that is published and not run. A description that
      // names one tells a reader to satisfy a check nobody runs.
      sql = filled => s"""
        |SELECT rule_code, severity, taxonomy_version, dpm_release, from_submission_date
        |FROM   '${whole("rules")("")}'
        |WHERE  module = '${filled("module")}' AND NOT active
        |ORDER  BY rule_code
        |LIMIT  $limit""".stripMargin.trim,
      reads = whole("rules"),
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
