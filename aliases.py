"""Short names for the axes, beside the DPM's own rather than instead of them.

The DPM names an axis in full - `Type of authentication`, `Payment transactions
geographical breakdown` - and someone asking what a column holds does not want the
taxonomy's sentence, they want the word. The target wording for `Y0101_r0190_c0020` asked
for `Authentication`, `Remote/non-remote` and `Transaction type = Fraud`.

So this maps the long name to the short one, and every function here returns both. The
pack's rule is not to silently correct the source: a search against the framework's own
wording has to keep working, and an alias that replaced the DPM name would break it. Same
decision as `Card funtion in payment`, where the misspelling is kept beside the correction
rather than replaced by it.

An alias is a local choice and not the EBA's. Where the target kept the DPM's wording -
`Reasons for authentication via non-strong customer authentication`, in full - there is no
entry here, because an alias that says the same thing is one more name to keep in step.

Pure, and the inputs are the strings as `05-datapoints.csv` spells them.
"""

from collections.abc import Mapping
from dataclasses import dataclass

from display_names import members

# The five axes the target renamed. Keyed on the DPM's own name, which is what
# `row_dimensions` and `column_dimensions` carry, so a typo here is a silent no-op -
# test_every_aliased_axis_is_an_axis_of_the_framework is what stops that.
AXIS: Mapping[str, str] = {
    "Type of authentication": "Authentication",
    "Type of initiation of payments": "Electronic / Non-electronic",
    "Type of payment channel": "Remote/non-remote",
    "Type of payment transaction": "Transaction type",
    "Payment transactions geographical breakdown": "Geographical breakdown",
}

# Two axes the layout carries as columns of its own rather than as dimension pairs: what a
# datapoint measures, and which framework and version it belongs to. They are named here
# so a rendering can label them the way it labels the rest, and they have no DPM-side name
# to sit beside - `metric` and `template` are field names, not axis labels.
METRIC_AXIS = "Value type"
FRAMEWORK_AXIS = "Taxonomy"

# The one member the target shortened. Scoped to its axis on purpose: `Fraud` alone is a
# worse name on an axis whose contrast is something other than payment transactions, and
# member labels are not unique across domains to begin with.
VALUE: Mapping[tuple[str, str], str] = {
    ("Type of payment transaction", "Fraudulent payment transaction"): "Fraud",
}


@dataclass(frozen=True)
class Labelled:
    """One dimension assignment under both names.

    Both are kept because they answer different questions: `axis`/`value` is what a reader
    is shown, `axis_source`/`value_source` is what the framework calls it and therefore
    what a search against the EBA's own wording has to match.
    """

    axis: str
    value: str
    axis_source: str
    value_source: str

    @property
    def renamed(self) -> bool:
        """Whether this assignment reads differently from the framework's own wording."""
        return (self.axis, self.value) != (self.axis_source, self.value_source)


def axis(dimension: str) -> str:
    """The short name for an axis, or the DPM's own where there is no alias."""
    return AXIS.get(dimension, dimension)


def value(dimension: str, member: str) -> str:
    """The short name for a member on one axis, or the member as the DPM spells it."""
    return VALUE.get((dimension, member), member)


def labelled_pair(dimension: str, member: str) -> Labelled:
    return Labelled(axis=axis(dimension), value=value(dimension, member), axis_source=dimension, value_source=member)


def labelled(dimensions: str) -> tuple[Labelled, ...]:
    """Every assignment in a `row_dimensions` or `column_dimensions` cell, under both names.

    The cell is parsed by display_names.members rather than here: one parser for the one
    spelling the CSV uses, so the two cannot disagree about what a `;` separates.
    """
    return tuple(labelled_pair(dimension, member) for dimension, member in members(dimensions).items())


def taxonomy(framework: str, version: str) -> Labelled:
    """The framework and version as an assignment, so it renders beside the dimensions."""
    return Labelled(
        axis=FRAMEWORK_AXIS, value=f"{framework} {version}", axis_source=FRAMEWORK_AXIS, value_source=framework
    )


def value_type(metric: str) -> Labelled:
    """The metric as an assignment. Its axis has no DPM-side label to sit beside."""
    return Labelled(axis=METRIC_AXIS, value=metric, axis_source=METRIC_AXIS, value_source=metric)
