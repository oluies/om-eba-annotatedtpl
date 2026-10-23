#!/usr/bin/env bash
# Render one page per template, twice: HTML for the site, GFM for the catalogue.
#
# The same source both times. That is what this spike exists to find out - whether one
# source can serve a public site and an OpenMetadata article without a second pipeline -
# and the answer is in _md/, which is markdown a catalogue takes as it is.
#
#   ./render.sh                       # the two templates the spike demonstrates
#   ./render.sh F_01.01 C_01.00       # any templates you name
#   DPM2_DB=../source/dpm2/dpm2_4_3.duckdb ./render.sh    # under another release
set -euo pipefail
cd "$(dirname "$0")"

if [ "$#" -gt 0 ]; then
  templates=("$@")
else
  # One template that has moved datapoints, one that has reworded a row: between them
  # they exercise both halves of the history section.
  templates=(F_18.00.a K_47.00.a)
fi

mkdir -p _md

# uv runs it so the kernel comes from the docs group rather than from whatever python is
# on PATH; --project .. because this directory is not the project root.
here() { uv run --group docs --project .. "$@"; }

here python pages.py "${templates[@]}" > /dev/null

# The whole project at once for HTML: the website's search index and navigation are
# built from the set of pages, so rendering them one at a time leaves search stale.
here quarto render --to html

for code in "${templates[@]}"; do
  here quarto render "$code.qmd" --to gfm --no-clean
  mv "_site/$code.md" "_md/$code.md"
  echo "  $code"
done

echo
echo "HTML in _site/, markdown for the catalogue in _md/:"
ls _md
