"""Where a row sits in the layout, as a label.

The EBA nests its rows: `Trusted beneficiary (Art.13 RTS)` means nothing on its own, and
what it means is the path down to it - credit transfers, initiated electronically, via a
remote channel, authenticated without SCA, broken down by reason. That path is what a
reader needs and what the row label alone does not carry.

**It is a label and not a derivation.** A level can contribute two dimension members, one,
or none, and a deeper level can supersede a shallower one on the same axis: in Y_04.01,
`0200 Issuance of a payment order by a fraudster` and `0210 Lost or stolen card` are parent
and child in the layout but both Event Type, so only the leaf survives. Across the PAY
templates 90 of 216 rows have a member count that differs from their non-abstract ancestor
count, by anything from -1 to +2. Rows 0200-0270 of Y_04.01 sit under a heading that
narrows to a remote payment channel and carry no channel member at all, in the EBA's own
model - tests/test_extraction_matches_the_dpm.py holds that down.

So: render this, and read the dimensions from `row_dimensions`. Never the other way round.

Pure. The input is the headers of one table version as HEADERS_SQL returns them.
"""

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

ROWS = "Y"  # the model's direction code for rows; X is columns and Z is sheets


@dataclass(frozen=True)
class Step:
    code: str
    label: str
    abstract: bool


class ChainError(Exception):
    """A parent that is not there, or a cycle. Both mean the headers are not a tree."""


def _by_code(headers: Iterable[Mapping[str, object]], direction: str) -> dict[str, Mapping[str, object]]:
    return {str(h["code"]): h for h in headers if h.get("direction") == direction}


def ancestry(headers: Iterable[Mapping[str, object]], code: str, direction: str = ROWS) -> tuple[Step, ...]:
    """Root first, the row itself last.

    Raises rather than returning a short chain: a missing parent or a cycle means the
    headers are not the tree this assumes, and a breadcrumb built from half of one reads
    like a complete answer. Measured over releases 4.2.1, 4.3 and 4.4 there are none -
    roughly 20000 headers each, every walk terminating at a root.
    """
    index = _by_code(headers, direction)
    steps: list[Step] = []
    seen: set[str] = set()
    at: str | None = code
    while at is not None:
        if at in seen:
            raise ChainError(f"{code} is in a cycle, at {at}")
        seen.add(at)
        header = index.get(at)
        if header is None:
            raise ChainError(f"{code} has no header {at} to climb to")
        steps.append(Step(code=at, label=str(header["label"]), abstract=bool(header["is_abstract"])))
        parent = header.get("parent_code")
        at = None if parent is None else str(parent)
    return tuple(reversed(steps))


def breadcrumb(steps: Sequence[Step], column_label: str | None = None) -> str:
    """The path as one line, with the column read after the root.

    The column goes second because that is how the coordinate reads: what is counted, then
    of what, then the narrowing. It is a reading order and not a hierarchy - the column is
    a different axis from the rows, and nothing here should be taken to say otherwise.

    Labels are kept exactly as the layout spells them, capitals and all. `Of which
    Initiated electronically` has that capital I in the source, and correcting it here
    would break a search against the framework's own wording.
    """
    if not steps:
        return ""
    labels = [steps[0].label, *([column_label] if column_label else []), *(s.label for s in steps[1:])]
    return ", ".join(labels)
