import {templates} from "./src/data/known.js";

export default {
  title: "EBA DPM, by template",
  toc: true,
  search: true,
  // One source file for every template page. Adding a framework to the publish adds
  // pages without touching this, and a template the EBA withdraws stops having one.
  dynamicPaths: templates().map(({code}) => `/t/${code}`),
  pages: [{name: "What this is", path: "/"}],
  // The theme caps every table at the prose measure. On a page whose content is tables,
  // that is what clips the labels, so this is loaded after it. The script runs before the
  // first paint: a reader who chose light should not see dark first.
  head: `<link rel="stylesheet" href="/dpm.css">
    <script type="module" src="/appearance.js"></script>
    <script type="module" src="/keyboard.js"></script>`,
  // The bar every page gets, which is where the light/dark control puts itself.
  header: '<span class="site">EBA DPM</span>',
  footer: `Derived from the EBA DPM 2.0 database. Reproduction of EBA material is
    authorised provided the source is acknowledged
    (<a href="https://www.eba.europa.eu/legal-notice">eba.europa.eu/legal-notice</a>).
    Not published by the EBA and not endorsed by it.`,
};
