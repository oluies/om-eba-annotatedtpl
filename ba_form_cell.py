"""Enrich a datapoint lookup from the warehouse's own form metadata.

`FIDW_BI.dbo.BA_Form_Cell` describes every cell of every form the warehouse holds, keyed
by `DPM_Cell_Code` in the shape `{Y 01.01, r0010, c0010, s0010}`. That is the same
coordinate `05-datapoints.csv` carries, so the two join directly and each supplies what
the other lacks:

    BA_Form_Cell   Datapoint_sk, Data_Type, Form_BK, Taxonomy_Name, the open-axis names,
                   presentation format, and every form - not just PAY and DORA
    the pack       the dimension members, the glossary terms, and EBA's VariableVID

A column can mean different things in different forms and taxonomy versions, so a lookup
here is scoped: `Current_flg = 1` is the current definition, which is what a description
should be written against unless someone asks otherwise.

Optional. Without `BA_` settings the pack's own data answers on its own, which is what an
agent with no database access gets. Connecting costs a round trip per call, so it is for
enrichment rather than for the hot path.

The SQL here has not been run against the real table - there is no access from where this
was written. Treat the first run as a test, and check that the column names match.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Connection to the warehouse. Unset means the enrichment is simply off."""

    model_config = SettingsConfigDict(env_prefix="BA_", env_file=".env", extra="ignore")

    server: str | None = None
    database: str = "FIDW_BI"
    table: str = "dbo.BA_Form_Cell"
    # Kerberos: no username or password, the ticket from kinit carries the identity.
    trusted_connection: bool = True
    username: str | None = None
    password: str | None = None
    driver: str = "ODBC Driver 18 for SQL Server"
    encrypt: bool = True
    trust_server_certificate: bool = False


SETTINGS = Settings()


class FormCell(BaseModel):
    """One row of BA_Form_Cell, only the fields a description needs."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    dpm_cell_code: str
    datapoint_sk: int | None = None
    table_code: str | None = None
    table_label: str | None = None
    row_code: str | None = None
    row_label: str | None = None
    column_code: str | None = None
    column_label: str | None = None
    open_axis_label_1: str | None = None
    open_axis_cnt: int | None = None
    data_type: str | None = None
    form_bk: str | None = None
    form_name: str | None = None
    taxonomy_name: str | None = None


def enabled() -> bool:
    return SETTINGS.server is not None


def connection_string() -> str:
    """ODBC string. Kerberos is Trusted_Connection with no credentials in it."""
    parts = [
        f"DRIVER={{{SETTINGS.driver}}}",
        f"SERVER={SETTINGS.server}",
        f"DATABASE={SETTINGS.database}",
        f"Encrypt={'yes' if SETTINGS.encrypt else 'no'}",
        f"TrustServerCertificate={'yes' if SETTINGS.trust_server_certificate else 'no'}",
    ]
    if SETTINGS.trusted_connection:
        parts.append("Trusted_Connection=yes")
    elif SETTINGS.username and SETTINGS.password:
        parts += [f"UID={SETTINGS.username}", f"PWD={SETTINGS.password}"]
    return ";".join(parts) + ";"


# Current_flg picks the definition in force. A cell code can appear under several forms
# and taxonomy versions, and a description written against a superseded one is wrong in a
# way nothing in the catalogue would show.
QUERY = """
SELECT  DPM_Cell_Code, Datapoint_sk, Table_Code, Table_Label,
        Row_Code, Row_Label, Column_Code, Column_Label,
        Open_Axis_Label_1, Open_Axis_cnt, Data_Type,
        Form_BK, Form_Name, Taxonomy_Name
FROM    {table}
WHERE   DPM_Cell_Code = ?
  AND   Current_flg = 1
"""


def fetch(dpm_cell_code: str, form_bk: str | None = None) -> list[FormCell]:
    """Current definitions of one cell, optionally narrowed to one form.

    Returns every match rather than one: a cell code present under several forms is a
    fact about the warehouse, and picking silently would hide it.
    """
    if not enabled():
        return []

    import pyodbc  # noqa: PLC0415 - optional, and only where the connection is used

    sql = QUERY.format(table=SETTINGS.table)
    params: list[Any] = [dpm_cell_code]
    if form_bk:
        sql += "  AND   Form_BK = ?\n"
        params.append(form_bk)

    with pyodbc.connect(connection_string()) as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)
        names = [c[0].lower() for c in cursor.description]
        return [FormCell.model_validate(dict(zip(names, row, strict=True))) for row in cursor.fetchall()]


def describe(cells: list[FormCell]) -> dict[str, Any]:
    """Fold the matches into something a lookup can return alongside its own answer.

    Several forms for one cell is the interesting case, so it is reported rather than
    resolved: the caller has to know which form the table it is describing belongs to.
    """
    if not cells:
        return {}
    if len(cells) == 1:
        cell = cells[0]
        return {
            "datapoint_sk": cell.datapoint_sk,
            "data_type": cell.data_type,
            "form_bk": cell.form_bk,
            "form_name": cell.form_name,
            "taxonomy_name": cell.taxonomy_name,
            "open_axis": cell.open_axis_label_1,
        }
    return {
        "ambiguous": (
            f"{len(cells)} current forms define this cell: "
            + ", ".join(f"{c.form_bk} ({c.taxonomy_name})" for c in cells)
            + ". The column means different things in each, so establish which form the table "
            "belongs to from its Form_BK before describing it."
        ),
        "forms": [
            {"form_bk": c.form_bk, "taxonomy_name": c.taxonomy_name, "datapoint_sk": c.datapoint_sk} for c in cells
        ],
    }
