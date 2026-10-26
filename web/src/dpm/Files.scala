package dpm

import org.scalajs.dom
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future
import scala.scalajs.js
import scala.scalajs.js.Thenable.Implicits.*
import scala.scalajs.js.typedarray.Uint8Array

/** Every file a statement names, fetched once and handed to DuckDB as bytes.
  *
  * httpfs reads a parquet over HTTP ranges, and GitHub Pages serves these gzipped: the
  * content-length it then reports is the compressed length, while a byte range is served
  * from the uncompressed file. DuckDB reads the footer where it was told the end is, finds
  * no magic bytes there, and the question fails in front of the reader with a NetworkError.
  * Which of the two variants the CDN happens to hold decides whether that happens - the
  * same page answered a FINREP question an hour before it refused to. `fetch` decompresses,
  * so the bytes are the file.
  *
  * The statement shown under an answer keeps the URL. That is the address the file really
  * has, and it is what a reader would run against it; only the copy DuckDB executes is
  * rewritten.
  */
object Files:
  private var database: Option[DuckDbModule.AsyncDuckDB] = None

  /** Keyed by URL, and the future rather than the name: two slots asking at once before
    * the first fetch has finished would otherwise fetch the same file twice.
    */
  private var registered: Map[String, Future[String]] = Map.empty

  def use(db: DuckDbModule.AsyncDuckDB): Unit = database = Some(db)

  /** DuckDB picks its reader from the extension, so the name keeps it. */
  def named(url: String): String =
    url.replaceAll("^https?://", "").replaceAll("[^\\w.]+", "_")

  private def register(url: String): Future[String] =
    registered.getOrElse(
      url, {
        val pending = database match
          case None => Future.failed(IllegalStateException(s"the engine is not open, so $url cannot be read"))
          case Some(db) =>
            for
              response <- dom.fetch(url).toFuture
              _ = if !response.ok then throw RuntimeException(s"${response.status} ${response.statusText} for $url")
              buffer <- response.arrayBuffer().toFuture
              local = named(url)
              _ <- db.registerFileBuffer(local, Uint8Array(buffer)).toFuture
            yield local
        registered += url -> pending
        pending
      },
    )

  private val urls = """'(https?://[^']+)'""".r

  /** Which files a statement names. */
  def reads(sql: String): List[String] = urls.findAllMatchIn(sql).map(_.group(1)).toList.distinct

  /** The statement with each URL replaced by the name its bytes are registered under.
    * Pure, so the rewrite is tested without an engine or a network.
    */
  def rewritten(sql: String, names: Map[String, String]): String =
    names.foldLeft(sql)((statement, pair) => statement.replace(s"'${pair._1}'", s"'${pair._2}'"))

  /** The statement as DuckDB will run it: each URL replaced by the name the bytes are
    * registered under. A statement naming no file is returned unchanged and costs nothing.
    */
  def localise(sql: String): Future[String] =
    val files = reads(sql)
    if files.isEmpty then Future.successful(sql)
    else Future.traverse(files)(url => register(url).map(url -> _)).map(pairs => rewritten(sql, pairs.toMap))
