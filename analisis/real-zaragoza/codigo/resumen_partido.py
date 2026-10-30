"""
Resumen del partido para la web y las redes (jornada 9: CE Europa 0-1 Real Zaragoza).

Lee las cifras de textos/video/jornada-N.json (sacadas de la ficha oficial del
club y de la revisión del resumen en vídeo) y dibuja:
    - proyectos/real-zaragoza/graficos/jornada-N/balon_y_remates.png (web)
    - datos/salida/resumen_jN_01..04.png (carrusel de 1080 × 1350 para redes)

Uso (desde la raíz del repositorio):
    python analisis/real-zaragoza/codigo/resumen_partido.py 9
"""

import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from cargar_datos import CARPETA_SALIDA, CARPETA_TEXTOS, RAIZ_WEB

LOGO = RAIZ_WEB / "assets" / "logo.png"

# Colores de la web (los mismos que tarjeta_dato.py)
PAPEL = "#f5f6f2"
TINTA = "#14261d"
TINTA_SUAVE = "#55635b"
VERDE = "#2f6b45"
NARANJA = "#d9480f"
GRIS = "#b9c2bb"
LINEA = "#d9ddd4"


def coma(x, decimales=1):
    return f"{x:.{decimales}f}".replace(".", ",")


def pie(fig, fuentes):
    """Línea, logo y fuentes abajo, igual que la tarjeta del dato."""
    fig.add_artist(Line2D([0.08, 0.92], [0.12, 0.12], color=LINEA, lw=1.2))
    eje_logo = fig.add_axes([0.08, 0.042, 0.075, 0.056])
    eje_logo.imshow(plt.imread(LOGO))
    eje_logo.axis("off")
    fig.text(0.175, 0.08, "Línea de pase · lineadepase.com", fontsize=11.5, color=TINTA)
    fig.text(0.175, 0.055, fuentes, fontsize=9.5, color=TINTA_SUAVE)


def cabecera(fig, d, titulo):
    fig.text(0.08, 0.92, f"RESUMEN DEL PARTIDO · JORNADA {d['jornada']}", fontsize=13, color=NARANJA, fontweight="bold")
    fig.text(0.08, 0.885, f"{d['local']} {d['marcador']} {d['visitante']} · Primera Federación", fontsize=12, color=TINTA_SUAVE)
    for i, linea in enumerate(titulo):
        fig.text(0.08, 0.81 - 0.05 * i, linea, fontsize=24, fontweight="bold", color=TINTA)


def barras_cuota(ax, cuotas, tam=14):
    """Cuota del Zaragoza en cada métrica, con la línea del 50 %."""
    etiquetas = [c["etiqueta"] for c in cuotas]
    valores = [c["zaragoza_pct"] for c in cuotas]
    ax.barh(etiquetas, [100] * len(valores), color=GRIS, height=0.55)
    ax.barh(etiquetas, valores, color=VERDE, height=0.55)
    ax.axvline(50, color=TINTA, lw=1, ls="--")
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    for i, c in enumerate(cuotas):
        ax.text(2, i, f"{coma(c['zaragoza_pct'])} %", va="center", color="white", fontsize=tam, fontweight="bold")
        ax.text(98, i, f"{coma(100 - c['zaragoza_pct'])} %", va="center", ha="right", color=TINTA, fontsize=tam - 2)
    ax.tick_params(axis="y", length=0, labelsize=tam - 1, colors=TINTA)
    ax.tick_params(axis="x", length=0, labelbottom=False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_facecolor(PAPEL)


def grafico_web(d, ruta):
    plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=120)
    fig.patch.set_facecolor(PAPEL)
    barras_cuota(ax, d["cuotas"], tam=13)
    ax.set_title("Parte del Zaragoza en cada métrica (verde) frente a la del CE Europa (gris)",
                 loc="left", fontsize=13, color=TINTA, pad=14)
    fig.text(0.01, 0.02, "La línea discontinua marca el reparto a partes iguales. Fuente: ficha oficial del Real Zaragoza. "
             "Cuota de tiros = tiros del equipo / 17.", fontsize=9.5, color=TINTA_SUAVE)
    fig.subplots_adjust(left=0.2, right=0.97, top=0.85, bottom=0.12)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=120, facecolor=PAPEL)
    plt.close(fig)


def carrusel(d, carpeta):
    plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]
    rutas = []
    tam = dict(figsize=(7.2, 9), dpi=150)

    # 1. Portada
    fig = plt.figure(**tam); fig.patch.set_facecolor(PAPEL)
    cabecera(fig, d, d["portada"]["titulo"])
    fig.text(0.08, 0.53, d["marcador"], fontsize=96, fontweight="bold", color=VERDE)
    for i, linea in enumerate(d["portada"]["texto"]):
        fig.text(0.08, 0.43 - 0.038 * i, linea, fontsize=14, color=TINTA_SUAVE)
    pie(fig, d["fuentes_redes"])
    rutas.append(carpeta / f"resumen_j{d['jornada']}_01.png"); fig.savefig(rutas[-1], dpi=150, facecolor=PAPEL); plt.close(fig)

    # 2. Cuotas
    fig = plt.figure(**tam); fig.patch.set_facecolor(PAPEL)
    cabecera(fig, d, ["Más balón y más pases,", "remates casi igualados"])
    ax = fig.add_axes([0.32, 0.36, 0.6, 0.32])
    barras_cuota(ax, d["cuotas"], tam=14)
    fig.text(0.08, 0.3, "Verde: Real Zaragoza · Gris: CE Europa", fontsize=12, color=TINTA_SUAVE)
    fig.text(0.08, 0.265, "Línea discontinua: reparto a partes iguales", fontsize=12, color=TINTA_SUAVE)
    fig.text(0.08, 0.2, f"{d['pases']['zaragoza']} pases frente a {d['pases']['rival']}; {d['tiros']['zaragoza']} tiros frente a {d['tiros']['rival']}.",
             fontsize=14, color=TINTA, fontweight="bold")
    pie(fig, d["fuentes_redes"])
    rutas.append(carpeta / f"resumen_j{d['jornada']}_02.png"); fig.savefig(rutas[-1], dpi=150, facecolor=PAPEL); plt.close(fig)

    # 3. Pases y tiros
    fig = plt.figure(**tam); fig.patch.set_facecolor(PAPEL)
    cabecera(fig, d, ["Circulación limpia,", "pocas llegadas a puerta"])
    filas = [("Pases completados", d["pases_completados"]["zaragoza"], d["pases_completados"]["rival"], ""),
             ("Precisión de pase", coma(d["precision"]["zaragoza"]), coma(d["precision"]["rival"]), " %"),
             ("Tiros", d["tiros"]["zaragoza"], d["tiros"]["rival"], ""),
             ("Tiros a puerta", d["tiros_puerta"]["zaragoza"], d["tiros_puerta"]["rival"], "")]
    fig.text(0.62, 0.66, "Zaragoza", fontsize=12, color=VERDE, fontweight="bold", ha="right")
    fig.text(0.9, 0.66, "Europa", fontsize=12, color=TINTA_SUAVE, fontweight="bold", ha="right")
    for i, (et, z, r, u) in enumerate(filas):
        y = 0.6 - 0.085 * i
        fig.text(0.08, y, et, fontsize=15, color=TINTA)
        fig.text(0.62, y, f"{z}{u}", fontsize=22, color=VERDE, fontweight="bold", ha="right")
        fig.text(0.9, y, f"{r}{u}", fontsize=22, color=TINTA_SUAVE, fontweight="bold", ha="right")
        fig.add_artist(Line2D([0.08, 0.92], [y - 0.025, y - 0.025], color=LINEA, lw=1))
    fig.text(0.08, 0.2, "Sin xG publicado, los tiros miden volumen,", fontsize=12, color=TINTA_SUAVE)
    fig.text(0.08, 0.17, "no la calidad de las ocasiones.", fontsize=12, color=TINTA_SUAVE)
    pie(fig, d["fuentes_redes"])
    rutas.append(carpeta / f"resumen_j{d['jornada']}_03.png"); fig.savefig(rutas[-1], dpi=150, facecolor=PAPEL); plt.close(fig)

    # 4. El gol y la temporada
    fig = plt.figure(**tam); fig.patch.set_facecolor(PAPEL)
    cabecera(fig, d, ["Un córner decidió", "el partido"])
    for i, paso in enumerate(d["gol"]):
        y = 0.66 - 0.075 * i
        fig.text(0.08, y, f"{i + 1}", fontsize=20, color=NARANJA, fontweight="bold")
        fig.text(0.15, y, paso, fontsize=15, color=TINTA)
    for i, linea in enumerate(d["temporada"]):
        fig.text(0.08, 0.3 - 0.04 * i, linea, fontsize=13, color=TINTA_SUAVE)
    pie(fig, d["fuentes_redes"])
    rutas.append(carpeta / f"resumen_j{d['jornada']}_04.png"); fig.savefig(rutas[-1], dpi=150, facecolor=PAPEL); plt.close(fig)
    return rutas


def main():
    jornada = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    d = json.loads((CARPETA_TEXTOS / "video" / f"resumen_redes_j{jornada}.json").read_text(encoding="utf-8"))
    grafico_web(d, RAIZ_WEB / "proyectos" / "real-zaragoza" / "graficos" / f"jornada-{jornada}" / "balon_y_remates.png")
    for r in carrusel(d, CARPETA_SALIDA):
        print(r)


if __name__ == "__main__":
    main()
