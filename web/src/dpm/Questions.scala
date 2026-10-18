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
/** One blank in a question.
  *
  * `options` is a query returning a single column of values to offer. It exists because
  * the model's own wording is unguessable: a dimension is "Counterparty sector" and its
  * member is "Credit institutions", trailing space and all, and a near miss matches
  * nothing rather than erroring. Offering what is there turns that from a trap into a
  * list. The field stays typeable - the values are many, and a code pasted from a report
  * should go straight in.
  */
final case class Slot(
    name: String,
    label: String,
    placeholder: String,
    example: String,
    options: Option[(String => String) => String] = None,
)

final case class Question(
    id: String,
    ask: String,
    slots: List[Slot],
    sql: (String => String) => String,
    reads: String => String,
    /** The words someone might use for this instead of the ones in `ask`. They exist for
      * the assistant: 0.5B and 1.5B both read "which rows add up to which" as the rules
      * question, because both are about rules and a template, and the id `sums` says
      * nothing on its own.
      */
    hints: String = "",
):
  /** Where the answer comes from, for the line under the results. */
  def source(filled: String => String): String = reads(filled("framework"))

object Questions:
  /** Parquet is split by framework, so a question names the partition it reads. One
    * question reads one partition: 176 kB for FINREP rather than 3.3 MB for all of them.
    */
  private def partition(table: String)(framework: String): String =
    Data.url(s"$table/framework=$framework/data_0.parquet")

  /** An unpartitioned table is read into the engine once per release, so a question names
    * the table rather than the file. `Data.cached` is what that covers.
    */
  private def whole(table: String)(framework: String): String =
    if Data.cached.contains(table) then table else Data.url(s"$table.parquet")

  /** The lists behind the slots. Every one of these reads a table that is already in the
    * engine - modules and headers are preloaded per release - so offering them costs
    * nothing over the wire except where the dimension and member lists read the same
    * partition the question itself will read.
    */
  private val frameworks = (_: String => String) => s"SELECT DISTINCT framework AS value FROM modules ORDER BY 1"

  private val templatesOf = (filled: String => String) =>
    s"""SELECT DISTINCT table_code AS value FROM headers
       |WHERE framework = '${filled("framework")}' ORDER BY 1""".stripMargin

  private val modulesOf = (filled: String => String) =>
    s"""SELECT DISTINCT module AS value FROM modules
       |WHERE framework = '${filled("framework")}' ORDER BY 1""".stripMargin

  private val dimensionsOf = (filled: String => String) =>
    s"""SELECT DISTINCT dimension AS value FROM '${partition("cell_members")(filled("framework"))}'
       |WHERE table_code = '${filled("table")}' ORDER BY 1""".stripMargin

  private val membersOf = (filled: String => String) =>
    s"""SELECT DISTINCT member AS value FROM '${partition("cell_members")(filled("framework"))}'
       |WHERE table_code = '${filled("table")}'
       |  AND trim(lower(dimension)) = trim(lower('${filled("dimension")}')) ORDER BY 1""".stripMargin

  private val framework =
    Slot("framework", "Framework", "FINREP, COREP, DORA…", "FINREP", Some(frameworks))
  private val template = Slot("table", "Template", "F_12.01.a", "F_12.01.a", Some(templatesOf))
  private val module = Slot("module", "Module", "FINREP9", "FINREP9", Some(modulesOf))

  /** Enough rows to read, few enough to render. The page says when it is reached, because
    * a table that stops at 200 without saying so reads as the whole answer.
    */
  val limit = 200

  val all: List[Question] = List(
    Question(
      id = "cells",
      ask = "Which cells does a template have?",
      hints = "the whole grid, every cell, all rows and columns of a template",
      slots = List(framework, template, Slot("module", "Module", "FINREP9", "FINREP9")),
      sql = filled => s"""
        |SELECT row_code, row_label, column_code, column_label, datapoint,
        |       '{' || table_code || ', r' || row_code || ', c' || column_code || '}' AS cell_code
        |FROM   '${partition("cells")(filled("framework"))}'
        |WHERE  table_code = '${filled("table")}' AND module = '${filled("module")}'
        |ORDER  BY row_code, column_code
        |LIMIT  $limit""".stripMargin.trim,
      reads = partition("cells"),
    ),
    Question(
      id = "dimensions",
      ask = "What does a template break down by?",
      hints = "which dimensions, what members exist, the wording of a dimension",
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
      hints = "one rule code, v0174_m, what does this outcome mean, severity of a code",
      slots = List(Slot("rule_code", "Rule code", "v0174_m", "v0174_m")),
      // The engine's occurrence number is stripped here as the lookup strips it: v3775_s_62
      // is the 62nd application of v3775_s, and the model has the rule, never the occurrence.
      sql = filled => s"""
        |SELECT module, taxonomy_version, dpm_release, severity, active,
        |       from_submission_date, expression
        |FROM   ${whole("rules")("")}
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
        |FROM   ${whole("headers")("")}
        |WHERE  table_code = '${filled("table")}' AND is_key
        |ORDER  BY code""".stripMargin.trim,
      reads = whole("headers"),
    ),
    Question(
      id = "aggregate",
      ask = "Which cells make up an aggregate? (one dimension, one member)",
      hints = "the codes behind a figure, cells where a dimension takes one member, "
        + "which cells are <member>, cells for counterparty sector = credit institutions",
      slots = List(
        framework,
        Slot("table", "Template", "F_04.04.1", "F_04.04.1", Some(templatesOf)),
        Slot("dimension", "Dimension", "Counterparty sector", "Counterparty sector", Some(dimensionsOf)),
        Slot("member", "Member", "Credit institutions", "Credit institutions", Some(membersOf)),
      ),
      // The wording has to come from the dimensions question: a near miss matches
      // nothing, and "Credit institutions " with a trailing space is a real item in the
      // model next to a clean one. trim on both sides is what the lookup does too.
      sql = filled => s"""
        |SELECT   m.table_code, c.datapoint, m.row_code, c.row_label, m.column_code, c.column_label
        |FROM     '${partition("cell_members")(filled("framework"))}' m
        |JOIN     '${partition("cells")(filled("framework"))}' c
        |         USING (table_code, row_code, column_code)
        |WHERE    m.table_code = '${filled("table")}'
        |     AND trim(lower(m.dimension)) = trim(lower('${filled("dimension")}'))
        |     AND trim(lower(m.member)) = trim(lower('${filled("member")}'))
        |GROUP BY ALL
        |ORDER BY m.row_code, m.column_code
        |LIMIT    $limit""".stripMargin.trim,
      reads = partition("cell_members"),
    ),
    Question(
      id = "sums",
      ask = "Which rows add up to which?",
      hints = "totals, subtotals, which rows sum to which, what adds up, arithmetic between rows",
      // 1780 edges for every framework and every module version: 17 kB, so no partition.
      // Offered from the sums table itself, so the list is the templates that have any -
      // which is a better answer than every template, and costs nothing: it is preloaded.
      slots = List(
        template.copy(options = Some(_ => "SELECT DISTINCT table_code AS value FROM sums ORDER BY 1")),
        module.copy(options =
          Some(filled => s"SELECT DISTINCT module AS value FROM sums WHERE table_code = '${filled("table")}' ORDER BY 1")
        ),
      ),
      sql = filled => s"""
        |SELECT total_row, addend_rows, columns, sheets, rule_code, severity
        |FROM   ${whole("sums")("")}
        |WHERE  table_code = '${filled("table")}' AND module = '${filled("module")}'
        |ORDER  BY total_row, rule_code""".stripMargin.trim,
      reads = whole("sums"),
    ),
    Question(
      id = "rules",
      ask = "Which validation rules reach a template?",
      hints = "every rule on a template, what is checked, the list of checks",
      slots = List(
        framework,
        Slot("table", "Template", "C_01.00", "C_01.00", Some(templatesOf)),
        Slot("module", "Module", "COREP_OF", "COREP_OF", Some(modulesOf)),
      ),
      // MATERIALIZED, not just a CTE: DuckDB inlines a plain one, so naming the
      // partition twice reads it twice - 1.9 MB for COREP where the file is 0.5.
      sql = filled => s"""
        |WITH cells AS MATERIALIZED (SELECT * FROM '${partition("rule_cells")(filled("framework"))}'),
        |     here AS (SELECT DISTINCT operation_vid FROM cells WHERE table_code = '${filled("table")}')
        |SELECT   r.rule_code, r.severity, r.active, r.taxonomy_version, r.dpm_release,
        |         list_sort(list(DISTINCT rc.row_code)) AS rows_here,
        |         count(DISTINCT rc.table_code) AS templates_named
        |FROM     ${whole("rules")("")} r
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
      hints = "dp152217, what is this id in a report, which cell is this datapoint",
      slots = List(framework, Slot("datapoint", "Datapoint", "152217 or dp152217", "152217")),
      // A report writes dp<N>; the model stores the number. Strip the prefix here rather
      // than ask the reader to.
      sql = filled => s"""
        |SELECT DISTINCT table_code, module, taxonomy_version,
        |       '{' || table_code || ', r' || row_code || ', c' || column_code || '}' AS cell_code,
        |       row_label, column_label
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
        |FROM   ${whole("properties")("")} p
        |LEFT JOIN ${whole("headers")("")} h ON h.property_code = p.code AND h.is_key
        |WHERE  p.code = '${filled("code")}'
        |ORDER  BY h.table_code""".stripMargin.trim,
      reads = whole("properties"),
    ),
    Question(
      id = "deactivated",
      ask = "Which rules has the EBA switched off?",
      hints = "deactivated rules, turned off, no longer run, inactive checks",
      slots = List(module),
      // active is false for a rule that is published and not run. A description that
      // names one tells a reader to satisfy a check nobody runs.
      sql = filled => s"""
        |SELECT rule_code, severity, taxonomy_version, dpm_release, from_submission_date
        |FROM   ${whole("rules")("")}
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
        |FROM   ${whole("modules")("")}
        |WHERE  framework = '${filled("framework")}'
        |ORDER  BY module, taxonomy_version""".stripMargin.trim,
      reads = whole("modules"),
    ),
  )

  def byId(id: String): Question = all.find(_.id == id).getOrElse(all.head)
