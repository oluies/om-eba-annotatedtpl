#!/usr/bin/env bash
# Render one page per template as GitHub-flavoured markdown for OpenMetadata, and as
# HTML to read it locally before uploading.
#
# The HTML is no longer published: obs/ builds the pages a reader sees, because a
# document rendered at build cannot offer a release selector and this one has to.
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
# RELEASE and RELEASES put the pages in a directory of their own and give every page
# links to the same template under the other releases. A page that says 4.3 is then 4.3
# all the way down - its cells, its rules, its severities and its history - rather than
# offering a choice it cannot honour, since Quarto renders once.
#
#   RELEASE=4.3 RELEASES="4.2.1 4.3 4.4" ./render.sh --framework COREP
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

if [ "${1:-}" = "--framework" ]; then
  shift
  [ "$#" -gt 0 ] || { echo "--framework needs at least one name, e.g. FINREP COREP" >&2; exit 2; }
  # All of them in one call, and one render over the lot: each framework's pages are
  # written before anything is rendered, so a second framework cannot delete the first
  # one's - which is what looping this script per framework would do.
  here python pages.py --framework "$@" --release "${RELEASE:-}" --releases ${RELEASES:-} > /dev/null
  echo "pages for $*:"
elif [ "$#" -gt 0 ]; then
  here python pages.py "$@" --release "${RELEASE:-}" --releases ${RELEASES:-} > /dev/null
else
  # One template that has moved datapoints, one that has reworded a row: between them
  # they exercise both halves of the history section.
  here python pages.py F_18.00.a K_47.00.a --release "${RELEASE:-}" --releases ${RELEASES:-} > /dev/null
fi

# A directory per release when one is named, so three renders do not overwrite each other.
site="_site${RELEASE:+/$RELEASE}"
markdown="_md${RELEASE:+/$RELEASE}"
mkdir -p "$markdown"

here quarto render --to html --output-dir "$site"
# --no-clean, or the second project render empties _site/ and the HTML from the first one
# goes with it. Quarto clears the output directory per render, not per format.
here quarto render --to gfm --no-clean --output-dir "$site"

# The markdown lands beside the HTML; the catalogue's half is moved out so that what is
# published and what is uploaded are two directories rather than one mixed one.
for page in "$site"/*.md; do
  [ -e "$page" ] || continue
  mv "$page" "$markdown/$(basename "$page")"
done

echo
echo "$(find "$site" -name '*.html' | wc -l | tr -d ' ') pages in $site/, $(find "$markdown" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ') in $markdown/ for the catalogue"
