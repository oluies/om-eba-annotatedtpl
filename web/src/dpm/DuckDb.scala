package dpm

import scala.scalajs.js
import scala.scalajs.js.annotation.JSImport

/** The slice of DuckDB-WASM this page uses: six calls.
  *
  * Imported straight from the CDN as an ES module, so there is no bundler and no npm in
  * this build - Scala.js emits ES modules and the browser resolves the URL itself.
  * `+esm` is jsDelivr's bundled build, which matters because the package's own entry
  * point imports apache-arrow by bare specifier and a browser cannot resolve that.
  *
  * No facade for duckdb-wasm exists for Scala.js; this is it, and it is deliberately the
  * smallest one that works rather than a translation of the whole API.
  */
@js.native
trait Bundle extends js.Object:
  val mainModule: String = js.native
  val mainWorker: String = js.native
  val pthreadWorker: js.UndefOr[String] = js.native

@js.native
trait ArrowRow extends js.Object:
  def toJSON(): js.Object = js.native

@js.native
trait ArrowTable extends js.Object:
  val numRows: Int = js.native
  def toArray(): js.Array[ArrowRow] = js.native

@js.native
trait Connection extends js.Object:
  def query(sql: String): js.Promise[ArrowTable] = js.native
  def close(): js.Promise[Unit] = js.native

@js.native
@JSImport("https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm", JSImport.Namespace)
object DuckDbModule extends js.Object:
  def getJsDelivrBundles(): js.Object = js.native
  def selectBundle(bundles: js.Object): js.Promise[Bundle] = js.native
  // The class is declared without the trait: a native class that implements a native
  // trait has to repeat the members as overrides, which buys nothing here.
  @js.native
  class AsyncDuckDB(logger: js.Object, worker: js.Object) extends js.Object:
    def instantiate(mainModule: String, pthreadWorker: js.UndefOr[String]): js.Promise[Unit] = js.native
    def connect(): js.Promise[Connection] = js.native
  @js.native
  class VoidLogger() extends js.Object
