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
    # No dot in the NAME: OpenMetadata quotes FQN parts containing one, so a glossary
    # called "PAY 4.2" is addressed as "PAY 4.2".Term and the CSV parent column stops
    # matching. The readable form is the displayName.
    glossary: str = "PAY_4_2"
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


def split_title(markdown: str, fallback: str) -> tuple[str, str]:
    """Separate the leading level-1 heading from the body.

    OpenMetadata renders the page's displayName as the heading above the content, so a
    body that starts with the same `# ...` shows the title twice. Take it for the
    displayName and drop it from the body; a file with no leading H1 is left alone.
    """
    lines = markdown.splitlines()
    head = next((i for i, line in enumerate(lines) if line.strip()), None)
    if head is None or not lines[head].startswith("# "):
        return fallback, markdown

    rest = lines[head + 1 :]
    while rest and not rest[0].strip():
        rest = rest[1:]
    return lines[head][2:].strip(), "\n".join(rest) + "\n"


def leaf(path: Path, name: str | None = None) -> Page:
    title, body = split_title(path.read_text(encoding="utf-8"), path.stem)
    return Page(name=name or path.stem, display_name=title, body=body)


def section(name: str, display_name: str, body: str, children: tuple[Page, ...]) -> Page:
    return Page(name=name, display_name=display_name, body=body, children=children)


def build_tree(pack: Path) -> Page:
    """Mirror the pack layout as a page hierarchy.

    An `EBA` root sits above the framework so COREP, FINREP or a later PAY release can
    be loaded alongside this one instead of each landing at the top level.
    """
    tables = tuple(leaf(p) for p in sorted((pack / "04-tables").glob("*.md")))
    glossary = tuple(leaf(p) for p in sorted((pack / "03-glossary").glob("*.md")))

    pay42 = section(
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

    return section(
        name="EBA",
        display_name="EBA reporting frameworks",
        body=(
            "Reporting frameworks published by the European Banking Authority, as\n"
            "annotated table layouts normalised for use in this catalogue.\n\n"
            "Content reproduced under the EBA legal notice, which authorises\n"
            "reproduction provided the source is acknowledged. Not affiliated with or\n"
            "endorsed by the EBA.\n"
        ),
        children=(pay42,),
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


PAGES_PATH = "/v1/contextCenter/pages"


def preflight(client: httpx.Client, *, check_pages: bool) -> str:
    """Fail with a diagnosis rather than an opaque 4xx from the first write.

    Three things go wrong here and they look alike in a stack trace: a base URL without
    `/api` (the ingress answers the path but rejects the method, which surfaces as 405),
    a server too old to have the Knowledge Page API, and a token that is not accepted.
    """
    base = str(client.base_url).rstrip("/")
    if not base.endswith("/api"):
        raise SystemExit(
            f"OM_HOST is {base!r}, but OpenMetadata serves its API under /api.\n"
            f"This should almost certainly be {base}/api - without it the ingress answers\n"
            "the request and rejects the method, which looks like a 405 on a valid path."
        )

    version = client.get("/v1/system/version")
    if version.status_code == 401:
        raise SystemExit("Authentication failed against /v1/system/version. Check OM_JWT_TOKEN.")
    if version.status_code != 200:
        raise SystemExit(
            f"GET {base}/v1/system/version returned {version.status_code}, so this is probably\n"
            "not an OpenMetadata API root. Check OM_HOST."
        )
    server = version.json().get("version", "unknown")

    if not check_pages:
        return server

    probe = client.get(PAGES_PATH, params={"limit": 1})
    if probe.status_code == 404:
        raise SystemExit(
            f"Server {server} has no {PAGES_PATH}. The Knowledge Page API is not in this\n"
            "release, so the markdown cannot be imported as pages. Re-run with\n"
            "--glossary-only to load the controlled vocabulary on its own."
        )
    if probe.status_code not in (200, 403):
        probe.raise_for_status()

    return server


def upsert_page(client: httpx.Client, page: Page, parent_id: str | None) -> str:
    response = client.put(PAGES_PATH, json=page_payload(page, parent_id))
    response.raise_for_status()
    return response.json()["id"]


def upsert_tree(client: httpx.Client, page: Page, parent_id: str | None = None, depth: int = 0) -> list[str]:
    """Parents before children, because a child needs its parent's id.

    Returns every id written, which is what the reindex call needs.
    """
    page_id = upsert_page(client, page, parent_id)
    print(f"{'  ' * depth}✓ {page.display_name}  ({page_id})")
    return [page_id, *(i for child in page.children for i in upsert_tree(client, child, page_id, depth + 1))]


def reindex(client: httpx.Client, page_ids: list[str]) -> None:
    """Push the written pages into the search index.

    The UI lists pages through `/search/hierarchy`, which reads the search index, while
    the write goes to the database. Indexing is asynchronous, so freshly written pages
    can be absent from every list view while `/hierarchy` shows them. Reindexing the
    specific ids closes that gap without a full cluster reindex.
    """
    response = client.post(
        "/v1/search/reindexEntities",
        params={"timeoutMinutes": 5},
        json=[{"id": page_id, "type": "page"} for page_id in page_ids],
    )
    if response.status_code == 403:
        print("  Reindex needs an admin or bot token; skipped. The pages exist either way.")
        return
    if response.status_code == 404:
        print("  No /v1/search/reindexEntities on this server; skipped.")
        return
    response.raise_for_status()
    print(f"  Reindex requested for {len(page_ids)} pages.")


def verify_listing(client: httpx.Client) -> None:
    """Report the database count against the search-index count.

    A gap between the two is the reason pages exist but do not show up in a list.
    """

    def count(path: str) -> int | str:
        response = client.get(path, params={"limit": 100})
        if response.status_code != 200:
            return f"HTTP {response.status_code}"
        payload = response.json()
        return len(payload.get("data", payload if isinstance(payload, list) else []))

    db = count(f"{PAGES_PATH}/hierarchy")
    search = count(f"{PAGES_PATH}/search/hierarchy")
    print(f"\n  database  /hierarchy:        {db}")
    print(f"  search    /search/hierarchy: {search}")
    if isinstance(db, int) and isinstance(search, int) and db > search:
        print(
            f"\n  {db - search} root page(s) are in the database but not in the search index,\n"
            "  which is why they do not appear in the UI list. Re-run without --dry-run to\n"
            "  reindex, or wait for the indexing job to catch up."
        )


def import_glossary(client: httpx.Client, glossary: str, csv_text: str, *, dry_run: bool) -> ImportResult:
    """PUT the term CSV. The endpoint consumes text/plain and returns a CsvImportResult."""
    response = client.put(
        f"/v1/glossaries/name/{glossary}/import",
        params={"dryRun": str(dry_run).lower()},
        content=csv_text,
        headers={"Content-Type": "text/plain"},
    )
    if response.status_code >= 400:
        # OpenMetadata puts the reason in the body. Raising bare for_status() throws it
        # away and leaves a status code that could mean several different things.
        raise SystemExit(
            f"\n  {response.request.method} {response.request.url}\n"
            f"  -> {response.status_code}\n"
            f"  {response.text[:1000]}"
        )
    return ImportResult.model_validate(response.json())


GLOSSARY_DESCRIPTION = (
    "Controlled vocabulary of the EBA PAY 4.2 (FRPPAY 4.2) framework for payment and fraud "
    "reporting under PSD2: the domains and their members, the dimensions that draw on them, "
    "and the metrics. Transcribed from the annotated table layout of 2026-01-06. Reproduced "
    "under the EBA legal notice, which authorises reproduction provided the source is "
    "acknowledged."
)


def ensure_glossary(client: httpx.Client, glossary: str) -> None:
    """Create the glossary if it is not there.

    The CSV import populates an existing glossary; it does not create one. Without this
    the import returns a bare 404 that reads like a wrong URL.
    """
    existing = client.get(f"/v1/glossaries/name/{glossary}")
    if existing.status_code == 200:
        return
    if existing.status_code != 404:
        existing.raise_for_status()

    print(f"  Glossary {glossary!r} does not exist; creating it.")
    created = client.put(
        "/v1/glossaries",
        json={
            "name": glossary,
            "displayName": "PAY 4.2 (FRPPAY 4.2)",
            "description": GLOSSARY_DESCRIPTION,
        },
    )
    if created.status_code == 403:
        raise SystemExit(
            f"  Not permitted to create glossary {glossary!r}. Create it in the UI, or use a\n"
            "  token with rights to create glossaries, then re-run."
        )
    if created.status_code >= 400:
        raise SystemExit(f"  Creating glossary {glossary!r} failed: {created.status_code}\n  {created.text[:1000]}")

    body = created.json()
    print(f"    created name={body.get('name')!r} fqn={body.get('fullyQualifiedName')!r} id={body.get('id')}")

    # Read it back rather than trusting the status code. A 2xx create followed by a 404
    # from the import means the two are not addressing the same thing, and the name the
    # server actually stored is what tells us why.
    recheck = client.get(f"/v1/glossaries/name/{glossary}")
    if recheck.status_code != 200:
        raise SystemExit(
            f"  Created glossary {glossary!r}, but GET /v1/glossaries/name/{glossary} still\n"
            f"  returns {recheck.status_code}. The server stored it as name="
            f"{body.get('name')!r}, fqn={body.get('fullyQualifiedName')!r}.\n"
            f"  Set OM_GLOSSARY to that name and re-run.\n  {recheck.text[:500]}"
        )


def run_glossary_import(client: httpx.Client, glossary: str, csv_path: Path, *, commit: bool) -> None:
    """Always dry run first; only write when that came back clean and --commit was given."""
    csv_text = csv_path.read_text(encoding="utf-8")

    print(f"\nGlossary dry run ({glossary}):")
    ensure_glossary(client, glossary)
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
    parser.add_argument(
        "--verify",
        action="store_true",
        help="compare the database listing against the search-index listing and stop. "
        "Use when pages exist but do not show up in the UI.",
    )
    parser.add_argument("--no-reindex", action="store_true", help="do not reindex after writing pages")
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
        base_url=settings.host.rstrip("/"),
        headers={"Authorization": f"Bearer {settings.jwt_token}"},
        verify=settings.ca_bundle or True,
        timeout=60.0,
    ) as client:
        server = preflight(client, check_pages=not args.glossary_only)
        print(f"OpenMetadata {server} at {str(client.base_url).rstrip('/')}")

        if args.verify:
            verify_listing(client)
            return

        if not args.glossary_only:
            page_ids = upsert_tree(client, tree)
            print(f"\n{len(page_ids)} pages written.")
            if not args.no_reindex:
                reindex(client, page_ids)

        if not args.pages_only:
            run_glossary_import(
                client,
                settings.glossary,
                PACK / "06-openmetadata-glossary.csv",
                commit=args.commit,
            )


if __name__ == "__main__":
    main()
