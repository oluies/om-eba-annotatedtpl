// Which templates have a page, for observablehq.config.js. The loader beside this writes
// catalogue.json at build; before the first build there is none, and an empty list is a
// site with no template pages rather than a build that fails.
//
// Named apart from the data it reads on purpose: this directory once held
// templates.js, templates.json.sh and templates.json at the same time, and a loader is
// found by stripping the extension - so the three collided and every cell on every page
// stopped running, with no error anywhere.
import {existsSync, readFileSync} from "node:fs";

export function templates() {
  const here = new URL("./catalogue.json", import.meta.url);
  return existsSync(here) ? JSON.parse(readFileSync(here, "utf-8")) : [];
}
