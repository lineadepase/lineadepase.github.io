"""Comprueba tamaño de controles, foco visible y contraste de tokens visuales."""
from __future__ import annotations

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

    print("Accesibilidad visual: 7 grupos de controles con mínimo 44 px; foco visible y contraste de texto SVG correctos en claro y oscuro.")


if __name__ == "__main__":
    audit()
