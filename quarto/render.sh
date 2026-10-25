#!/usr/bin/env bash
# Render one page per template, twice: HTML for the site, GFM for the catalogue.
#
# The same source both times, which is the thing this spike exists to find out - whether
# one source can serve a public site and an OpenMetadata article without a second
# pipeline. The answer is in _md/, which is markdown a catalogue takes as it is.
#
#   ./render.sh                        # the two templates the spike demonstrates
#   ./render.sh F_01.01 C_01.00        # any templates you name
#   ./render.sh --framework DORA       # a whole framework, with an index page
#   DPM2_DB=../source/dpm2/dpm2_4_3.duckdb ./render.sh     # under another release
#
# Both renders are of the whole project rather than file by file. Quarto starts one
# kernel per render, so a project of 154 pages pays for one startup and not 154 - the
# difference between about a minute and about ten.
set -euo pipefail
cd "$(dirname "$0")"

here() { uv run --group docs --project .. "$@"; }

# Last run's pages, which may name templates or a framework this one does not. Everything
# but the two sources: index.qmd is written by hand, _body.qmd is what the stubs include.
# Matching [A-Z]_* instead left DORA.qmd behind, and a FINREP render published a DORA page.
find . -maxdepth 1 -name '*.qmd' ! -name 'index.qmd' ! -name '_body.qmd' -delete
mkdir -p _md

if [ "${1:-}" = "--framework" ]; then
  shift
  [ "$#" -gt 0 ] || { echo "--framework needs at least one name, e.g. FINREP COREP" >&2; exit 2; }
  # All of them in one call, and one render over the lot: each framework's pages are
  # written before anything is rendered, so a second framework cannot delete the first
  # one's - which is what looping this script per framework would do.
  here python pages.py --framework "$@" > /dev/null
  echo "pages for $*:"
elif [ "$#" -gt 0 ]; then
  here python pages.py "$@" > /dev/null
else
  # One template that has moved datapoints, one that has reworded a row: between them
  # they exercise both halves of the history section.
  here python pages.py F_18.00.a K_47.00.a > /dev/null
fi

here quarto render --to html
# --no-clean, or the second project render empties _site/ and the HTML from the first one
# goes with it. Quarto clears the output directory per render, not per format.
here quarto render --to gfm --no-clean

# The markdown lands beside the HTML; the catalogue's half is moved out so that what is
# published and what is uploaded are two directories rather than one mixed one.
for page in _site/*.md; do
  [ -e "$page" ] || continue
  mv "$page" "_md/$(basename "$page")"
done

echo
echo "$(find _site -name '*.html' | wc -l | tr -d ' ') pages in _site/, $(find _md -name '*.md' | wc -l | tr -d ' ') in _md/ for the catalogue"
