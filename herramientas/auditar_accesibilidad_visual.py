"""Comprueba tamaño de controles, foco visible y contraste de tokens visuales."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGETS = (
    ("assets/experiencia.css", ".boton-menu"),
    ("assets/estilo.css", ".selector-tema select"),
    ("assets/experiencia.css", ".filtros-galeria-visual button"),
    ("assets/experiencia.css", "#controles-comparador select,#controles-mapa select"),
    ("assets/estilo.css", ".ampliar-grafico"),
    ("assets/estilo.css", ".controles-ampliacion button"),
    ("assets/estilo.css", ".boton,.filtros button"),
)


def declarations(source: str, selector: str) -> list[str]:
    pattern = re.escape(selector) + r"\s*\{([^{}]*)\}"
    return re.findall(pattern, source)


def min_heights(source: str, selector: str) -> list[float]:
    values = []
    for block in declarations(source, selector):
        values.extend(float(value) for value in re.findall(r"min-height\s*:\s*([\d.]+)px", block))
    return values


def color_tokens(source: str, selector: str) -> dict[str, str]:
    blocks = declarations(source, selector)
    if not blocks:
        raise ValueError(f"Falta el bloque CSS {selector}.")
    return dict(re.findall(r"(--[\w-]+)\s*:\s*(#[\da-fA-F]{3,8})", blocks[0]))


def luminance(value: str) -> float:
    digits = value.lstrip("#")
    if len(digits) == 3:
        digits = "".join(character * 2 for character in digits)
    if len(digits) != 6:
        raise ValueError(f"Formato de color no admitido: {value}")
    channels = [int(digits[index:index + 2], 16) / 255 for index in (0, 2, 4)]
    linear = [channel / 12.92 if channel <= .04045 else ((channel + .055) / 1.055) ** 2.4
              for channel in channels]
    return .2126 * linear[0] + .7152 * linear[1] + .0722 * linear[2]


def contrast(first: str, second: str) -> float:
    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + .05) / (dark + .05)


class ControlNameParser(HTMLParser):
    """Subset statico de nombres HTML nativos; limites en ACCESIBILIDAD.md."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.controls, self.labels, self.label_stack = [], [], []
        self.buttons, self.id_stack, self.id_text = [], [], {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "label":
            label = {"for": attrs.get("for", ""), "text": ""}
            self.labels.append(label)
            self.label_stack.append(label)
        if attrs.get("id"):
            self.id_stack.append({"id": attrs["id"], "tag": tag, "text": ""})
        if tag in {"button", "input", "select", "textarea"}:
            control = {"tag": tag, "attrs": attrs, "text": "",
                       "wrapped": [label for label in self.label_stack if not label["for"]]}
            self.controls.append(control)
            if tag == "button":
                self.buttons.append(control)
        if tag == "img" and attrs.get("alt") and self.buttons:
            self.buttons[-1]["text"] += " " + attrs["alt"]

    def handle_endtag(self, tag):
        if tag == "label" and self.label_stack:
            self.label_stack.pop()
        if tag == "button" and self.buttons:
            self.buttons.pop()
        for index in range(len(self.id_stack) - 1, -1, -1):
            if self.id_stack[index]["tag"] == tag:
                item = self.id_stack.pop(index)
                self.id_text[item["id"]] = item["text"].strip()
                break

    def handle_data(self, data):
        for label in self.label_stack:
            label["text"] += data
        for button in self.buttons:
            button["text"] += data
        for item in self.id_stack:
            item["text"] += data

    def unnamed_controls(self):
        issues = []
        for control in self.controls:
            tag, attrs = control["tag"], control["attrs"]
            if tag == "input" and attrs.get("type", "text").lower() == "hidden":
                continue
            labels = [label["text"].strip() for label in self.labels
                      if attrs.get("id") and label["for"] == attrs["id"]]
            labels.extend(label["text"].strip() for label in control["wrapped"])
            labelled_by = " ".join(self.id_text.get(identifier, "")
                                    for identifier in attrs.get("aria-labelledby", "").split())
            value = attrs.get("value", "") if tag == "input" and attrs.get("type", "").lower() in {
                "button", "submit", "reset", "image"
            } else ""
            name = (attrs.get("aria-label") or labelled_by or attrs.get("title")
                    or control["text"] or value or " ".join(labels))
            if not name.strip():
                issues.append(f"<{tag}> sin nombre accesible")
        return issues


def audit_control_names() -> int:
    valid_examples = (
        '<button aria-label="Cerrar"></button>',
        '<label for="q">Buscar</label><input id="q">',
        '<label>Equipo<select><option>Zaragoza</option></select></label>',
        '<span id="action">Descargar</span><button aria-labelledby="action"></button>',
        '<button><img src="icon.svg" alt="Compartir"></button>',
    )
    for markup in valid_examples:
        parser = ControlNameParser()
        parser.feed(markup)
        if parser.unnamed_controls():
            raise RuntimeError(f"Falla la autocomprobación de control válido: {markup}")

    parser = ControlNameParser()
    parser.feed('<button></button><input type="text" id="sin-etiqueta">')
    expected = ["<button> sin nombre accesible", "<input> sin nombre accesible"]
    if parser.unnamed_controls() != expected:
        raise RuntimeError("La autocomprobación no detecta un botón sin nombre y un campo sin etiqueta.")

    page_count = 0
    problems = []
    for path in sorted(ROOT.rglob("*.html")):
        parser = ControlNameParser()
        parser.feed(path.read_text(encoding="utf-8"))
        page_count += 1
        for issue in parser.unnamed_controls():
            problems.append(f"{path.relative_to(ROOT)}: {issue}")
    if problems:
        preview = "\n".join(problems[:20])
        remaining = len(problems) - min(len(problems), 20)
        suffix = f"\n... y {remaining} más" if remaining else ""
        raise RuntimeError(f"Controles sin nombre accesible ({len(problems)}):\n{preview}{suffix}")
    return page_count


def audit() -> None:
    styles = {
        path: (ROOT / path).read_text(encoding="utf-8")
        for path in {item[0] for item in TARGETS} | {"assets/experiencia.css"}
    }
    for path, selector in TARGETS:
        sizes = min_heights(styles[path], selector)
        if not sizes or min(sizes) < 44:
            found = ", ".join(f"{size:g}px" for size in sizes) or "ninguna regla min-height"
            raise RuntimeError(f"{selector} en {path}: se requieren 44 px; encontrado {found}.")

    base = styles["assets/estilo.css"]
    experience = styles["assets/experiencia.css"]
    base_focus = declarations(base, ":focus-visible")
    gallery_focus = declarations(experience,
        ".tarjeta-galeria-visual a:focus-visible,.filtros-galeria-visual button:focus-visible")
    if not any(re.search(r"outline\s*:\s*3px\s+solid\s+var\(--senal-texto\)", block)
               for block in base_focus):
        raise RuntimeError("Falta un indicador de foco visible de 3 px con color adaptable al tema.")
    if not any(re.search(r"outline\s*:\s*3px\s+solid\s+var\(--senal-texto\)", block)
               for block in gallery_focus):
        raise RuntimeError("El foco de los filtros y tarjetas de galería debe usar --senal-texto.")

    light = color_tokens(base, ":root")
    dark = light | color_tokens(base, ':root[data-theme="dark"]')
    for theme, tokens in (("claro", light), ("oscuro", dark)):
        panel = tokens["--panel"]
        focus_ratio = contrast(tokens["--senal-texto"], panel)
        svg_text_ratio = contrast(tokens["--tinta-suave"], panel)
        if focus_ratio < 3:
            raise RuntimeError(f"Contraste del foco en tema {theme}: {focus_ratio:.2f}:1 (<3:1).")
        if svg_text_ratio < 4.5:
            raise RuntimeError(f"Contraste del texto de gráficos en tema {theme}: {svg_text_ratio:.2f}:1 (<4,5:1).")

    pages = audit_control_names()
    print(f"Accesibilidad visual: 7 grupos de controles con mínimo 44 px; foco y contraste SVG correctos en claro y oscuro; controles con nombre accesible en {pages} páginas.")


if __name__ == "__main__":
    audit()
