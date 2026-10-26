// Light, dark, or whatever the machine says — remembered between pages and visits.
//
// The theme switches on `prefers-color-scheme` alone, so a reader on a dark machine had no
// way to read this on white, which is what someone circulating it in an office needs. The
// stored choice is applied in <head>, before the first paint, or the page flashes the
// other palette first.
const KEY = "dpm-appearance";
const CHOICES = [["auto", "Auto"], ["light", "Light"], ["dark", "Dark"]];

function remembered() {
  try {
    const found = localStorage.getItem(KEY);
    return CHOICES.some(([value]) => value === found) ? found : "auto";
  } catch (problem) {
    // Private browsing, or storage switched off. Following the machine is the default
    // anyway, so there is nothing to recover from.
    return "auto";
  }
}

function apply(choice) {
  if (choice === "auto") document.documentElement.removeAttribute("data-theme");
  else document.documentElement.setAttribute("data-theme", choice);
  try {
    localStorage.setItem(KEY, choice);
  } catch (problem) {
    // The page still looks right for this visit; only the memory is lost.
  }
}

function control() {
  const held = document.createElement("div");
  held.className = "appearance";
  held.append(Object.assign(document.createElement("span"), {textContent: "Appearance"}));
  const buttons = CHOICES.map(([value, label]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.setAttribute("aria-pressed", String(value === remembered()));
    button.addEventListener("click", () => {
      apply(value);
      for (const other of buttons) other.setAttribute("aria-pressed", String(other === button));
    });
    return button;
  });
  held.append(...buttons);
  return held;
}

// Applied while <head> is parsing, before the first paint, so a reader who chose light
// never sees dark first. The control itself needs the header, which comes later.
apply(remembered());

const place = () => document.querySelector("#observablehq-header")?.append(control());
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", place);
else place();
