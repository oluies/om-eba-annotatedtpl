package dpm

import com.raquo.laminar.api.L.*
import org.scalajs.dom
import scala.scalajs.js
import scala.util.Try

/** Light, dark, or whatever the machine says.
  *
  * The page is drawn in the system's own Canvas and CanvasText, so a reader on a dark
  * machine had no way to read it on white - which is what someone circulating it in an
  * office needs. Forcing `color-scheme` on the root element is the whole mechanism; the
  * CSS for it is three lines.
  *
  * The key is the one the template pages use, and both are on the same origin, so a
  * choice made on either carries to the other.
  */
object Appearance:
  private val key = "dpm-appearance"
  private val choices = List("auto" -> "Auto", "light" -> "Light", "dark" -> "Dark")

  /** Private browsing, or storage switched off: following the machine is the default
    * anyway, so there is nothing to recover from.
    */
  private def remembered: String =
    Try(Option(dom.window.localStorage.getItem(key))).toOption.flatten.filter(found => choices.exists(_._1 == found)).getOrElse("auto")

  private def apply(choice: String): Unit =
    if choice == "auto" then dom.document.documentElement.removeAttribute("data-theme")
    else dom.document.documentElement.setAttribute("data-theme", choice)
    Try(dom.window.localStorage.setItem(key, choice)).toOption.getOrElse(())

  def control: HtmlElement =
    val chosen = Var(remembered)
    apply(chosen.now())
    div(
      cls := "appearance",
      span("Appearance"),
      choices.map: (value, text) =>
        button(
          tpe := "button",
          text,
          // aria-pressed rather than a class: the state has to reach a screen reader, and
          // these three are a set of toggles, not links.
          aria.pressed <-- chosen.signal.map(chosen => (chosen == value).toString),
          onClick --> { _ =>
            apply(value)
            chosen.set(value)
          },
        ),
    )
