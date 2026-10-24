"""Score a local translation model against the Official Journal's own Swedish.

The point of having `source/its_labels.csv` is not only the labels. It is that we now hold
2 379 three-way translations that a Member State's lawyers signed off, which makes every
claim about a translation model testable instead of arguable. This runs a model over a
sample and says how often it produced the published wording.

    ollama serve &
    uv run source/score_translation.py                      # the model you have
    uv run source/score_translation.py --model qwen3:32b --sample 50
    uv run source/score_translation.py --language de

What it measured when it was written, against gemma4 on this machine, 25 labels:

    plain                         exact  1/25
    with a 40-term glossary       exact  6/25

Six times better and still wrong nineteen times out of twenty-five. The failures are
terminology, not fluency: `Debt securities` came back as `Skuldsäkerheter`, which is
fluent Swedish and is not the term - the Journal says `Räntebärande värdepapper`. A better
model writes better Swedish; it does not know which Swedish the regulation uses. One run
produced `Säkerhet på nivå 1 utom säkerställda obligation` for `Level 1 collateral which
is extremely high quality covered bonds` - `utom` means "except", so the label was
negated. That is the failure mode that matters, because it reads perfectly.

So: a model is for our own prose, and for a first draft of the vocabulary the Journal does
not carry - dimension members, metrics, module names - which a human then approves. It is
not for the labels. The labels are published.
"""

from __future__ import annotations

import argparse
import csv
import random
import re
import time
from pathlib import Path
from typing import Any, NamedTuple

import httpx

HERE = Path(__file__).resolve().parent
LABELS = HERE / "its_labels.csv"
OLLAMA = "http://127.0.0.1:11434/api/generate"

PLAIN = (
    "Translate this EBA supervisory reporting label from English to {language}. "
    "Answer with the translation only, no explanation.\n\n{text}"
)

WITH_GLOSSARY = (
    "Translate this EBA supervisory reporting label from English to {language}, using the "
    "official terminology below wherever it applies. Answer with the translation only.\n\n"
    "Official terms:\n{glossary}\n\nTranslate: {text}"
)

LANGUAGES = {"sv": "Swedish", "de": "German"}


class Score(NamedTuple):
    """How a model did on one condition."""

    condition: str
    exact: int
    normalised: int
    asked: int
    seconds: float
    misses: list[tuple[str, str, str]]


def normal(text: str) -> str:
    """For comparing two translations of the same label.

    Case, numbering and punctuation are not what is being judged - whether the model chose
    the published term is. Letters outside a-z are kept, or every Swedish answer would
    collapse to the same string.
    """
    without_number = re.sub(r"^[\d.\s]*", "", text.strip())
    return re.sub(r"[^\w]+", " ", without_number.lower(), flags=re.UNICODE).strip()


def answer(text: str) -> str:
    """The translation out of a reply that may carry reasoning before it.

    A reasoning model opens with a <think> block, and with a long prompt that block can
    run to the token limit so the answer never arrives. Unterminated blocks are stripped
    too, which is what turns that case into a visible miss rather than a crash.
    """
    stripped = re.sub(r"<think>.*?(</think>|$)", " ", text, flags=re.S)
    lines = [line.strip().strip('"') for line in stripped.splitlines() if line.strip()]
    return lines[-1] if lines else ""


def ask(model: str, prompt: str, client: httpx.Client) -> str:
    """One translation, at temperature zero."""
    response = client.post(
        OLLAMA,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            # Room for a reasoning block and the answer after it. 80 was enough for the
            # short prompt and not for the glossary one, which scored that condition zero
            # and looked like the glossary having made the model worse.
            "options": {"temperature": 0, "num_predict": 600},
        },
        timeout=300.0,
    )
    response.raise_for_status()
    return answer(response.json()["response"])


def score(model: str, sample: list[dict[str, str]], prompt: str, language: str, condition: str, **rest: Any) -> Score:
    """Run one condition over the sample."""
    exact = normalised = 0
    misses: list[tuple[str, str, str]] = []
    started = time.time()
    with httpx.Client() as client:
        for row in sample:
            got = ask(model, prompt.format(language=LANGUAGES[language], text=row["en"], **rest), client)
            if got == row[language]:
                exact += 1
            elif normal(got) == normal(row[language]):
                normalised += 1
            else:
                misses.append((row["en"], row[language], got))
    return Score(condition, exact, exact + normalised, len(sample), time.time() - started, misses)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", default="gemma4:latest", help="an ollama model you have pulled")
    parser.add_argument("--language", default="sv", choices=sorted(LANGUAGES), help="the target language")
    parser.add_argument("--sample", type=int, default=25, help="how many labels to translate per condition")
    parser.add_argument("--glossary", type=int, default=40, help="how many official terms to show, 0 for none")
    parser.add_argument("--labels", type=Path, default=LABELS, help="the three-way labels to score against")
    parser.add_argument("--misses", type=int, default=5, help="how many wrong answers to print")
    parser.add_argument("--seed", type=int, default=7, help="which sample, so two models get the same one")
    args = parser.parse_args()

    if not args.labels.exists():
        raise SystemExit(f"{args.labels} is not there; source/fetch_its_labels.py --out writes it.")
    with args.labels.open(encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if 12 < len(row["en"]) < 90]
    if len(rows) < args.sample + args.glossary:
        raise SystemExit(f"{args.labels} has {len(rows)} usable rows, fewer than the sample and glossary want.")

    # The glossary is drawn from rows the model is not asked to translate, or it would be
    # scored on terms it was handed the answers to.
    chooser = random.Random(args.seed)
    sample = chooser.sample(rows, args.sample)
    rest = [row for row in rows if row not in sample]
    glossary = chooser.sample(rest, args.glossary) if args.glossary else []
    terms = "\n".join(f"{row['en']} = {row[args.language]}" for row in glossary)

    conditions = [("plain", PLAIN, {})]
    if glossary:
        conditions.append(("with glossary", WITH_GLOSSARY, {"glossary": terms}))

    print(f"{args.model}, English to {LANGUAGES[args.language]}, {args.sample} labels from {args.labels.name}\n")
    for condition, prompt, rest_args in conditions:
        found = score(args.model, sample, prompt, args.language, condition, **rest_args)
        print(
            f"{found.condition:<14} exact {found.exact:>3}/{found.asked}"
            f"   same after normalising {found.normalised:>3}/{found.asked}"
            f"   ({found.seconds:.0f}s, {found.seconds / max(found.asked, 1):.1f}s a label)"
        )
        for english, published, got in found.misses[: args.misses]:
            print(f"    EN       {english[:72]}")
            print(f"    Journal  {published[:72]}")
            print(f"    model    {got[:72] or '(no answer)'}")
        print()


if __name__ == "__main__":
    main()
