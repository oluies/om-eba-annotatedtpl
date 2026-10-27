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
  // that is what clips the labels, so the stylesheet is loaded after it.
  //
  // The stored appearance is applied by a classic inline script rather than by the module
  // below, because a module script is deferred: it runs after the document is parsed, and
  // nothing makes the browser wait for it before painting. A reader on a dark machine who
  // chose light would see dark first, on every page, because Framework navigates between
  // pages with a full load. The key is repeated here rather than imported for the same
  // reason - an import is a module - and web/public/index.html does the same for the
  // query page.
  head: `<link rel="stylesheet" href="/dpm.css">
    <script>
      try {
        var chosen = localStorage.getItem("dpm-appearance");
        if (chosen === "light" || chosen === "dark") document.documentElement.setAttribute("data-theme", chosen);
      } catch (problem) {
        // Storage switched off. Following the machine is the default anyway.
      }
    </script>
    <script type="module" src="/appearance.js"></script>
    <script type="module" src="/keyboard.js"></script>`,
  // The bar every page gets, which is where the light/dark control puts itself.
  header: '<span class="site">EBA DPM</span>',
  footer: `Derived from the EBA DPM 2.0 database. Reproduction of EBA material is
    authorised provided the source is acknowledged
    (<a href="https://www.eba.europa.eu/legal-notice">eba.europa.eu/legal-notice</a>).
    Not published by the EBA and not endorsed by it.`,
};
