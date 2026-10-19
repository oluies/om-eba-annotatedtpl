package dpm

import org.scalajs.dom
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future
import scala.scalajs.js
import scala.scalajs.js.Thenable.Implicits.*

/** Where the parquet lives, as an absolute URL, for one DPM release.
  *
  * DuckDB-WASM resolves nothing relative: a browser has no working directory, so
  * `data/rules.parquet` is "No files found that match the pattern" and an absolute URL
  * is the only thing httpfs can fetch. Derived from the document's own base, so the page
  * works at a project path - `/om-eba-annotatedtpl/` on GitHub Pages - as well as at a
  * root.
  *
  * The release is part of the path because releases are separate answers to the same
  * question: FINREP9 is taxonomy 3.2.0 in DPM 4.0 and 3.3.0 from 4.2, and v0174_m is an
  * error in one and a warning in another. Switching release re-asks, it does not merge.
  */
object Data:
  // The fallback is for the tests, which build statements to read them and run in node
  // with no document. A relative path is useless to httpfs, which is the whole point of
  // this object - but in a browser there is always a document, so it is never the one in
  // a query that runs.
  private lazy val root: String =
    if js.typeOf(js.Dynamic.global.document) == "undefined" then "data/"
    else new dom.URL("data/", dom.document.baseURI).href

  /** Mutable, once, at startup: the page cannot know which releases were published until
    * it has read releases.json, and every query needs the answer. Set before the first
    * question can be asked.
    */
  private var current: String = ""

  def release: String = current

  def use(release: String): Unit = current = release

  def url(path: String): String = if current.isEmpty then root + path else s"$root$current/$path"

  /** The small, unpartitioned tables, read once per release into the engine.
    *
    * Measured rather than assumed: with `Cache-Control: max-age=600` - what GitHub Pages
    * sends - a second visit refetched every range, and within one session each question
    * re-read the files it names. These five are 450 kB together, so reading them once
    * costs less than asking three questions does without it. The partitioned tables stay
    * on HTTP: they are per framework and only the needed one is ever touched.
    */
  val cached: List[String] = List("modules", "rules", "sums", "headers", "properties")

  def preload(name: String): String = s"CREATE OR REPLACE TABLE $name AS SELECT * FROM '${url(s"$name.parquet")}'"

  /** What a release says about itself: which database it was built from, when, and
    * whether that release is a draft. One small request, and the page shows the answer
    * where the release is chosen - a reader picking 4.4 should not have to read a NOTICE
    * to learn that the EBA is still changing it.
    */
  final case class About(draft: Boolean, generated: String, source: String)

  def about(release: String): Future[About] =
    dom.fetch(s"$root$release/manifest.json")
      .toFuture
      .flatMap(response => if response.ok then response.text().toFuture else Future.successful("{}"))
      .map: text =>
        val parsed = js.JSON.parse(text)
        About(
          draft = parsed.draft.asInstanceOf[js.UndefOr[Boolean]].getOrElse(false),
          generated = Option(parsed.generated_at).map(_.toString).getOrElse(""),
          source = Option(parsed.source).map(_.toString).getOrElse(""),
        )
      .recover { case _ => About(draft = false, generated = "", source = "") }

  /** What was published, newest last. A site with one release and no index still works:
    * the list is empty and the paths have no release in them.
    */
  def published(): Future[List[String]] =
    dom.fetch(root + "releases.json")
      .toFuture
      .flatMap(response => if response.ok then response.text().toFuture else Future.successful("[]"))
      .map(text => js.JSON.parse(text).asInstanceOf[js.Array[String]].toList)
      .recover { case _ => Nil }
