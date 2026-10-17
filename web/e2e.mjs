// Drive the page the way a reader would, in a real browser.
//
//   ./build.sh --js-mode release          # writes public/main.js
//   uv run ../source/gen_wasm_data.py     # writes public/data
//   python3 server.py public 8097 &       # a static server that speaks byte ranges
//   npm install playwright && npx playwright install chromium
//   node e2e.mjs
//
// Not part of CI: it wants a browser download and the DPM. CI compiles the page instead,
// which catches the breakage that matters without either.
import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage();
let bytes = 0;
page.on("response", (r) => { if (r.url().includes("127.0.0.1")) bytes += Number(r.headers()["content-length"] ?? 0); });
page.on("console", (m) => { if (m.type() === "error") console.log("console error:", m.text()); });
page.on("pageerror", (e) => console.log("PAGE ERROR:", e.message));

await page.goto("http://127.0.0.1:8097/index.html", { waitUntil: "load" });
await page.waitForSelector(".controls button");
console.log("shell rendered:", await page.textContent("h1"));
console.log("questions:", (await page.$$eval("select option", (os) => os.map((o) => o.textContent))).length);

const ask = async (label, fills) => {
  await page.selectOption("select", { label });
  for (const [n, v] of Object.entries(fills)) {
    const input = page.locator(`.controls label:has-text("${n}") input`);
    await input.fill(v);
  }
  const before = bytes;
  await page.click(".controls button");
  // The status also carries "loading the engine", so waiting on it alone races the
  // first question against an 8 MB download.
  await page.waitForFunction(
    () => document.querySelector(".answer table tbody tr") !== null
      || /Error|error/.test(document.querySelector(".status")?.textContent ?? ""),
    { timeout: 180000 },
  );
  const problem = (await page.textContent(".status")).trim();
  if (problem) { console.log(`\n### ${label} — FAILED: ${problem}`); return; }
  const meta = await page.textContent(".meta");
  const head = await page.$$eval(".answer thead th", (t) => t.map((x) => x.textContent));
  const first = await page.$$eval(".answer tbody tr:nth-child(-n+2) td", (t) => t.map((x) => x.textContent));
  console.log(`\n### ${label}`);
  console.log("   ", meta, `· ${Math.round((bytes - before) / 1024)} kB over the wire`);
  console.log("    columns:", head.join(", "));
  console.log("    first rows:", first.slice(0, 12).join(" | "));
};

await ask("Which cells does a template have?", { Framework: "FINREP", Template: "F_12.01.a", Module: "FINREP9" });
await ask("What does a template break down by?", { Framework: "FINREP", Template: "F_04.04.1" });
await ask("What does a validation code mean?", { "Rule code": "v3775_s_62" });
await ask("What are a template's key dimensions?", { Framework: "AMLA", Template: "V_04.01" });
await ask("Which module versions is a framework reported under?", { Framework: "FINREP" });

const sql = await page.textContent(".answer details pre");
console.log("\nSQL shown with the answer:\n" + sql.split("\n").slice(0, 4).map((l) => "    " + l).join("\n"));
console.log(`\ntotal pulled: ${Math.round(bytes / 1024)} kB`);
await browser.close();
