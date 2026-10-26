// Four accessibility defects in Observable Framework's own HTML, patched after the build.
//
// None of them is reachable from observablehq.config.js: `head` is inserted after the
// elements in question, and nothing in the config can set an attribute on <html> or
// remove a meta the renderer writes. The site is published to people who are required to
// meet WCAG 2.1 AA, so the choice is to patch the output or to not publish - and these
// are small enough to be worth sending upstream, which is a separate errand.
//
//   node accessible.mjs dist
//
// Framework 1.13.4. Each patch is written so that it does nothing once Framework fixes
// the defect itself.
import {readdirSync, readFileSync, statSync, writeFileSync} from "node:fs";
import {join} from "node:path";

/** Every patch, as one pure function, so the tests do not need a built site. */
export function fix(html) {
  return [
    // 3.1.1 Language of page. Framework writes a bare <html>, so a screen reader reads
    // English text with whatever voice the user's system defaults to - and "Kärnprimär-
    // kapitalrelation" in an English voice is not Swedish. The pages are English; the
    // Swedish and German columns carry their own lang below.
    (text) => (/<html[\s>]/.test(text) && !/<html[^>]*\slang=/.test(text) ? text.replace("<html", '<html lang="en"') : text),

    // 1.4.4 Resize text. `maximum-scale=1` stops a reader pinching to zoom on a phone,
    // which is a failure on its own and a bad one for a page of dense tables.
    (text) => text.replace('<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">', '<meta name="viewport" content="width=device-width, initial-scale=1">'),

    // 1.3.1 Info and relationships. The sidebar's close button is a <label> placed
    // directly inside an <ol>, where only <li> is allowed; assistive technology is
    // entitled to drop it or to miscount the list.
    (text) => text.replace(/<ol>(\s*)(<label id="observablehq-sidebar-close"[^>]*><\/label>)/, "$2$1<ol>"),

    // 4.1.2 Name, role, value. The search field has a placeholder and no accessible name.
    // A placeholder is not a name: it disappears on the first keystroke.
    (text) => text.replace(/<input type="search" placeholder="Search">/, '<input type="search" placeholder="Search" aria-label="Search this site">'),
  ].reduce((text, patch) => patch(text), html);
}

function* pages(root) {
  for (const entry of readdirSync(root)) {
    const path = join(root, entry);
    if (statSync(path).isDirectory()) yield* pages(path);
    else if (entry.endsWith(".html")) yield path;
  }
}

if (process.argv[1]?.endsWith("accessible.mjs")) {
  const root = process.argv[2] ?? "dist";
  let changed = 0;
  for (const path of pages(root)) {
    const before = readFileSync(path, "utf-8");
    const after = fix(before);
    if (after !== before) {
      writeFileSync(path, after);
      changed++;
    }
  }
  console.log(`${changed} pages patched for accessibility`);
}
