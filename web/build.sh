#!/usr/bin/env bash
# Build the page into public/. No npm and no bundler: Scala.js emits ES modules and the
# browser resolves the CDN import itself.
set -euo pipefail
cd "$(dirname "$0")"
scala-cli --power package src/dpm -o public/main.js --js -f "$@"
ls -la public/*.js | awk '{printf "  %-28s %6.1f kB\n", $NF, $5/1000}'
