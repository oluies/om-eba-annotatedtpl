#!/usr/bin/env bash
# Build the template pages.
#
#   OBS_FRAMEWORKS="COREP FINREP" DPM2_DB=../source/dpm2/dpm2_4_4.duckdb ./build.sh
#
# Two steps and not one, because observablehq.config.js has to know which templates exist
# before the build starts - dynamicPaths is read when the config is loaded, and a data
# loader runs during the build, which is too late. So the catalogue is written first.
set -euo pipefail
cd "$(dirname "$0")"

./src/data/catalogue.json.sh > src/data/catalogue.json
echo "$(node -e 'console.log(JSON.parse(require("fs").readFileSync("src/data/catalogue.json")).length)') templates"

# Which releases the selector offers. The publish writes this; locally it is whatever has
# been generated, and one release is a selector with one entry rather than a broken page.
if [ -f ../web/public/data/releases.json ]; then
  cp ../web/public/data/releases.json src/data/releases.json
fi

npx --no-install observable build
