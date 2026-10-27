// 2.1.1 Keyboard, and 1.3.1 on the way.
//
// Inputs.table renders its rows into a scrolling box. Until this site turned the row
// selection off, every row held a checkbox, so the box always had something focusable in
// it and a keyboard user could reach it by tabbing. With the checkboxes gone - they were
// 133 unlabelled form controls per page, and nothing read the selection - the box became
// scrollable content that a keyboard cannot reach at all.
//
// So each one is made focusable, and named after the heading it sits under, which is what
// a screen reader announces when the focus lands there: "Every cell, region".
const named = (box) => {
  // From the box itself, not from its parent: a display() can put the heading and the
  // table in one cell, and both reworded-rows tables do. Starting a level up skipped
  // their <h3> and announced them as the section above - "The same rows in Swedish and
  // German" for a table of what the regulation reworded.
  let before = box;
  while (before) {
    for (let node = before.previousElementSibling; node; node = node.previousElementSibling) {
      if (/^H[1-6]$/.test(node.tagName)) return node.textContent.trim();
    }
    before = before.parentElement;
  }
  return "Table";
};

const reachable = (root) => {
  for (const box of root.querySelectorAll?.('form[class*="-table"]') ?? []) {
    if (box.hasAttribute("tabindex")) continue;
    box.setAttribute("tabindex", "0");
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", named(box));
  }
};

function watch() {
  const main = document.querySelector("#observablehq-main");
  if (!main) return;
  reachable(main);
  // Every table is rendered by a cell, and a cell re-runs whenever the release changes -
  // so this cannot be done once at load.
  new MutationObserver(() => reachable(main)).observe(main, {childList: true, subtree: true});
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", watch);
else watch();
