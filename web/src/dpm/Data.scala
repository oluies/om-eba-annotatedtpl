package dpm

import org.scalajs.dom

/** Where the parquet lives, as an absolute URL.
  *
  * DuckDB-WASM resolves nothing relative: a browser has no working directory, so
  * `data/rules.parquet` is "No files found that match the pattern" and an absolute URL
  * is the only thing httpfs can fetch. Derived from the document's own base, so the page
  * works at a project path - `/om-eba-annotatedtpl/` on GitHub Pages - as well as at a
  * root.
  */
object Data:
  lazy val base: String = new dom.URL("data/", dom.document.baseURI).href

  def url(path: String): String = base + path
