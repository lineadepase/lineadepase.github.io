"""
Diapositivas de la previa ampliada para redes (1080 × 1350 px) y gráfico para la web.

Completa la portada (previa_portada.py) y la tarjeta de datos (previa_redes.py):
    03 cómo llega el rival: goles frente a xG, jornada a jornada
    04 jugador a seguir
    05 expectativa del partido según el modelo de goles
    06 cierre con la web y las cuentas de Línea de pase

Los datos del rival salen de datos/entrada/grupo2_partidos.csv. El jugador y la
expectativa, de textos/previa_j<N>_carrusel.json, que se rellena a mano con sus
fuentes. Uso, después de previa_redes.py:
    python analisis/real-zaragoza/codigo/previa_carrusel.py 9

Escribe datos/salida/previa_03_tendencia.png ... previa_06_cierre.png y el
gráfico de la web en proyectos/real-zaragoza/graficos/previa/rival_xg.png.
"""

import json
import sys
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Rectangle

from cargar_datos import CARPETA_ENTRADA, CARPETA_SALIDA, CARPETA_TEXTOS, RAIZ_WEB

FONDO = "#12221d"
PANEL = "#1a2f27"
TEXTO = "#f2f4ef"
SUAVE = "#9fb3a7"
VERDE_CLARO = "#a8d5b5"
VERDE = "#3f8f5a"
NARANJA = "#ff7a2f"
LINEA = "#3b5247"
GRIS = "#8a958e"

CUENTAS = [
    ("Web", "lineadepase.com"),
    ("Instagram", "@lineadepasefutbol"),
    ("YouTube", "@lineadepasefutbol"),
    ("Facebook", "Línea de pase"),
    ("LinkedIn", "Ángel Marqueta Alonso"),
]


def num(x, dec=1):
    """Número con coma decimal."""
    return f"{x:.{dec}f}".replace(".", ",")


def lienzo(jornada, seccion):
    plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]
    fig = plt.figure(figsize=(7.2, 9), dpi=150)
    fig.patch.set_facecolor(FONDO)
    fig.text(0.08, 0.925, "LÍNEA DE PASE", fontsize=13, fontweight="bold", color=TEXTO)
    fig.text(0.08, 0.885, f"PREVIA · JORNADA {jornada} · {seccion}", fontsize=11.5,
             fontweight="bold", color=VERDE_CLARO)
    return fig


def pie(fig, texto):
    fig.add_artist(Rectangle((0.08, 0.118), 0.06, 0.004, color=NARANJA, transform=fig.transFigure))
    fig.add_artist(Line2D([0.14, 0.92], [0.12, 0.12], color=LINEA, lw=1))
    fig.text(0.08, 0.075, "lineadepase.com", fontsize=13, fontweight="bold", color=TEXTO)
    fig.text(0.08, 0.045, texto, fontsize=9.5, color=SUAVE)


def partidos_rival(rival):
    d = pd.read_csv(CARPETA_ENTRADA / "grupo2_partidos.csv")
    return d[d["equipo"] == rival].sort_values("jornada")


def tendencia(p, rival, jornada, corte, ruta):
    fig = lienzo(jornada, "CÓMO LLEGA EL RIVAL")
    gf, xg = int(p["goles_favor"].sum()), p["xg"].sum()
    gc, xga = int(p["goles_contra"].sum()), p["xg_rival"].sum()
    fig.text(0.08, 0.81, f"{rival}: crea más", fontsize=27, fontweight="bold", color=TEXTO)
    fig.text(0.08, 0.765, "de lo que marca", fontsize=27, fontweight="bold", color=TEXTO)
    fig.text(0.08, 0.72, f"{gf} goles con {num(xg)} xG a favor · {gc} encajados con {num(xga)} xG en contra",
             fontsize=11.5, color=SUAVE)

    etiquetas = [f"J{j}" for j in p["jornada"]]
    x = range(len(p))
    for i, (col_g, col_xg, titulo, y0) in enumerate([
            ("goles_favor", "xg", "A favor", 0.46), ("goles_contra", "xg_rival", "En contra", 0.185)]):
        ax = fig.add_axes([0.08, y0, 0.84, 0.18])
        ax.set_facecolor(FONDO)
        lado = titulo.lower()
        ax.bar(x, p[col_g], color=VERDE if i == 0 else "#b8452a", width=0.6, label=f"Goles {lado}")
        ax.plot(x, p[col_xg], color=TEXTO, marker="o", lw=2, ms=5.5, label=f"xG {lado}")
        ax.set_xticks(list(x), etiquetas, color=SUAVE, fontsize=10)
        ax.set_ylim(0, 3.6)
        ax.set_yticks([0, 1, 2, 3])
        ax.tick_params(colors=SUAVE, labelsize=10, length=0)
        for lado in ("top", "right", "left"):
            ax.spines[lado].set_visible(False)
        ax.spines["bottom"].set_color(LINEA)
        ax.grid(axis="y", color=LINEA, lw=0.6)
        ax.set_axisbelow(True)
        ax.text(0.0, 1.1, titulo.upper(), fontsize=10.5, fontweight="bold", color=NARANJA, transform=ax.transAxes)
        ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.22), ncol=2, fontsize=10,
                  labelcolor=SUAVE, frameon=False)
    pie(fig, f"Goles y xG por partido, jornadas 1 a {corte}. Fuente: Sofascore.")
    fig.savefig(ruta, dpi=150, facecolor=FONDO)
    plt.close(fig)


def grafico_web(p, rival, ruta):
    """Versión clara para la página, con los colores de los gráficos del informe."""
    plt.rcParams["font.family"] = ["DejaVu Sans"]
    fig, ejes = plt.subplots(1, 2, figsize=(10, 3.8), dpi=150, sharey=True)
    x = range(len(p))
    etiquetas = [f"J{j}" for j in p["jornada"]]
    for ax, (col_g, col_xg, titulo, color) in zip(ejes, [
            ("goles_favor", "xg", "A favor", "#1f6b3e"), ("goles_contra", "xg_rival", "En contra", "#b8452a")]):
        ax.bar(x, p[col_g], color=color, width=0.6, label=f"Goles {titulo.lower()}")
        ax.plot(x, p[col_xg], color="#0f2418", marker="o", lw=2, label=f"xG {titulo.lower()}")
        ax.legend(frameon=False, loc="upper left")
        ax.set_xticks(list(x), etiquetas)
        ax.set_title(f"{rival} · {titulo.lower()}", loc="left", fontweight="bold", color="#0f2418")
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#e3e7e0")
        ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150, facecolor="white")
    plt.close(fig)


def jugador(c, jornada, ruta):
    j = c["jugador"]
    fig = lienzo(jornada, "JUGADOR A SEGUIR")
    titular = textwrap.wrap(j.get("titulo", f"Jugador a seguir del {c['rival']}"), 24)
    for k, linea in enumerate(titular[:2]):
        fig.text(0.08, 0.81 - 0.045 * k, linea, fontsize=27, fontweight="bold", color=TEXTO)
    # Dorsal grande en lugar de foto (sin imágenes con derechos de terceros)
    fig.add_artist(FancyBboxPatch((0.08, 0.465), 0.30, 0.24, transform=fig.transFigure,
                                  boxstyle="round,pad=0,rounding_size=0.02", fc=PANEL, ec=LINEA))
    fig.text(0.23, 0.585, j["dorsal"], fontsize=110, fontweight="bold", color=NARANJA,
             ha="center", va="center")
    fig.text(0.44, 0.655, j["nombre"].split(" ")[0], fontsize=24, fontweight="bold", color=TEXTO)
    fig.text(0.44, 0.615, " ".join(j["nombre"].split(" ")[1:]), fontsize=24, fontweight="bold", color=TEXTO)
    fig.text(0.44, 0.565, c["rival"], fontsize=13, color=VERDE_CLARO, fontweight="bold")
    fig.text(0.44, 0.53, f"{j['posicion']} · {j['edad']} años", fontsize=12.5, color=SUAVE)
    y = 0.385
    for cifra, texto in j["datos"]:
        fig.text(0.08, y, cifra, fontsize=30, fontweight="bold", color=TEXTO)
        fig.text(0.30, y + 0.012, texto, fontsize=12.5, color=SUAVE)
        y -= 0.062
    fig.text(0.08, 0.2, textwrap.fill(j["lectura"], 62), fontsize=11.5, color=TEXTO, linespacing=1.5, va="top")
    pie(fig, f"Datos de liga hasta la jornada {jornada - 1}. Fuentes: {j['fuentes']}.")
    fig.savefig(ruta, dpi=150, facecolor=FONDO)
    plt.close(fig)


def expectativa(c, jornada, local, visitante, ruta):
    e = c["expectativa"]
    fig = lienzo(jornada, "EXPECTATIVA")
    fig.text(0.08, 0.81, "Un partido abierto", fontsize=27, fontweight="bold", color=TEXTO)
    fig.text(0.08, 0.765, "según el modelo", fontsize=27, fontweight="bold", color=TEXTO)
    filas = [(f"Gana {local}", e["local"], GRIS), ("Empate", e["empate"], "#5d6b63"),
             (f"Gana {visitante}", e["visitante"], NARANJA)]
    y = 0.64
    for etiqueta, valor, color in filas:
        fig.text(0.08, y + 0.04, etiqueta, fontsize=13, color=TEXTO, fontweight="bold")
        fig.add_artist(Rectangle((0.08, y), 0.84, 0.028, color=PANEL, transform=fig.transFigure))
        fig.add_artist(Rectangle((0.08, y), 0.84 * valor / 100, 0.028, color=color, transform=fig.transFigure))
        fig.text(0.92, y + 0.04, f"{num(valor)} %", fontsize=13, color=TEXTO, fontweight="bold", ha="right")
        y -= 0.105
    fig.text(0.08, 0.32, f"Goles esperados: {num(e['goles_local'], 2)} – {num(e['goles_visitante'], 2)}",
             fontsize=15, fontweight="bold", color=TEXTO)
    fig.text(0.08, 0.295, textwrap.fill(e["lectura"], 66), fontsize=11, color=SUAVE, linespacing=1.5, va="top")
    fig.text(0.08, 0.16, "Una probabilidad no es un pronóstico.", fontsize=11, color=TEXTO, fontweight="bold")
    pie(fig, "Modelo de Poisson con ataque, defensa y ventaja de campo · 80 partidos del grupo 2.")
    fig.savefig(ruta, dpi=150, facecolor=FONDO)
    plt.close(fig)


def cierre(ruta):
    plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]
    fig = plt.figure(figsize=(7.2, 9), dpi=150)
    fig.patch.set_facecolor(FONDO)
    eje = fig.add_axes([0.08, 0.80, 0.11, 0.088])
    eje.imshow(plt.imread(RAIZ_WEB / "assets" / "logo.png"))
    eje.axis("off")
    fig.text(0.22, 0.835, "Línea de pase", fontsize=24, fontweight="bold", color=TEXTO)
    fig.text(0.08, 0.715, "Fútbol explicado", fontsize=32, fontweight="bold", color=TEXTO)
    fig.text(0.08, 0.66, "con datos", fontsize=32, fontweight="bold", color=NARANJA)
    fig.text(0.08, 0.635, "Previas, análisis jornada a jornada y herramientas\npara explorar el grupo 2 de Primera Federación.",
             fontsize=12.5, color=SUAVE, linespacing=1.5, va="top")
    y = 0.46
    for red, cuenta in CUENTAS:
        fig.add_artist(Line2D([0.08, 0.92], [y - 0.022, y - 0.022], color=LINEA, lw=0.8))
        fig.text(0.08, y, red.upper(), fontsize=10.5, fontweight="bold", color=VERDE_CLARO)
        fig.text(0.92, y - 0.004, cuenta, fontsize=15, fontweight="bold", color=TEXTO, ha="right")
        y -= 0.065
    fig.add_artist(FancyBboxPatch((0.08, 0.075), 0.84, 0.07, transform=fig.transFigure,
                                  boxstyle="round,pad=0,rounding_size=0.015", fc=NARANJA, ec="none"))
    fig.text(0.5, 0.11, "Síguenos y guarda la previa para el partido", fontsize=14, fontweight="bold",
             color=FONDO, ha="center", va="center")
    fig.savefig(ruta, dpi=150, facecolor=FONDO)
    plt.close(fig)


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        raise SystemExit("Uso: python previa_carrusel.py <jornada>")
    jornada = int(sys.argv[1])
    c = json.loads((CARPETA_TEXTOS / f"previa_j{jornada}_carrusel.json").read_text(encoding="utf-8"))
    base = json.loads((CARPETA_SALIDA / "previa_redes.json").read_text(encoding="utf-8"))
    if base["jornada"] != jornada:
        raise SystemExit("previa_redes.json no es de esta jornada: ejecuta antes previa_redes.py")
    p = partidos_rival(c["rival"])
    corte = base["datos_hasta_jornada"]
    p = p[p["jornada"] <= corte]

    tendencia(p, c["rival"], jornada, corte, CARPETA_SALIDA / "previa_03_tendencia.png")
    jugador(c, jornada, CARPETA_SALIDA / "previa_04_jugador.png")
    expectativa(c, jornada, base["local"], base["visitante"], CARPETA_SALIDA / "previa_05_expectativa.png")
    cierre(CARPETA_SALIDA / "previa_06_cierre.png")
    carpeta_web = RAIZ_WEB / "proyectos" / "real-zaragoza" / "graficos" / "previa"
    carpeta_web.mkdir(parents=True, exist_ok=True)
    grafico_web(p, c["rival"], carpeta_web / "rival_xg.png")
    print("Diapositivas de la previa generadas")


if __name__ == "__main__":
    main()
