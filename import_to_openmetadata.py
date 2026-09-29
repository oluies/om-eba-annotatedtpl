"""Import the PAY 4.2 documentation pack into OpenMetadata.

The markdown files become Knowledge Pages under `/v1/contextCenter/pages`; the glossary
CSV goes to `/v1/glossaries/name/{glossary}/import`. There is no bulk upload of files and
no place to put a zip archive: `docStore/document.json` is a generic JSON payload store
that the UI uses for persona layouts, not a document library.

Endpoints and field names were read from the OpenMetadata schema rather than assumed:

    PUT /v1/contextCenter/pages                       createOrUpdate, idempotent on name
    PUT /v1/glossaries/name/{name}/import?dryRun=     Content-Type: text/plain, body = CSV

`createPage.json` requires `name`, `pageType` and `page`; the markdown body goes in
`description`, which the schema types as markdown.

Usage:

    export OM_HOST=http://localhost:8585/api
    export OM_JWT_TOKEN=...
    uv run --with httpx --with pydantic-settings python import_to_openmetadata.py --dry-run
    uv run --with httpx --with pydantic-settings python import_to_openmetadata.py
"""

import argparse
import csv
import io
from collections.abc import Iterator
from pathlib import Path
from typing import Literal

import httpx
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from pydantic_settings import BaseSettings, SettingsConfigDict

PACK = Path(__file__).parent


class Settings(BaseSettings):
    """Connection details. Read once, at the edge."""

    model_config = SettingsConfigDict(env_prefix="OM_", env_file=".env", extra="ignore")

    host: str = "http://localhost:8585/api"
    jwt_token: str
    glossary: str = "PAY 4.2"
    ca_bundle: str | None = None


class Page(BaseModel):
    """One Knowledge Page and its children. Frozen: built once, then walked."""

    model_config = ConfigDict(frozen=True)

    name: str
    display_name: str
    body: str
    children: tuple["Page", ...] = ()


ImportStatus = Literal["success", "failure", "aborted", "partialSuccess", "running"]


class ImportResult(BaseModel):
    """Response of a glossary CSV import.

    Fields mirror `type/csvImportResult.json`; the status values come from
    `basic.json#/definitions/status`. Validated here so a shape change in a future
    OpenMetadata version fails loudly at the boundary rather than being read as a
    successful import.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, frozen=True, extra="ignore")

    dry_run: bool | None = None
    status: ImportStatus | None = None
    abort_reason: str | None = None
    number_of_rows_processed: int = 0
    number_of_rows_passed: int = 0
    number_of_rows_failed: int = 0
    import_results_csv: str | None = None

    @property
    def clean(self) -> bool:
        """Safe to commit: everything passed and nothing was rejected."""
        return self.status == "success" and self.number_of_rows_failed == 0

    def summary(self) -> str:
        head = (
            f"status={self.status} processed={self.number_of_rows_processed} "
            f"passed={self.number_of_rows_passed} failed={self.number_of_rows_failed}"
        )
        return head if not self.abort_reason else f"{head}\n  aborted: {self.abort_reason}"

    def failures(self, limit: int = 20) -> list[str]:
        """Rows the server rejected, read back out of the result CSV it returns."""
        if not self.import_results_csv:
            return []
        rows = list(csv.reader(io.StringIO(self.import_results_csv)))
        return [
            " | ".join(cell for cell in row if cell)[:200]
            for row in rows[1:]
            if row and row[0].strip().lower() not in {"success", ""}
        ][:limit]


# --------------------------------------------------------------------------------------
# Building the tree - pure apart from the file reads
# --------------------------------------------------------------------------------------


def title_of(markdown: str, fallback: str) -> str:
    """The first level-1 heading, else the fallback."""
    return next((line[2:].strip() for line in markdown.splitlines() if line.startswith("# ")), fallback)


def leaf(path: Path, name: str | None = None) -> Page:
    body = path.read_text(encoding="utf-8")
    return Page(name=name or path.stem, display_name=title_of(body, path.stem), body=body)


def section(name: str, display_name: str, body: str, children: tuple[Page, ...]) -> Page:
    return Page(name=name, display_name=display_name, body=body, children=children)


def build_tree(pack: Path) -> Page:
    """Mirror the pack layout as a page hierarchy."""
    tables = tuple(leaf(p) for p in sorted((pack / "04-tables").glob("*.md")))
    glossary = tuple(leaf(p) for p in sorted((pack / "03-glossary").glob("*.md")))

    return section(
        name="PAY 4.2",
        display_name="PAY 4.2 (FRPPAY 4.2)",
        body=(pack / "README.md").read_text(encoding="utf-8"),
        children=(
            leaf(pack / "01-framework.md", name="Framework"),
            leaf(pack / "02-agent-instructions.md", name="Agent instructions"),
            section(
                "Glossary",
                "Glossary",
                "Controlled vocabulary of PAY 4.2: domains and their members, the\n"
                "dimensions that draw on them, and the metrics.\n",
                glossary,
            ),
            section(
                "Templates",
                "Templates",
                f"One page per PAY 4.2 template ({len(tables)} in total). Each lists the\n"
                "variants, columns, rows and datapoint ids.\n",
                tables,
            ),
        ),
    )


def walk(page: Page, depth: int = 0) -> Iterator[tuple[Page, int]]:
    yield page, depth
    for child in page.children:
        yield from walk(child, depth + 1)


# --------------------------------------------------------------------------------------
# Talking to OpenMetadata - all the I/O lives below this line
# --------------------------------------------------------------------------------------


def page_payload(page: Page, parent_id: str | None) -> dict[str, object]:
    """`page` is required by createPage.json; article.json's own fields are all optional."""
    body: dict[str, object] = {
        "name": page.name,
        "displayName": page.display_name,
        "description": page.body,
        "pageType": "Article",
        "page": {},
    }
    return body if parent_id is None else body | {"parent": {"id": parent_id, "type": "page"}}


def upsert_page(client: httpx.Client, page: Page, parent_id: str | None) -> str:
    response = client.put("/v1/contextCenter/pages", json=page_payload(page, parent_id))
    response.raise_for_status()
    return response.json()["id"]


def upsert_tree(client: httpx.Client, page: Page, parent_id: str | None = None, depth: int = 0) -> int:
    """Parents before children, because a child needs its parent's id."""
    page_id = upsert_page(client, page, parent_id)
    print(f"{'  ' * depth}✓ {page.display_name}  ({page_id})")
    return 1 + sum(upsert_tree(client, child, page_id, depth + 1) for child in page.children)


def import_glossary(client: httpx.Client, glossary: str, csv_text: str, *, dry_run: bool) -> ImportResult:
    """PUT the term CSV. The endpoint consumes text/plain and returns a CsvImportResult."""
    response = client.put(
        f"/v1/glossaries/name/{glossary}/import",
        params={"dryRun": str(dry_run).lower()},
        content=csv_text,
        headers={"Content-Type": "text/plain"},
    )
    response.raise_for_status()
    return ImportResult.model_validate(response.json())


def run_glossary_import(client: httpx.Client, glossary: str, csv_path: Path, *, commit: bool) -> None:
    """Always dry run first; only write when that came back clean and --commit was given."""
    csv_text = csv_path.read_text(encoding="utf-8")

    print(f"\nGlossary dry run ({glossary}):")
    dry = import_glossary(client, glossary, csv_text, dry_run=True)
    print(f"  {dry.summary()}")
    for line in dry.failures():
        print(f"  ✗ {line}")

    match (commit, dry.clean):
        case (False, _):
            print("\n  Nothing written. Re-run with --commit once the dry run looks right.")
        case (True, False):
            raise SystemExit(
                f"\n  Refusing to commit: the dry run reported status={dry.status} with "
                f"{dry.number_of_rows_failed} rejected row(s). Fix the CSV and try again."
            )
        case (True, True):
            print("\n  Dry run clean, committing:")
            result = import_glossary(client, glossary, csv_text, dry_run=False)
            print(f"  {result.summary()}")
            for line in result.failures():
                print(f"  ✗ {line}")
            if not result.clean:
                raise SystemExit("\n  The commit did not come back clean. Check the glossary in the UI.")
            print(f"  {result.number_of_rows_passed} terms written to glossary {glossary!r}.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="print the page tree, contact nothing")
    parser.add_argument(
        "--commit",
        action="store_true",
        help="write the glossary terms for real. Without it the glossary is only dry run. "
        "The dry run happens either way, and a commit is refused if it is not clean.",
    )
    parser.add_argument("--pages-only", action="store_true", help="skip the glossary")
    parser.add_argument("--glossary-only", action="store_true", help="skip the Knowledge Pages")
    args = parser.parse_args()

    tree = build_tree(PACK)

    if args.dry_run:
        for page, depth in walk(tree):
            print(f"{'  ' * depth}{page.name:<24} {page.display_name}  ({len(page.body)} bytes)")
        print(f"\n{sum(1 for _ in walk(tree))} pages would be written to /v1/contextCenter/pages")
        print("Glossary CSV would be dry-run against /v1/glossaries/name/.../import?dryRun=true")
        return

    settings = Settings()  # type: ignore[call-arg]  # jwt_token comes from the environment
    with httpx.Client(
        base_url=settings.host,
        headers={"Authorization": f"Bearer {settings.jwt_token}"},
        verify=settings.ca_bundle or True,
        timeout=60.0,
    ) as client:
        if not args.glossary_only:
            total = upsert_tree(client, tree)
            print(f"\n{total} pages written.")

        if not args.pages_only:
            run_glossary_import(
                client,
                settings.glossary,
                PACK / "06-openmetadata-glossary.csv",
                commit=args.commit,
            )


if __name__ == "__main__":
    main()
