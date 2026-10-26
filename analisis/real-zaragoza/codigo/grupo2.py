"""
El grupo 2 de Primera Federación con los datos de Sofascore: los 20 equipos,
no solo el Zaragoza.

Uso (desde la raíz del repositorio):
    python analisis/real-zaragoza/codigo/grupo2.py

También se ejecuta al final de actualizar.py.

Qué hace:
    1. Lee datos/entrada/grupo2_partidos.csv: una fila por equipo y partido
       (cada partido aparece dos veces, una desde cada lado), con el resultado
       y las estadísticas de Sofascore de los dos equipos.
    2. Calcula una tabla por equipo: puntos, goles, xG a favor y en contra,
       puntos esperados, tiros, calidad de los tiros, posesión…
    3. Dibuja los gráficos en proyectos/real-zaragoza/graficos/grupo2/.
    4. Escribe la pestaña «Grupo 2» (proyectos/real-zaragoza/grupo-2.html)
       con la tabla, los gráficos y el texto de textos/grupo2.html.

Por qué guardo los partidos «por equipo» y no «por partido»:
    Con una fila por partido (local y visitante en columnas) cada cálculo por
    equipo obliga a mirar dos sitios: cuando juega en casa y cuando juega
    fuera. Con una fila por equipo y partido (el formato «team-match», el
    habitual en analítica) basta con un groupby("equipo"). A cambio cada
    partido ocupa dos filas, y eso hay que tenerlo en cuenta al sumar totales
    del grupo (por eso los totales los saco siempre por equipo).

Puntos esperados (xPts):
    Para cada partido supongo que los goles de cada equipo siguen una
    distribución de Poisson con media igual a su xG. Con eso calculo la
    probabilidad de ganar, empatar y perder, y los puntos esperados son
    3 · P(ganar) + 1 · P(empatar). Es una aproximación sencilla y conocida:
    ignora que los goles de un partido no son del todo independientes, pero
    sirve para ver qué equipos van por encima o por debajo de lo que generan.
    Los encuentros sin xG se excluyen de xPts y de su comparación con puntos
    reales: ambas magnitudes usan los mismos partidos. Dos encuentros usan fuentes
    complementarias, identificadas por separado en el CSV y en el método.
"""

import html
import math
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")   # sin ventana: solo guardo los PNG
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
PROYECTO = Path(__file__).resolve().parents[1]
ENTRADA = PROYECTO / "datos" / "entrada"
SALIDA = PROYECTO / "datos" / "salida"
TEXTOS = PROYECTO / "textos"
WEB = PROYECTO.parents[1]
CARPETA_PAGINAS = WEB / "proyectos" / "real-zaragoza"
GRAFICOS = CARPETA_PAGINAS / "graficos" / "grupo2"

ZARAGOZA = "Real Zaragoza"

# Colores: el Zaragoza en azul (con el círculo azul y blanco) y el resto del
# grupo en gris, para que el ojo vaya directo a él sin perder el contexto.
AZUL = "#213e96"
AZUL_CLARO = "#8fa9ce"
NARANJA = "#ff6a2b"
GRIS = "#b7bfb6"
GRIS_OSCURO = "#7c8796"
TINTA = "#11264a"
TINTA_SUAVE = "#4b607e"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 12.5,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.edgecolor": GRIS,
    "axes.labelcolor": TINTA_SUAVE,
    "xtick.color": TINTA_SUAVE,
    "ytick.color": TINTA_SUAVE,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "legend.frameon": False,
})

# Nombres cortos para las etiquetas de los gráficos
CORTOS = {
    "Juventud Torremolinos CF": "Torremolinos",
    "Real Madrid Castilla": "R. M. Castilla",
    "Atlético Madrileño": "At. Madrileño",
    "Rayo Majadahonda": "Majadahonda",
    "CDA Águilas FC": "Águilas",
    "CD Teruel": "Teruel",
    "CE Europa": "Europa",
    "UD Ibiza": "Ibiza",
    "SD Huesca": "Huesca",
    "Real Zaragoza": "Zaragoza",
}

e = html.escape


def corto(nombre):
    return CORTOS.get(nombre, nombre)


# ---------------------------------------------------------------------------
# Puntos esperados
# ---------------------------------------------------------------------------

def poisson(k, media):
    """Probabilidad de marcar exactamente k goles si la media es `media`."""
    return math.exp(-media) * media ** k / math.factorial(k)


def puntos_esperados(xg, xg_rival, max_goles=10):
    """3 · P(ganar) + P(empatar) suponiendo goles de Poisson independientes.

    Recorro todos los marcadores posibles hasta 10-10 (la probabilidad de que
    un equipo de esta categoría marque más de 10 es despreciable) y sumo las
    probabilidades de los que son victoria y los que son empate.
    """
    p_ganar = p_empatar = 0.0
    for a in range(max_goles + 1):
        pa = poisson(a, xg)
        for b in range(max_goles + 1):
            p = pa * poisson(b, xg_rival)
            if a > b:
                p_ganar += p
            elif a == b:
                p_empatar += p
    return 3 * p_ganar + p_empatar


# ---------------------------------------------------------------------------
# Tabla por equipo
# ---------------------------------------------------------------------------

def cargar():
    """Lee los partidos y añade puntos, puntos esperados y una marca de si hay xG."""
    p = pd.read_csv(ENTRADA / "grupo2_partidos.csv", encoding="utf-8-sig")
    p["puntos"] = np.select([p.goles_favor > p.goles_contra, p.goles_favor == p.goles_contra], [3, 1], 0)
    p["con_xg"] = p["xg"].notna() & p["xg_rival"].notna()
    # Un xG ausente no se sustituye por cero ni por el resultado real.
    p["xpts"] = p.apply(lambda f: puntos_esperados(f.xg, f.xg_rival) if f.con_xg else np.nan, axis=1)
    return p


def tabla_equipos(p):
    """Una fila por equipo con todo lo que uso en la página.

    Las medias «por partido» del xG se calculan solo con los partidos que
    tienen xG (si no, un partido sin dato contaría como cero y bajaría la media).
    """
    con = p[p.con_xg]
    t = p.groupby("equipo").agg(
        pj=("jornada", "size"),
        puntos=("puntos", "sum"),
        gf=("goles_favor", "sum"),
        gc=("goles_contra", "sum"),
        xpts=("xpts", lambda v: v.sum(min_count=1)),
        tiros=("tiros", "mean"),
        tiros_contra=("tiros_rival", "mean"),
        posesion=("posesion_pct", "mean"),
        duelos=("duelos_ganados_pct", "mean"),
    )
    x = con.groupby("equipo").agg(
        pj_xg=("jornada", "size"),
        puntos_xg=("puntos", "sum"),
        xg=("xg", "sum"),
        xg_contra=("xg_rival", "sum"),
        gf_xg=("goles_favor", "sum"),     # goles en los partidos con xG, para comparar con justicia
        gc_xg=("goles_contra", "sum"),
        tiros_xg=("tiros", "sum"),
        tiros_contra_xg=("tiros_rival", "sum"),
        dentro=("tiros_dentro_area", "sum"),
    )
    t = t.join(x)
    t["dg"] = t.gf - t.gc
    t["xg_pp"] = t.xg / t.pj_xg                          # xG a favor por partido
    t["xg_contra_pp"] = t.xg_contra / t.pj_xg            # xG en contra por partido
    t["xg_dif_pp"] = t.xg_pp - t.xg_contra_pp            # diferencia por partido: el mejor resumen de «quién domina»
    t["eficacia"] = t.gf_xg - t.xg                       # goles por encima (+) o por debajo (−) de su xG
    t["eficacia_def"] = t.xg_contra - t.gc_xg            # goles encajados por debajo (+, bien) o por encima (−) del xG en contra
    t["xg_por_tiro"] = t.xg / t.tiros_xg                 # calidad media de cada tiro
    t["xg_por_tiro_contra"] = t.xg_contra / t.tiros_contra_xg
    t["pct_dentro"] = t.dentro / t.tiros_xg * 100        # % de tiros desde dentro del área
    t["dif_puntos"] = t.puntos_xg - t.xpts                  # puntos por encima (+) o por debajo (−) de lo esperado
    # Orden de la clasificación: puntos, diferencia de goles y goles a favor.
    # (El reglamento usa primero el enfrentamiento directo, pero con siete
    # jornadas casi ningún empate está resuelto así; lo aviso en la página.)
    t = t.sort_values(["puntos", "dg", "gf"], ascending=False)
    t.insert(0, "posicion", range(1, len(t) + 1))
    return t.reset_index()


def acumulado_por_jornada(p):
    """Diferencia de xG acumulada jornada a jornada de cada equipo (para el gráfico de evolución)."""
    con = p[p.con_xg].copy()
    con["dif"] = con.xg - con.xg_rival
    piv = con.pivot_table(index="jornada", columns="equipo", values="dif", aggfunc="sum").fillna(0)
    return piv.cumsum()


# ---------------------------------------------------------------------------
# Gráficos
# ---------------------------------------------------------------------------

def guardar(fig, nombre):
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    fig.savefig(GRAFICOS / nombre, dpi=160, bbox_inches="tight")
    plt.close(fig)


def punto(ax, x, y, es_zgz, **kw):
    """Punto de un equipo: el Zaragoza con el círculo partido azul y blanco y más grande."""
    if es_zgz:
        ax.plot(x, y, marker="o", markersize=15, fillstyle="left", markerfacecolor=AZUL,
                markerfacecoloralt="white", markeredgecolor=AZUL, markeredgewidth=1.6, ls="", zorder=4)
    else:
        ax.scatter(x, y, s=70, color=GRIS_OSCURO, edgecolor="white", lw=0.8, zorder=3, **kw)


def etiquetas(ax, t, cx, cy, mover=None):
    """Nombre corto junto a cada punto. El del Zaragoza en negrita y azul.

    `mover` es un diccionario {equipo: (dx, dy, alineación)} en puntos tipográficos para
    separar las etiquetas que se pisan (lo calcula solapes()). Son dos o tres
    casos por gráfico y así no meto otra librería (adjustText) solo para esto.
    """
    mover = mover or {}
    ax.margins(x=0.08)   # un poco de aire a los lados para que no se corte ningún nombre
    for f in t.itertuples():
        zgz = f.equipo == ZARAGOZA
        dx, dy, alinear = mover.get(f.equipo, (6, 4, "left"))
        ax.annotate(corto(f.equipo), (getattr(f, cx), getattr(f, cy)), xytext=(dx, dy),
                    textcoords="offset points", ha=alinear,
                    fontsize=9 if zgz else 8, fontweight="bold" if zgz else "normal",
                    color=AZUL if zgz else TINTA_SUAVE, zorder=5)


def solapes(t, cx, cy, eje_y_invertido=False):
    """Busca etiquetas que se van a pisar y decide a dónde mover una de ellas.

    Una etiqueta ocupa más a lo ancho que a lo alto, así que considero que dos
    equipos chocan si están a menos del 12 % del rango en x y del 4 % en y.
    - Si están casi en la misma vertical, bajo la etiqueta del que se ve más
      abajo en el gráfico (ojo: con el eje y invertido, «abajo» es el valor mayor).
    - Si no, paso a la izquierda la etiqueta del que está más a la izquierda.
    Devuelve {equipo: (dx, dy, alineación)} para etiquetas().
    """
    rx = t[cx].max() - t[cx].min()
    ry = t[cy].max() - t[cy].min()
    mover = {}
    filas = list(t.itertuples())
    for i, a in enumerate(filas):
        for b in filas[i + 1:]:
            dx = abs(getattr(a, cx) - getattr(b, cx)) / rx
            dy = abs(getattr(a, cy) - getattr(b, cy)) / ry
            if dx > 0.12 or dy > 0.04:
                continue
            if dx < 0.03:
                # El que se ve más abajo: menor valor de y, o mayor si el eje está invertido
                abajo = max(a, b, key=lambda f: getattr(f, cy)) if eje_y_invertido \
                    else min(a, b, key=lambda f: getattr(f, cy))
                mover.setdefault(abajo.equipo, (6, -12, "left"))
            else:
                izquierda = min(a, b, key=lambda f: getattr(f, cx))
                mover.setdefault(izquierda.equipo, (-6, 4, "right"))
    # Ajustes de lectura para el grupo de puntos más próximo tras la J8.
    if cx == "tiros" and cy == "xg_por_tiro":
        mover.update({"Gimnàstic": (-6, 4, "right"),
                      "SD Huesca": (-6, -12, "right"),
                      "Sant Andreu": (6, -12, "left")})
    if cx == "posesion" and cy == "xg_pp":
        mover.update({"CE Europa": (-6, 10, "right"),
                      "Real Jaén": (-6, -10, "right"),
                      "Juventud Torremolinos CF": (6, -8, "left"),
                      "Sant Andreu": (6, -4, "left"),
                      "SD Huesca": (6, -12, "left")})
    return mover


def mapa_dominio(t):
    """Dispersión: xG a favor por partido (x) frente a xG en contra por partido (y).

    El eje y va invertido para que «arriba» sea siempre bueno (concede poco)
    y «a la derecha» también (genera mucho). Las líneas discontinuas son la
    media del grupo y dividen el gráfico en cuatro cuadrantes.
    """
    fig, ax = plt.subplots(figsize=(9, 7))
    mx, my = t.xg_pp.mean(), t.xg_contra_pp.mean()
    ax.axvline(mx, color=GRIS, ls="--", lw=1)
    ax.axhline(my, color=GRIS, ls="--", lw=1)
    for f in t.itertuples():
        punto(ax, f.xg_pp, f.xg_contra_pp, f.equipo == ZARAGOZA)
    etiquetas(ax, t, "xg_pp", "xg_contra_pp", mover=solapes(t, "xg_pp", "xg_contra_pp", eje_y_invertido=True))
    ax.invert_yaxis()
    # Rótulos de los cuadrantes en las esquinas
    caja = dict(fontsize=8.5, color=TINTA_SUAVE, style="italic")
    ax.text(0.98, 0.86, "Genera mucho y concede poco", transform=ax.transAxes, ha="right", va="top", **caja)
    ax.text(0.02, 0.02, "Genera poco y concede mucho", transform=ax.transAxes, ha="left", va="bottom", **caja)
    ax.set_xlabel("xG a favor por partido →")
    ax.set_ylabel("← xG en contra por partido (arriba, mejor)")
    ax.set_title("Quién domina los partidos en el grupo 2")
    guardar(fig, "dominio.png")


def puntos_vs_esperados(t):
    """Gráfico de pesas (dumbbell): puntos reales frente a puntos esperados.
    La línea une los dos valores; cuanto más larga, más se aleja el equipo de lo que genera."""
    t = t.sort_values("puntos")
    fig, ax = plt.subplots(figsize=(9, 8))
    y = np.arange(len(t))
    for yi, f in zip(y, t.itertuples()):
        zgz = f.equipo == ZARAGOZA
        color = AZUL if zgz else GRIS_OSCURO
        ax.plot([f.xpts, f.puntos_xg], [yi, yi], color=AZUL_CLARO if zgz else GRIS, lw=3, zorder=1)
        ax.scatter(f.xpts, yi, s=55, facecolor="white", edgecolor=color, lw=1.8, zorder=3)
        if zgz:
            ax.plot(f.puntos_xg, yi, marker="o", markersize=10, fillstyle="left", markerfacecolor=AZUL,
                    markerfacecoloralt="white", markeredgecolor=AZUL, ls="", zorder=4)
        else:
            ax.scatter(f.puntos_xg, yi, s=55, color=color, zorder=3)
    ax.set_yticks(y, [corto(f.equipo) + (f" ({f.pj_xg}/{f.pj})" if f.pj_xg < f.pj else "") for f in t.itertuples()])
    for lbl in ax.get_yticklabels():
        if lbl.get_text() == corto(ZARAGOZA):
            lbl.set_color(AZUL)
            lbl.set_fontweight("bold")
    ax.set_xlabel("Puntos")
    ax.scatter([], [], s=55, facecolor="white", edgecolor=GRIS_OSCURO, label="Puntos esperados (xPts)")
    ax.scatter([], [], s=55, color=GRIS_OSCURO, label="Puntos reales en partidos con xG")
    ax.legend(loc="lower right")
    ax.set_title("Puntos reales y esperados · solo partidos con xG")
    guardar(fig, "puntos_esperados.png")


def eficacia(t):
    """Dos barras divergentes por equipo: goles marcados menos su xG (ataque)
    y xG en contra menos goles encajados (portería y defensa). En los dos casos,
    positivo es «mejor de lo esperado»."""
    t = t.sort_values("eficacia")
    fig, axes = plt.subplots(1, 2, figsize=(11, 7), sharey=True)
    y = np.arange(len(t))
    for ax, col, titulo in ((axes[0], "eficacia", "Ataque: goles − xG"),
                            (axes[1], "eficacia_def", "Defensa: xG en contra − goles encajados")):
        colores = [AZUL if n == ZARAGOZA else (GRIS_OSCURO if v >= 0 else NARANJA)
                   for n, v in zip(t.equipo, t[col])]
        ax.barh(y, t[col], color=colores, height=0.65)
        ax.axvline(0, color=TINTA_SUAVE, lw=1)
        ax.set_title(titulo, fontsize=11)
        for yi, v in zip(y, t[col]):
            ax.text(v + (0.08 if v >= 0 else -0.08), yi, con_signo(v, 1), va="center",
                    ha="left" if v >= 0 else "right", fontsize=7.5, color=TINTA_SUAVE)
        lim = max(abs(t[col]).max(), 1) + 1
        ax.set_xlim(-lim, lim)
    axes[0].set_yticks(y, [corto(n) for n in t.equipo])
    for lbl in axes[0].get_yticklabels():
        if lbl.get_text() == corto(ZARAGOZA):
            lbl.set_color(AZUL)
            lbl.set_fontweight("bold")
    fig.suptitle("¿Quién rinde por encima de lo que generan sus ocasiones?", x=0.02, ha="left",
                 fontweight="bold", fontsize=13)
    fig.text(0.02, -0.01, "Positivo: mejor de lo esperado. Solo partidos con xG; dos usan fuentes complementarias.", fontsize=8.5,
             color=TINTA_SUAVE)
    fig.tight_layout()
    guardar(fig, "eficacia.png")


def tiros_y_calidad(t):
    """Dispersión: cuántos tiros hace cada equipo por partido y qué calidad media tienen.
    Arriba a la derecha estarían los que tiran mucho y bien."""
    fig, ax = plt.subplots(figsize=(9, 6.5))
    ax.axvline(t.tiros.mean(), color=GRIS, ls="--", lw=1)
    ax.axhline(t.xg_por_tiro.mean(), color=GRIS, ls="--", lw=1)
    for f in t.itertuples():
        punto(ax, f.tiros, f.xg_por_tiro, f.equipo == ZARAGOZA)
    etiquetas(ax, t, "tiros", "xg_por_tiro", mover=solapes(t, "tiros", "xg_por_tiro"))
    ax.set_xlabel("Tiros por partido")
    ax.set_ylabel("xG por tiro (calidad media)")
    ax.set_title("Volumen y calidad de los tiros")
    guardar(fig, "tiros_calidad.png")


def posesion_y_peligro(t):
    """Dispersión: posesión media frente a xG por partido. Sirve para ver si
    tener el balón se convierte en ocasiones o se queda en posesión estéril."""
    fig, ax = plt.subplots(figsize=(9, 6.5))
    ax.axvline(50, color=GRIS, ls="--", lw=1)
    ax.axhline(t.xg_pp.mean(), color=GRIS, ls="--", lw=1)
    for f in t.itertuples():
        punto(ax, f.posesion, f.xg_pp, f.equipo == ZARAGOZA)
    etiquetas(ax, t, "posesion", "xg_pp", mover=solapes(t, "posesion", "xg_pp"))
    # Recta de regresión (mínimos cuadrados) para ver la tendencia del grupo
    a, b = np.polyfit(t.posesion, t.xg_pp, 1)
    xs = np.linspace(t.posesion.min(), t.posesion.max(), 50)
    ax.plot(xs, a * xs + b, color=AZUL_CLARO, lw=1.2, zorder=1)
    r = np.corrcoef(t.posesion, t.xg_pp)[0, 1]          # correlación de Pearson
    ax.text(0.02, 0.97, f"Correlación: {r:.2f}".replace(".", ","), transform=ax.transAxes, va="top",
            fontsize=9, color=TINTA_SUAVE)
    ax.set_xlabel("Posesión media (%)")
    ax.set_ylabel("xG a favor por partido")
    ax.set_title("¿Tener el balón da ocasiones?")
    guardar(fig, "posesion_peligro.png")


def evolucion(acum, t):
    """Diferencia de xG acumulada jornada a jornada: el Zaragoza y los cinco
    siguientes de la clasificación en color; el resto, en gris de fondo."""
    destacados = list(t.equipo.head(6))
    if ZARAGOZA not in destacados:
        destacados.append(ZARAGOZA)
    paleta = ["#d69e2e", "#805ad5", "#3f8f5c", "#c05621", "#b83280", "#2c7a7b"]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for eq in acum.columns:
        if eq not in destacados:
            ax.plot(acum.index, acum[eq], color=GRIS, lw=1, alpha=0.6, zorder=1)
    i = 0
    for eq in destacados:
        if eq == ZARAGOZA:
            ax.plot(acum.index, acum[eq], color=AZUL, lw=3, zorder=4, label=corto(eq))
        else:
            ax.plot(acum.index, acum[eq], color=paleta[i % len(paleta)], lw=1.8, zorder=3, label=corto(eq))
            i += 1
    ax.axhline(0, color=TINTA_SUAVE, lw=1)
    ax.set_xticks(acum.index, [f"J{j}" for j in acum.index])
    ax.set_ylabel("xG a favor − xG en contra (acumulado)")
    ax.set_title("Evolución de la diferencia de xG")
    ax.legend(ncol=3, fontsize=8.5, loc="upper left")
    guardar(fig, "evolucion_xg.png")


# ---------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------

def con_signo(v, dec=2):
    """+1,4 / −0,7 con el signo menos de verdad (−) y sin el feo «−0,0»."""
    v = round(v, dec)
    if v == 0:
        return numero(0, dec)
    return ("+" if v > 0 else "−") + numero(abs(v), dec)


def numero(v, dec=2):
    """Número a la española, con coma decimal."""
    return f"{v:.{dec}f}".replace(".", ",")


def tabla_html(t):
    """Tabla de la página: clasificación con las métricas de Sofascore al lado."""
    filas = []
    for f in t.itertuples():
        clase = ' class="propio"' if f.equipo == ZARAGOZA else ""
        filas.append(
            f"<tr{clase}><td class=\"n\">{f.posicion}</td><th scope=\"row\">{e(f.equipo)}</th>"
            f"<td class=\"n\">{f.pj}</td><td class=\"n\"><b>{f.puntos}</b></td><td class=\"n\">{f.puntos_xg}</td><td class=\"n\">{numero(f.xpts, 1)}</td>"
            f"<td class=\"n\">{con_signo(f.dif_puntos, 1)}</td>"
            f"<td class=\"n\">{f.gf}–{f.gc}</td><td class=\"n\">{f.pj_xg}/{f.pj}</td><td class=\"n\">{numero(f.xg, 1)}–{numero(f.xg_contra, 1)}</td>"
            f"<td class=\"n\">{con_signo(f.xg_dif_pp)}</td>"
            f"<td class=\"n\">{numero(f.tiros, 1)}</td><td class=\"n\">{numero(f.xg_por_tiro)}</td>"
            f"<td class=\"n\">{numero(f.posesion, 0)} %</td></tr>")
    return f"""<div class="tarjeta tabla" tabindex="0" role="region" aria-label="Tabla del grupo 2, desplazable"><table class="tabla-grupo">
      <thead><tr><th class="n">#</th><th>Equipo</th><th class="n">PJ</th><th class="n">Pts</th><th class="n" title="Puntos reales solo en encuentros con xG">Pts con xG</th><th class="n" title="Puntos esperados solo en encuentros con xG">xPts</th>
      <th class="n" title="Puntos reales menos esperados, solo en los mismos partidos con xG">Dif.</th><th class="n">Goles</th><th class="n" title="Partidos con xG sobre partidos jugados">PJ xG</th><th class="n">xG</th>
      <th class="n" title="xG a favor menos xG en contra, por partido">xG dif./PJ</th><th class="n">Tiros/PJ</th>
      <th class="n">xG/tiro</th><th class="n">Posesión</th></tr></thead>
      <tbody>{"".join(filas)}</tbody></table></div>"""


def actualidad_html():
    """Resultados y clasificación revisados, independientes del corte de xG."""
    c = pd.read_csv(ENTRADA / "clasificacion.csv")
    j = int(c.tras_jornada.max())
    c = c[c.tras_jornada == j].sort_values("posicion")
    resultados = pd.read_csv(ENTRADA / "grupo2_resultados.csv")
    resultados = resultados[resultados.jornada == j]
    filas = []
    for f in c.itertuples():
        clase = ' class="propio"' if f.equipo == ZARAGOZA else ""
        filas.append(f'<tr{clase}><td>{f.posicion}</td><th scope="row">{e(f.equipo)}</th>'
                     f'<td>{f.pj}</td><td><b>{f.puntos}</b></td><td>{f.g}</td><td>{f.e}</td>'
                     f'<td>{f.p}</td><td>{f.gf}</td><td>{f.gc}</td><td>{f.gf-f.gc:+d}</td></tr>')
    partidos = ''.join(f'<li>{e(f.local)} <strong>{f.goles_local}–{f.goles_visitante}</strong> {e(f.visitante)}</li>'
                       for f in resultados.itertuples())
    return j, f"""<section class="seccion" aria-labelledby="t-actualidad">
    <p class="etiqueta">Actualizado el 20/10/2026 · Jornada {j} completa</p>
    <h2 id="t-actualidad">Resultados y clasificación tras la jornada {j}</h2>
    <p>El Villarreal B alcanza al Zaragoza con 17 puntos y lidera por diferencia de goles (+8 frente a +6). El Murcia queda tercero con 16; Cartagena y Real Jaén suman 15. La jornada deja 25 goles: seis victorias locales, una visitante y tres empates.</p>
    <ul>{partidos}</ul>
    <div class="tarjeta tabla" tabindex="0" role="region" aria-label="Clasificación tras la jornada {j}, desplazable"><table>
    <thead><tr><th>#</th><th>Equipo</th><th>PJ</th><th>Pts</th><th>G</th><th>E</th><th>P</th><th>GF</th><th>GC</th><th>DG</th></tr></thead>
    <tbody>{''.join(filas)}</tbody></table></div>
    <p class="nota">Fuentes: <a href="{e(resultados.iloc[0].fuente_url)}" target="_blank" rel="noopener">resultados de AS</a> y <a href="{e(c.iloc[0].fuente_url)}" target="_blank" rel="noopener">clasificación en la web del Real Zaragoza</a>. Los empates se muestran por diferencia de goles; la clasificación definitiva depende de los criterios reglamentarios.</p>
    </section>"""


def escribir_pagina(t, jornada):
    """Monta grupo-2.html con la misma cabecera, pestañas y pie que el resto."""
    import paginas_partidos as pp                      # reutilizo la plantilla y las pestañas
    texto_ruta = TEXTOS / "grupo2.html"
    analisis = texto_ruta.read_text(encoding="utf-8") if texto_ruta.exists() else ""
    figura = lambda archivo, alt, pie: (f'<figure class="figura"><img src="graficos/grupo2/{archivo}?v=j{jornada}-xg79-cobertura" alt="{alt}" '
                                        f'loading="lazy"><figcaption>{pie}</figcaption></figure>')
    jornada_actual, actualidad = actualidad_html()
    cuerpo = f"""<main class="envoltorio">
  <p class="migas"><a href="../index.html">Proyectos</a> / <a href="index.html">Real Zaragoza 2026/27</a> / Grupo 2</p>
  {pp.pestanas("grupo")}
  <section class="seccion primera" aria-labelledby="t-grupo">
    <p class="etiqueta">Primera Federación · Grupo 2 · Resultados J{jornada_actual} · Estadísticas avanzadas J{jornada}</p>
    <h1 id="t-grupo">El grupo 2, con datos</h1>
    <p class="entradilla">Clasificación y resultados hasta la jornada {jornada_actual}. La comparación de xG, puntos esperados, tiros y posesión está actualizada hasta la jornada {jornada}, con la cobertura indicada en cada apartado.</p>
  </section>
  {actualidad}
  <section class="seccion" aria-labelledby="t-simulacion">
    <p class="etiqueta">Investigación</p><h2 id="t-simulacion">¿Y si el grupo 2 se jugara 10.000 veces?</h2>
    <p>Una simulación de lo que queda de temporada con las probabilidades de ascenso, playoff y descenso de los 20 equipos.</p>
    <div class="enlaces"><a class="boton lleno" href="simulacion.html">Leer la simulación</a></div>
  </section>
  <section class="seccion lectura" aria-labelledby="t-lectura">
    <p class="etiqueta">Lo que dicen los datos</p><h2 id="t-lectura">Lectura avanzada · J{jornada}</h2>
    {analisis}
  </section>
  <section class="seccion" aria-labelledby="t-tabla">
    <p class="etiqueta">Clasificación ampliada</p><h2 id="t-tabla">La tabla, con xG · J{jornada}</h2>
    <p class="nota">Ordenada por puntos, diferencia de goles y goles a favor. PJ xG: encuentros con xG sobre partidos jugados. Los goles esperados totales y su diferencia se calculan solo en partidos con dato. Pts: puntos de toda la liga. Pts con xG y xPts: puntos reales y esperados solo en los encuentros con xG. Dif.: resta de estas dos últimas columnas; no incluye partidos sin dato.</p>
    {tabla_html(t)}
  </section>
  <section class="seccion lectura" aria-labelledby="t-graficos">
    <p class="etiqueta">Gráficos</p><h2 id="t-graficos">El grupo, en seis gráficos · J{jornada}</h2>
    {figura("dominio.png", "Dispersión de xG a favor y en contra por partido de los 20 equipos", "Cada punto es un equipo. Arriba a la derecha, los que generan mucho y conceden poco. Las líneas discontinuas son la media del grupo.")}
    {figura("puntos_esperados.png", "Puntos reales y puntos esperados de cada equipo", "Círculo hueco: puntos esperados. Círculo lleno: puntos reales de los mismos encuentros con xG. Los equipos con cobertura incompleta indican sus partidos entre paréntesis; sus totales no representan toda la temporada.")}
    {figura("eficacia.png", "Goles marcados menos xG y xG en contra menos goles encajados por equipo", "Izquierda: acierto de cara a puerta. Derecha: acierto del portero y la defensa. Positivo, mejor de lo esperado.")}
    {figura("evolucion_xg.png", "Diferencia de xG acumulada por jornada de los equipos de arriba", "El Zaragoza y los cinco primeros de la tabla; el resto, en gris.")}
    {figura("tiros_calidad.png", "Tiros por partido y xG por tiro de cada equipo", "Volumen (eje horizontal) frente a calidad media de cada tiro (eje vertical).")}
    {figura("posesion_peligro.png", "Posesión media y xG por partido de cada equipo", "La línea azul claro es la tendencia del grupo.")}
  </section>
  <section class="seccion lectura" id="metodo-grupo" aria-labelledby="t-metodo-grupo">
    <p class="etiqueta">Cómo está hecho</p><h2 id="t-metodo-grupo">Método y límites</h2>
    <ul>
      <li>Base de Sofascore de los {int(t.pj.sum() / 2)} partidos jugados del grupo, con dos xG recuperados de fuentes complementarias; la J8 está contrastada con capturas y texto aportados por el usuario. Tabla completa: en <a href="../../analisis/real-zaragoza/datos/entrada/grupo2_partidos.csv">grupo2_partidos.csv</a> (una fila por equipo y partido).</li>
      <li>Los puntos esperados suponen que los goles de cada equipo siguen una distribución de Poisson con media igual a su xG. Es una aproximación: no tiene en cuenta el marcador ni cómo cambia un partido después de un gol.</li>
      <li>Hay xG en 79 de los 80 encuentros: 77 de Sofascore y dos de fuentes complementarias. Villarreal B–Algeciras (J2): 0,93–2,07, publicado por <a href="https://scangoal.com/h2h/algeciras-vs-villarreal-b">ScanGoal</a>. Gimnàstic–Sant Andreu (J5): 0,52–2,19, publicado por <a href="https://nb-bet.com/en/Events/1624476-himnastik-sant-andryu-prognoz-na-match">nb-bet</a> y coincidente en ScanGoal. No se ha confirmado el proveedor ni el modelo de estos dos xG: la serie combinada puede tener diferencias metodológicas. Las columnas fuente_xg y nota_xg identifican su procedencia; se conserva la <a href="../../analisis/real-zaragoza/datos/salida/grupo2_equipos_solo_sofascore.csv">tabla calculada solo con Sofascore</a> para comparar. Huesca–Sant Andreu (J1) sigue sin xG fiable: se excluye de las medias de xG y de ambos lados de la comparación entre puntos reales y esperados. No se le asigna un xG ni xPts. PJ xG indica la cobertura de cada equipo.</li>
      <li>Con {jornada} jornadas, una racha buena o mala de cara a puerta pesa mucho. Estas cifras describen lo que ha pasado; no predicen la clasificación final.</li>
      <li>La tabla ordena los empates por diferencia de goles. El reglamento usa antes el enfrentamiento directo, así que algún puesto puede no coincidir con la clasificación oficial.</li>
    </ul>
    <div class="enlaces"><a class="boton lleno" href="https://github.com/lineadepase/lineadepase.github.io/blob/main/analisis/real-zaragoza/codigo/grupo2.py" target="_blank" rel="noopener">Ver el código</a><a class="boton" href="index.html">Volver a la temporada</a></div>
  </section>
</main>"""
    (CARPETA_PAGINAS / "grupo-2.html").write_text(
        pp.pagina(f"Grupo 2 de Primera Federación: resultados J{jornada_actual} y datos avanzados J{jornada}",
                  "Los 20 equipos del grupo 2 de Primera Federación con xG, puntos esperados, tiros y posesión, con fuentes y cobertura documentadas.",
                  cuerpo), encoding="utf-8")


def main():
    p = cargar()
    t = tabla_equipos(p)
    # Guardo la tabla por equipo en UTF-8 con BOM, para que Excel enseñe bien las tildes
    SALIDA.mkdir(parents=True, exist_ok=True)
    t.round(3).to_csv(SALIDA / "grupo2_equipos.csv", index=False, encoding="utf-8-sig")
    # Una segunda tabla permite consultar solo la cobertura de Sofascore.
    original = p.copy()
    extra = original["nota_xg"].fillna("").ne("")
    original.loc[extra, ["xg", "xg_rival", "xpts"]] = np.nan
    original.loc[extra, "con_xg"] = False
    tabla_equipos(original).round(3).to_csv(
        SALIDA / "grupo2_equipos_solo_sofascore.csv", index=False, encoding="utf-8-sig")
    mapa_dominio(t)
    puntos_vs_esperados(t)
    eficacia(t)
    tiros_y_calidad(t)
    posesion_y_peligro(t)
    evolucion(acumulado_por_jornada(p), t)
    jornada = int(p.jornada.max())
    escribir_pagina(t, jornada)
    z = t[t.equipo == ZARAGOZA].iloc[0]
    print(f"Grupo 2 tras la J{jornada}: {len(t)} equipos, {int(t.pj.sum() / 2)} partidos.")
    print(f"Zaragoza: {z.posicion}.º, {z.puntos} pts, {z.xpts:.1f} xPts, xG dif./PJ {z.xg_dif_pp:+.2f}")


if __name__ == "__main__":
    main()
