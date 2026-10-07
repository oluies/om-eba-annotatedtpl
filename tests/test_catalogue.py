"""Writing to OpenMetadata, against a fake server that behaves like the real one.

Two of these cover failures that happened in production and were reported as bugs:

  * the server HTML-escapes on write, so a byte-for-byte read-back called a successful
    write "the server kept the old description";
  * an application bot is denied EditDisplayName by policy, and sending the label with
    the description meant a denied label failed the whole write.

The fake therefore escapes on write and can be told to deny a label, because a mock that
is kinder than the server tests nothing.
"""

import json

import httpx
import pytest

from describe_table import denied_display_name, landed, put_column, unescaped

SCHEMA = "SQLSASTest.FIDW_BI.dbo"
TABLE = f"{SCHEMA}.Y_01_01"
DENIAL = {
    "code": 403,
    "message": (
        "Principal: CatalogPrincipal{name='mcpapplicationbot'} operation EditDisplayName "
        "denied by role ApplicationBotImpersonationRole, policy ApplicationBotPolicy"
    ),
}


def sanitise(text):
    """What the server's OWASP policy does on every write."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("+", "&#43;")


class Fake:
    """A column store that escapes on write, and optionally refuses display names."""

    def __init__(self, columns, deny_label=False):
        self.columns = {
            f"{TABLE}.{name}": {"name": name, "fullyQualifiedName": f"{TABLE}.{name}", **fields}
            for name, fields in columns.items()
        }
        self.deny_label = deny_label
        self.bodies = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        fqn = request.url.path.split("/v1/columns/name/")[1]
        if request.method == "GET":
            found = self.columns.get(fqn)
            return httpx.Response(200, json=found) if found else httpx.Response(404, json={})
        body = json.loads(request.content)
        self.bodies.append(body)
        if self.deny_label and "displayName" in body:
            return httpx.Response(403, json=DENIAL)
        self.columns[fqn] |= {
            key: sanitise(value) for key, value in body.items() if key in ("description", "displayName")
        }
        return httpx.Response(200, json=self.columns[fqn])


def http_to(fake):
    return httpx.Client(base_url="http://om.test/api", transport=httpx.MockTransport(fake))


# --- the sanitisation false negative ---------------------------------------------------


@pytest.mark.parametrize(
    ("wanted", "stored"),
    [
        ("a and b", "a and b"),
        ("a & b", "a &amp; b"),
        ("<TEMPLATE>", "&lt;TEMPLATE&gt;"),
        ("1 + 1", "1 &#43; 1"),
        ("  padded  ", "padded"),
    ],
)
def test_landed_allows_for_the_servers_escaping(wanted, stored):
    assert landed(wanted, stored)


@pytest.mark.parametrize("stored", [None, "", "something else"])
def test_landed_still_detects_a_write_that_did_not_happen(stored):
    assert not landed("what we sent", stored)


def test_unescaped_undoes_the_escapes_in_sequence():
    """`&amp;` is undone first, so a double-escaped plus collapses all the way to `+`.

    That is deliberate and safe here, not an accident: the comparison only ever asks
    whether what we sent survived, and nothing this pack generates contains an ampersand
    or a plus sign in the first place - the build guard refuses one. A stored value is
    double-escaped only if an already-escaped value was sent, which never happens.
    """
    assert unescaped("1 &amp;#43; 1") == "1 + 1"


# --- the denied display name ------------------------------------------------------------


def test_denied_display_name_recognises_the_policy_refusal():
    assert denied_display_name(httpx.Response(403, json=DENIAL))


@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(200, json={}),
        httpx.Response(403, json={"code": 403, "message": "operation EditDescription denied"}),
        httpx.Response(404, json={}),
    ],
)
def test_denied_display_name_does_not_fire_on_anything_else(response):
    assert not denied_display_name(response)


def test_put_column_retries_without_the_label_so_the_description_lands():
    fake = Fake({"Y0101_r0010_c0010": {"description": ""}}, deny_label=True)
    with http_to(fake) as http:
        response, dropped = put_column(
            http, f"{TABLE}.Y0101_r0010_c0010", {"description": "what it measures", "displayName": "A label"}
        )
    assert response.status_code == 200
    assert dropped is True
    assert fake.columns[f"{TABLE}.Y0101_r0010_c0010"]["description"] == "what it measures"
    assert not fake.columns[f"{TABLE}.Y0101_r0010_c0010"].get("displayName")
    assert "displayName" not in fake.bodies[-1], "the retry must not resend the label"


def test_put_column_sends_one_request_when_the_label_is_allowed():
    fake = Fake({"Y0101_r0010_c0010": {"description": ""}})
    with http_to(fake) as http:
        response, dropped = put_column(http, f"{TABLE}.Y0101_r0010_c0010", {"description": "d", "displayName": "L"})
    assert (response.status_code, dropped) == (200, False)
    assert len(fake.bodies) == 1


def test_put_column_does_not_retry_a_body_that_is_only_a_label():
    """Nothing would be left to send, so the refusal has to surface as a refusal."""
    fake = Fake({"Y0101_r0010_c0010": {"description": "kept"}}, deny_label=True)
    with http_to(fake) as http:
        response, dropped = put_column(http, f"{TABLE}.Y0101_r0010_c0010", {"displayName": "L"})
    assert response.status_code == 403
    assert dropped is False


# --- the agent's write tool -------------------------------------------------------------


def write(monkeypatch, fake, **kwargs):
    import describe_table

    monkeypatch.setenv("OM_HOST", "http://om.test/api")
    monkeypatch.setenv("OM_JWT_TOKEN", "test")
    monkeypatch.setattr(describe_table, "client", lambda settings: http_to(fake))
    return describe_table.write_column_metadata(TABLE, "Y0101_r0010_c0010", **kwargs)


def test_write_column_metadata_writes_into_an_empty_description(monkeypatch):
    fake = Fake({"Y0101_r0010_c0010": {"description": ""}})
    answer = write(monkeypatch, fake, description="Number of credit transfers")
    assert answer["written"] is True


def test_write_column_metadata_refuses_to_replace_prose_nobody_read(monkeypatch):
    fake = Fake({"Y0101_r0010_c0010": {"description": "written by a human"}})
    answer = write(monkeypatch, fake, description="mine")
    assert answer["written"] is False
    assert "nothing says you read it" in answer["reason"]
    assert fake.bodies == [], "it must not have written anything"


def test_write_column_metadata_replaces_it_when_the_caller_quotes_it_back(monkeypatch):
    fake = Fake({"Y0101_r0010_c0010": {"description": "written by a human"}})
    answer = write(monkeypatch, fake, description="mine", expect_current="written by a human")
    assert answer["written"] is True


def test_write_column_metadata_refuses_a_stale_quote(monkeypatch):
    fake = Fake({"Y0101_r0010_c0010": {"description": "changed since you read it"}})
    answer = write(monkeypatch, fake, description="mine", expect_current="what I read")
    assert answer["written"] is False
    assert "someone changed it" in answer["reason"]


def test_write_column_metadata_is_a_no_op_when_it_already_says_that(monkeypatch):
    fake = Fake({"Y0101_r0010_c0010": {"description": "already this"}})
    answer = write(monkeypatch, fake, description="already this")
    assert answer["unchanged"] is True
    assert fake.bodies == []


def test_write_column_metadata_reports_a_column_that_does_not_exist(monkeypatch):
    answer = write(monkeypatch, Fake({}), description="d")
    assert answer == {"column_fqn": f"{TABLE}.Y0101_r0010_c0010", "written": False, "reason": "no such column"}


def test_write_column_metadata_needs_something_to_write(monkeypatch):
    answer = write(monkeypatch, Fake({"Y0101_r0010_c0010": {}}), description="   ")
    assert answer["reason"] == "nothing to set"
