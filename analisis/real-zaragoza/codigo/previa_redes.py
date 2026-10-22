"""
Imagen y cifras de la previa para redes (Instagram, Facebook y LinkedIn).

Usa los mismos datos y cálculos que previa.py, así que la imagen dice lo mismo
que la página de la previa. Se ejecuta después de previa.py:
    python analisis/real-zaragoza/codigo/previa_redes.py 9
    python analisis/real-zaragoza/codigo/previa_redes.py 9 --estadio "Can Dragó (Barcelona)"

Escribe en datos/salida/:
    previa_redes.png   tarjeta de 1080 × 1350 px con los colores de la web
    previa_redes.json  las cifras de la tarjeta, para redactar los textos

La hora sale de datos/sofascore.json (en UTC) y se muestra en hora de Madrid.
Si el partido no está ahí, la tarjeta no pone hora y el JSON lo indica.
"""

import argparse
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Rectangle

import calculos
from cargar_datos import CARPETA_SALIDA, RAIZ_WEB, cargar_todo
from previa import ZARAGOZA, partidos_del_rival

# Colores de la web (los mismos de las imágenes para compartir)
FONDO = "#12221d"
TEXTO = "#f2f4ef"
SUAVE = "#9fb3a7"
VERDE_CLARO = "#a8d5b5"
NARANJA = "#ff7a2f"
LINEA = "#3b5247"
COLOR_RESULTADO = {"V": "#3f8f5a", "E": "#8a958e", "D": "#b8452a"}

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]


def hora_del_partido(jornada):
    """Inicio del partido en hora de Madrid, o None si no está en sofascore.json."""
    calendario = json.loads((RAIZ_WEB / "datos" / "sofascore.json").read_text(encoding="utf-8"))
    for p in calendario["partidos"]:
        if p["competicion"] == "Primera Federación" and p["jornada"] == jornada:
            inicio = datetime.fromisoformat(p["inicio"].replace("Z", "+00:00"))
            return inicio.astimezone(ZoneInfo("Europe/Madrid"))
    return None


def sede(partidos, donde):
    """Puntos, partidos y goles en casa o fuera."""
    p = partidos[partidos["sede"] == donde]
    return {"puntos": int(p["puntos"].sum()), "posibles": 3 * len(p), "partidos": len(p),
            "goles_favor": int(p["goles_favor"].sum()), "goles_contra": int(p["goles_contra"].sum())}


def forma(partidos, ultimos=5):
    """Últimos resultados como letras V / E / D, del más antiguo al más reciente."""
    letras = {"Victoria": "V", "Empate": "E", "Derrota": "D"}
    return "".join(letras[r] for r in partidos.tail(ultimos)["resultado"])


def cifras(jornada, estadio):
    datos = cargar_todo()
    proximo = datos["proximos"][datos["proximos"]["jornada"] == jornada]
    if proximo.empty:
        raise SystemExit(f"La jornada {jornada} no está en proximos.csv")
    proximo = proximo.iloc[0]
    nombre_rival = proximo["rival"]
    sede_zgz = proximo["sede"]
    sede_rival = "Casa" if sede_zgz == "Fuera" else "Fuera"

    zaragoza = calculos.solo_liga(calculos.preparar_partidos(datos["partidos"]))
    rival = partidos_del_rival(nombre_rival)
    clasificacion = calculos.preparar_clasificacion(datos["clasificacion"])
    corte = int(clasificacion["tras_jornada"].max()) if "tras_jornada" in clasificacion else None
    fila_z = clasificacion[clasificacion["equipo"] == ZARAGOZA].iloc[0]
    fila_r = clasificacion[clasificacion["equipo"] == nombre_rival].iloc[0]
    lider = clasificacion.sort_values("posicion").iloc[0]

    inicio = hora_del_partido(jornada)
    return {
        "jornada": jornada,
        "datos_hasta_jornada": corte,
        "local": nombre_rival if sede_zgz == "Fuera" else ZARAGOZA,
        "visitante": ZARAGOZA if sede_zgz == "Fuera" else nombre_rival,
        "rival": nombre_rival,
        "sede_zaragoza": sede_zgz,
        "inicio_madrid": inicio.isoformat() if inicio is not None else None,
        "estadio": estadio,
        "zaragoza": {"posicion": int(fila_z.posicion), "puntos": int(fila_z.puntos),
                     "goles_favor": int(fila_z.gf), "goles_contra": int(fila_z.gc),
                     "sede": sede(zaragoza, sede_zgz), "forma": forma(zaragoza)},
        "rival_datos": {"posicion": int(fila_r.posicion), "puntos": int(fila_r.puntos),
                        "goles_favor": int(fila_r.gf), "goles_contra": int(fila_r.gc),
                        "sede": sede(rival, sede_rival), "forma": forma(rival)},
        "lider": {"equipo": lider.equipo, "puntos": int(lider.puntos)},
    }


def dibujar(c, ruta):
    plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]
    fig = plt.figure(figsize=(7.2, 9), dpi=150)  # 1080 × 1350 px
    fig.patch.set_facecolor(FONDO)
    t = fig.text
    z, r = c["zaragoza"], c["rival_datos"]
    rival_corto = c["rival"]

    t(0.08, 0.925, "LÍNEA DE PASE", fontsize=13, fontweight="bold", color=TEXTO)
    t(0.08, 0.885, f"PREVIA · PRIMERA FEDERACIÓN · JORNADA {c['jornada']}",
      fontsize=11.5, fontweight="bold", color=VERDE_CLARO)
    t(0.08, 0.80, f"{c['local']} –", fontsize=34, fontweight="bold", color=TEXTO)
    t(0.08, 0.745, c["visitante"], fontsize=34, fontweight="bold", color=TEXTO)

    partes = []
    if c["inicio_madrid"]:
        inicio = datetime.fromisoformat(c["inicio_madrid"])
        partes.append(f"{DIAS[inicio.weekday()].capitalize()} {inicio.day} de {MESES[inicio.month - 1]}")
        partes.append(inicio.strftime("%H:%M"))
    if c["estadio"]:
        partes.append(c["estadio"])
    t(0.08, 0.70, " · ".join(partes), fontsize=12, color=SUAVE)
    fig.add_artist(Line2D([0.08, 0.92], [0.675, 0.675], color=LINEA, lw=1))

    def bloque(y, etiqueta, principal, secundaria):
        t(0.08, y, etiqueta, fontsize=10.5, fontweight="bold", color=NARANJA)
        t(0.08, y - 0.042, principal, fontsize=15, fontweight="bold", color=TEXTO)
        t(0.08, y - 0.075, secundaria, fontsize=13, color=SUAVE)

    diferencia = abs(z["puntos"] - r["puntos"])
    bloque(0.635, f"CLASIFICACIÓN TRAS LA J{c['datos_hasta_jornada']}",
           f"Real Zaragoza: {z['posicion']}.º, {z['puntos']} puntos ({z['goles_favor']}-{z['goles_contra']})",
           f"{rival_corto}: {r['posicion']}.º, {r['puntos']} puntos ({r['goles_favor']}-{r['goles_contra']}). "
           f"Diferencia: {diferencia} punto{'' if diferencia == 1 else 's'}")

    zs, rs = z["sede"], r["sede"]
    donde_z = "fuera" if c["sede_zaragoza"] == "Fuera" else "en casa"
    donde_r = "en casa" if c["sede_zaragoza"] == "Fuera" else "fuera"
    bloque(0.505, "SEGÚN LA SEDE",
           f"Zaragoza {donde_z}: {zs['puntos']} de {zs['posibles']} puntos ({zs['goles_favor']}-{zs['goles_contra']})",
           f"{rival_corto} {donde_r}: {rs['puntos']} de {rs['posibles']} puntos ({rs['goles_favor']}-{rs['goles_contra']})")

    t(0.08, 0.375, "ÚLTIMOS CINCO PARTIDOS", fontsize=10.5, fontweight="bold", color=NARANJA)
    for i, (equipo, letras) in enumerate([("Real Zaragoza", z["forma"]), (rival_corto, r["forma"])]):
        y = 0.315 - 0.065 * i
        t(0.08, y + 0.012, equipo, fontsize=14, fontweight="bold", color=TEXTO)
        for j, letra in enumerate(letras):
            x = 0.50 + j * 0.085
            fig.add_artist(FancyBboxPatch((x, y), 0.065, 0.045, transform=fig.transFigure,
                                          boxstyle="round,pad=0.002,rounding_size=0.008",
                                          fc=COLOR_RESULTADO[letra], ec="none"))
            t(x + 0.0325, y + 0.0225, letra, fontsize=14, fontweight="bold", color="white",
              ha="center", va="center")

    t(0.08, 0.17, "Del más antiguo al más reciente. Pocas jornadas: sirven para situar\n"
                  "el partido, no para adivinar el resultado.",
      fontsize=10.5, color=SUAVE, linespacing=1.5)
    fig.add_artist(Rectangle((0.08, 0.118), 0.06, 0.004, color=NARANJA, transform=fig.transFigure))
    fig.add_artist(Line2D([0.14, 0.92], [0.12, 0.12], color=LINEA, lw=1))
    t(0.08, 0.075, "lineadepase.com", fontsize=13, fontweight="bold", color=TEXTO)
    t(0.08, 0.045, f"Datos hasta la jornada {c['datos_hasta_jornada']}. "
                   "Fuentes: Real Zaragoza, futbolme y BeSoccer.", fontsize=9.5, color=SUAVE)

    fig.savefig(ruta, dpi=150, facecolor=FONDO)
    plt.close(fig)


def main():
    lector = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    lector.add_argument("jornada", type=int)
    lector.add_argument("--estadio", default="", help="Estadio tal como debe aparecer en la tarjeta")
    args = lector.parse_args()

    c = cifras(args.jornada, args.estadio)
    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    dibujar(c, CARPETA_SALIDA / "previa_redes.png")
    (CARPETA_SALIDA / "previa_redes.json").write_text(
        json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(c, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
