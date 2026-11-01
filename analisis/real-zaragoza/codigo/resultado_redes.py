"""
Imágenes del resultado y análisis del último partido para redes y web.

Lee las cifras de datos/salida y datos/entrada y los textos editoriales de
textos/resultado_jornada.json (titular, destacados y fuentes). No usa escudos,
logotipos, fotografías ni imágenes generadas con IA: todo se dibuja con HTML
y CSS y se exporta con Chromium (Playwright).

Uso, desde la raíz del repositorio:
    python analisis/real-zaragoza/codigo/resultado_redes.py

Escribe en datos/salida/resultado/:
    resultado_1_portada.png      1080 × 1350
    resultado_2_cronologia.png   1080 × 1350
    resultado_3_numeros.png      1080 × 1350
    resultado_4_contexto.png     1080 × 1350
    resultado_5_siguiente.png    1080 × 1350
    resultado_web.png            1672 × 941 (y una copia .webp para la web)
    resultado.json               cifras y textos usados en las imágenes
"""

import json
import re
from datetime import datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from cargar_datos import CARPETA_ENTRADA, CARPETA_SALIDA, CARPETA_TEXTOS, RAIZ_WEB

ZARAGOZA = "Real Zaragoza"
FUENTES = Path(__file__).resolve().parent / "recursos" / "fuentes"
SALIDA = CARPETA_SALIDA / "resultado"
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]


def fecha_larga(fecha):
    d = pd.Timestamp(fecha)
    return f"{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]}"


def minuto_texto(minuto, anadido):
    return f"{int(minuto)}+{int(anadido)}" if int(anadido) else f"{int(minuto)}"


def datos_partido(pid):
    partidos = pd.read_csv(CARPETA_SALIDA / "partidos_liga.csv", encoding="utf-8-sig")
    p = partidos[partidos["partido_id"] == pid].iloc[0]
    casa = p["sede"] == "Casa"
    local, visitante = (ZARAGOZA, p["rival"]) if casa else (p["rival"], ZARAGOZA)
    gl, gv = (int(p["goles_favor"]), int(p["goles_contra"])) if casa else (int(p["goles_contra"]), int(p["goles_favor"]))

    goles = pd.read_csv(CARPETA_ENTRADA / "goles.csv")
    goles = goles[goles["partido_id"] == pid].copy()
    goles["orden"] = goles["minuto"] + goles["anadido"] / 100
    goles = goles.sort_values("orden")
    eventos, a_favor, en_contra = [], 0, 0
    for g in goles.itertuples():
        if g.sentido == "Favor":
            a_favor += 1
        else:
            en_contra += 1
        marcador = f"{a_favor}-{en_contra}" if casa else f"{en_contra}-{a_favor}"
        detalle = []
        if g.penalti == "si":
            detalle.append("de penalti")
        if g.propia_puerta == "si":
            detalle.append("en propia puerta")
        if isinstance(g.asistencia, str) and g.asistencia:
            detalle.append(f"pase de {g.asistencia}")
        eventos.append({"tipo": "gol", "minuto": minuto_texto(g.minuto, g.anadido), "orden": g.orden,
                        "jugador": g.jugador, "equipo": ZARAGOZA if g.sentido == "Favor" else p["rival"],
                        "propio": g.sentido == "Favor", "marcador": marcador, "detalle": ", ".join(detalle)})

    tarjetas = pd.read_csv(CARPETA_ENTRADA / "tarjetas.csv")
    rojas = tarjetas[(tarjetas["partido_id"] == pid) & tarjetas["tarjeta"].isin(["Roja", "Segunda amarilla"])]
    for t in rojas.itertuples():
        m = int(t.minuto)
        texto = f"90+{m - 90}" if m > 90 else str(m)
        eventos.append({"tipo": "roja", "minuto": texto, "orden": 90 + (m - 90) / 100 if m > 90 else m,
                        "jugador": t.jugador, "equipo": ZARAGOZA, "propio": True,
                        "detalle": "doble amarilla" if t.tarjeta == "Segunda amarilla" else "roja directa"})

    cambios = pd.read_csv(CARPETA_ENTRADA / "cambios.csv")
    cambios = cambios[cambios["partido_id"] == pid]
    por_minuto = cambios.groupby("minuto")["entra"].apply(list)
    for minuto, nombres in por_minuto.items():
        if len(nombres) >= 2:   # solo los cambios múltiples, para no saturar la cronología
            eventos.append({"tipo": "cambios", "minuto": str(int(minuto)), "orden": float(minuto),
                            "jugador": ", ".join(nombres), "equipo": ZARAGOZA, "propio": True,
                            "detalle": f"{len(nombres)} cambios a la vez"})
    eventos.sort(key=lambda e: e["orden"])

    est = pd.read_csv(CARPETA_ENTRADA / "estadisticas.csv")
    est = est[(est["partido_id"] == pid) & (est["periodo"] == "Partido") & (est["calidad"] == "ok")]
    numeros = []
    if pd.notna(p["posesion_pct"]):
        numeros.append(("Posesión", f"{int(p['posesion_pct'])} %", f"{100 - int(p['posesion_pct'])} %",
                        float(p["posesion_pct"]), 100 - float(p["posesion_pct"])))
    if pd.notna(p["tiros_zaragoza"]):
        numeros.append(("Tiros", str(int(p["tiros_zaragoza"])), str(int(p["tiros_rival"])),
                        float(p["tiros_zaragoza"]), float(p["tiros_rival"])))
    if pd.notna(p["a_puerta_zaragoza"]):
        numeros.append(("Tiros a puerta", str(int(p["a_puerta_zaragoza"])), str(int(p["a_puerta_rival"])),
                        float(p["a_puerta_zaragoza"]), float(p["a_puerta_rival"])))
    valores = {r.metrica: (r.zaragoza, r.valor_rival) for r in est.itertuples()}
    if "pases" in valores:
        z, r = valores["pases"]
        numeros.append(("Pases", str(int(z)), str(int(r)), float(z), float(r)))
        if "pases_completados" in valores:
            cz, cr = valores["pases_completados"]
            pz, pr = round(100 * cz / z), round(100 * cr / r)
            numeros.append(("Precisión en el pase", f"{pz} %", f"{pr} %", float(pz), float(pr)))

    return {"partido": p, "casa": casa, "local": local, "visitante": visitante, "gl": gl, "gv": gv,
            "eventos": eventos, "numeros": numeros}


def siguiente_partido(despues_de):
    cal = json.loads((RAIZ_WEB / "datos" / "sofascore.json").read_text(encoding="utf-8"))
    madrid = ZoneInfo("Europe/Madrid")
    for p in sorted(cal["partidos"], key=lambda x: x["inicio"]):
        inicio = datetime.fromisoformat(p["inicio"].replace("Z", "+00:00")).astimezone(madrid)
        if inicio.date() > pd.Timestamp(despues_de).date():
            return {"local": p["local"], "visitante": p["visitante"], "competicion": p["competicion"],
                    "jornada": p["jornada"], "inicio": inicio,
                    "tv": ", ".join(t["canal"] + (" (en abierto)" if t.get("abierto") else "") for t in p.get("tv", []))}
    return None


CSS = """
@font-face{font-family:Archivo;font-weight:400;src:url(FUENTES/archivo-latin-400-normal.woff2)}
@font-face{font-family:Archivo;font-weight:600;src:url(FUENTES/archivo-latin-600-normal.woff2)}
@font-face{font-family:Archivo;font-weight:700;src:url(FUENTES/archivo-latin-700-normal.woff2)}
@font-face{font-family:Archivo;font-weight:800;src:url(FUENTES/archivo-latin-800-normal.woff2)}
@font-face{font-family:Big;font-weight:700;src:url(FUENTES/big-shoulders-display-latin-700-normal.woff2)}
@font-face{font-family:Big;font-weight:800;src:url(FUENTES/big-shoulders-display-latin-800-normal.woff2)}
@font-face{font-family:Big;font-weight:900;src:url(FUENTES/big-shoulders-display-latin-900-normal.woff2)}
*{box-sizing:border-box;margin:0;padding:0}
:root{--noche:#0f3d25;--franja:#14492d;--cal:#f4f7f1;--suave:#b9cdbf;--senal:#ff6a2b;--claro:#a8d5b5;--linea:rgba(244,247,241,.18)}
body{width:WIDTHpx;height:HEIGHTpx;overflow:hidden;font-family:Archivo,sans-serif;color:var(--cal);
 background:repeating-linear-gradient(90deg,var(--noche) 0 90px,var(--franja) 90px 180px)}
.lienzo{position:relative;width:100%;height:100%;padding:72px 76px}
.campo{position:absolute;inset:40px;border:3px solid var(--linea);border-radius:6px;pointer-events:none}
.campo:before{content:"";position:absolute;left:50%;top:50%;width:300px;height:300px;margin:-150px 0 0 -150px;border:3px solid var(--linea);border-radius:50%}
.campo:after{content:"";position:absolute;left:0;right:0;top:50%;border-top:3px solid var(--linea)}
.velo{position:absolute;inset:0;background:linear-gradient(180deg,rgba(9,30,18,.55),rgba(9,30,18,.88))}
.contenido{position:relative;height:100%;display:flex;flex-direction:column}
.etiqueta{font-weight:700;font-size:25px;letter-spacing:.2em;text-transform:uppercase;color:var(--claro)}
.etiqueta b{color:var(--senal)}
.pie{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:22px;color:var(--suave);border-top:2px solid var(--linea);padding-top:22px}
.pie strong{color:var(--cal);font-size:26px;letter-spacing:.02em}
.titulo{font-family:Big;font-weight:900;text-transform:uppercase;line-height:.92;letter-spacing:.005em;text-wrap:balance}
.barra{width:120px;height:10px;background:var(--senal);border-radius:5px}
"""


def sin_corte(texto):
    """Escapa el texto y evita que un marcador como 2-2 se parta en dos líneas."""
    return re.sub(r"(\d+-\d+)", r'<span style="white-space:nowrap">\1</span>', escape(texto))


def con_ilustracion(extra, t, clave):
    """Si textos/resultado_jornada.json trae una ilustración (ruta desde la raíz del repositorio),
    la usa de fondo con un velo oscuro para que el marcador y el titular se lean bien."""
    ruta = t.get(clave)
    if not ruta:
        return extra
    imagen = (RAIZ_WEB / ruta).resolve()
    if not imagen.is_file():
        raise SystemExit(f"No existe la ilustración {ruta}")
    return extra + f"""
body{{background:#0b1d13 url({imagen.as_uri()}) center/cover no-repeat}}
.campo{{display:none}}
.velo{{background:linear-gradient(180deg,rgba(7,22,14,.6) 0%,rgba(7,22,14,.08) 26%,rgba(7,22,14,.08) 50%,rgba(7,22,14,.88) 72%,rgba(7,22,14,.96) 100%)}}
body{{filter:saturate(1.15)}}
.goles,.equipo,.titular{{text-shadow:0 4px 24px rgba(0,0,0,.85),0 0 4px rgba(0,0,0,.5)}}
"""


def pagina(cuerpo, ancho=1080, alto=1350, extra=""):
    css = CSS.replace("FUENTES", FUENTES.as_uri()).replace("WIDTH", str(ancho)).replace("HEIGHT", str(alto))
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{css}{extra}</style></head>
<body><div class="lienzo"><div class="campo"></div><div class="velo"></div><div class="contenido">{cuerpo}</div></div></body></html>"""


def pie(fuentes):
    return f'<div class="pie"><span><strong>Línea de pase</strong><br>lineadepase.com</span><span style="text-align:right;max-width:620px">{escape(fuentes)}</span></div>'


def portada(d, t, cab):
    goles = [e for e in d["eventos"] if e["tipo"] == "gol"]
    def lista(equipo):
        return "<br>".join(f"{escape(e['jugador'])} {e['minuto']}'" for e in goles if e["equipo"] == equipo) or "—"
    extra = """
.velo{background:radial-gradient(circle at 50% 36%,rgba(255,106,43,.28),rgba(255,106,43,0) 42%),linear-gradient(180deg,rgba(9,30,18,.45),rgba(9,30,18,.9))}
.equipo{font-family:Big;font-weight:900;font-size:112px;text-transform:uppercase;line-height:.9}
.equipo.der{text-align:right}
.goles{font-family:Big;font-weight:900;font-size:330px;line-height:.78;display:flex;justify-content:center;align-items:center;gap:34px;margin:22px 0 16px;text-shadow:0 8px 40px rgba(0,0,0,.35)}
.goles i{font-style:normal;color:var(--senal);font-size:200px}
.autores{display:grid;grid-template-columns:1fr 1fr;gap:30px;font-size:26px;color:var(--suave);line-height:1.45;margin-top:26px}
.autores div:last-child{text-align:right}
.autores b{color:var(--cal);font-weight:700}
.titular{margin-top:20px;font-size:84px}
.sub{margin-top:18px;font-size:31px;line-height:1.35;color:var(--cal);max-width:900px}
.lugar{margin-top:16px;margin-bottom:26px;font-size:26px;color:var(--claro);font-weight:600}
"""
    cuerpo = f"""<p class="etiqueta">{escape(cab)}</p>
<div class="equipo" style="margin-top:38px">{escape(d['local'])}</div>
<div class="goles">{d['gl']}<i>–</i>{d['gv']}</div>
<div class="equipo der">{escape(d['visitante'])}</div>
<div class="autores"><div><b>{escape(d['local'])}</b><br>{lista(d['local'])}</div><div><b>{escape(d['visitante'])}</b><br>{lista(d['visitante'])}</div></div>
<div class="barra" style="margin-top:34px"></div>
<h1 class="titulo titular">{sin_corte(t['titular'])}</h1>
<p class="sub">{sin_corte(t['subtitulo'])}</p>
<p class="lugar">{escape(fecha_larga(d['partido']['fecha']).capitalize())} · {escape(t['estadio'])}</p>
{pie(t['fuentes'])}"""
    extra = con_ilustracion(extra, t, "ilustracion")
    return pagina(cuerpo, extra=extra)


def cartel(d, t, cab, panoramica=False):
    """Portada con la ilustración a la vista: el texto ocupa una franja (arriba en vertical,
    a la izquierda en la web) y deja ver la escena del partido."""
    clave = "ilustracion_web" if panoramica else "ilustracion"
    imagen = (RAIZ_WEB / t[clave]).resolve()
    if not imagen.is_file():
        raise SystemExit(f"No existe la ilustración {t[clave]}")
    if panoramica:
        extra = f"""
.lienzo{{padding:64px 84px}}
body{{background:#0b1d13 url({imagen.as_uri()}) center/cover no-repeat}}
.campo{{display:none}}
.velo{{background:linear-gradient(90deg,rgba(7,22,14,.94) 0%,rgba(7,22,14,.82) 30%,rgba(7,22,14,0) 46%),linear-gradient(0deg,rgba(7,22,14,.85) 0%,rgba(7,22,14,0) 16%)}}
.bloque{{width:600px;margin-top:40px}}
.equipo{{font-family:Big;font-weight:900;font-size:78px;text-transform:uppercase;line-height:.95}}
.goles{{font-family:Big;font-weight:900;font-size:190px;line-height:.85;margin:14px 0;white-space:nowrap}}
.goles i{{font-style:normal;color:var(--senal);font-size:110px;margin:0 14px;vertical-align:middle}}
.titular{{margin-top:34px;font-size:64px}}
.lugar{{margin-top:16px;font-size:26px;color:var(--claro);font-weight:600}}
.pie{{font-size:20px}}
"""
        cuerpo = f"""<p class="etiqueta">{escape(cab)}</p>
<div class="bloque"><div class="equipo">{escape(d['local'])}</div>
<div class="goles">{d['gl']}<i>–</i>{d['gv']}</div>
<div class="equipo">{escape(d['visitante'])}</div>
<h1 class="titulo titular">{sin_corte(t['titular'])}</h1>
<p class="lugar">{escape(fecha_larga(d['partido']['fecha']).capitalize())} · {escape(t['estadio'])}</p></div>
<div style="flex:1"></div>{pie(t['fuentes'] + ' · Ilustración creada con IA')}"""
        return pagina(cuerpo, 1672, 941, extra)
    extra = f"""
body{{background:#0b1d13 url({imagen.as_uri()}) center/cover no-repeat}}
.campo{{display:none}}
.velo{{background:linear-gradient(180deg,rgba(7,22,14,.95) 0%,rgba(7,22,14,.85) 22%,rgba(7,22,14,0) 40%,rgba(7,22,14,0) 86%,rgba(7,22,14,.9) 100%)}}
.marcador{{display:flex;align-items:center;justify-content:space-between;gap:24px;margin-top:26px}}
.equipo{{font-family:Big;font-weight:900;font-size:66px;text-transform:uppercase;line-height:.95;width:330px}}
.equipo.der{{text-align:right}}
.goles{{font-family:Big;font-weight:900;font-size:150px;line-height:.85;white-space:nowrap}}
.goles i{{font-style:normal;color:var(--senal);font-size:90px;margin:0 10px;vertical-align:middle}}
.titular{{margin-top:22px;font-size:62px;text-align:center}}
"""
    cuerpo = f"""<p class="etiqueta" style="text-align:center">{escape(cab)}</p>
<div class="marcador"><div class="equipo">{escape(d['local'])}</div><div class="goles">{d['gl']}<i>–</i>{d['gv']}</div>
<div class="equipo der">{escape(d['visitante'])}</div></div>
<h1 class="titulo titular">{sin_corte(t['titular'])}</h1>
<div style="flex:1"></div>{pie(t['fuentes'] + ' · Ilustración creada con IA')}"""
    return pagina(cuerpo, extra=extra)


def cronologia(d, t, cab):
    extra = """
.lista{margin-top:40px;position:relative;padding-left:190px;flex:1;display:flex;flex-direction:column;justify-content:center;gap:22px}
.lista:before{content:"";position:absolute;left:152px;top:10px;bottom:10px;width:4px;background:var(--linea)}
.ev{position:relative;background:rgba(244,247,241,.07);border:2px solid var(--linea);border-radius:18px;padding:18px 26px}
.ev .min{position:absolute;left:-190px;top:50%;transform:translateY(-50%);width:120px;text-align:right;font-family:Big;font-weight:900;font-size:50px}
.ev:after{content:"";position:absolute;left:-46px;top:50%;width:24px;height:24px;margin-top:-12px;border-radius:50%;background:var(--suave)}
.ev.propio{border-color:rgba(255,106,43,.75)}
.ev.propio:after{background:var(--senal)}
.ev.roja:after{background:#e23b3b;border-radius:4px}
.ev h3{font-size:34px;font-weight:800;display:flex;justify-content:space-between;gap:20px}
.ev h3 span{font-family:Big;font-weight:900;font-size:44px;color:var(--senal)}
.ev p{margin-top:6px;font-size:24px;color:var(--suave)}
"""
    filas = []
    for e in d["eventos"]:
        clase = "ev" + (" propio" if e["propio"] and e["tipo"] == "gol" else "") + (" roja" if e["tipo"] == "roja" else "")
        if e["tipo"] == "gol":
            h = f"Gol de {escape(e['jugador'])} <span>{e['marcador']}</span>"
            p = escape(e["equipo"] + (f" · {e['detalle']}" if e["detalle"] else ""))
        elif e["tipo"] == "roja":
            h = f"Expulsión de {escape(e['jugador'])}"
            p = escape(f"{e['equipo']} · {e['detalle']}")
        else:
            h = "Triple cambio" if e["detalle"].startswith("3") else escape(e["detalle"].capitalize())
            p = escape(f"Entran {e['jugador']}")
        filas.append(f'<div class="{clase}"><span class="min">{e["minuto"]}\'</span><h3>{h}</h3><p>{p}</p></div>')
    cuerpo = f"""<p class="etiqueta">{escape(cab)}</p>
<h2 class="titulo" style="font-size:96px;margin-top:22px">Cómo se movió<br>el marcador</h2>
<div class="lista">{''.join(filas)}</div>{pie(t['fuentes'])}"""
    return pagina(cuerpo, extra=extra)


def numeros(d, t, cab):
    extra = """
.cab{display:flex;justify-content:space-between;margin-top:40px;font-size:30px;font-weight:800}
.cab span:last-child{color:var(--suave)}
.fila{margin-top:28px}
.fila p{text-align:center;font-size:26px;color:var(--suave);font-weight:600;letter-spacing:.06em;text-transform:uppercase}
.par{display:grid;grid-template-columns:150px 1fr 150px;align-items:center;gap:20px;margin-top:12px}
.par b{font-family:Big;font-weight:900;font-size:62px}
.par b:last-child{text-align:right;color:var(--suave)}
.pista{display:flex;height:26px;border-radius:13px;overflow:hidden;background:rgba(244,247,241,.12)}
.pista i{display:block;background:var(--senal)}
.pista u{display:block;background:var(--suave);opacity:.55}
.nota{margin-top:30px;margin-bottom:24px;font-size:23px;color:var(--suave);line-height:1.45}
"""
    filas = []
    for nombre, tz, tr, vz, vr in d["numeros"]:
        total = (vz + vr) or 1
        filas.append(f'<div class="fila"><p>{escape(nombre)}</p><div class="par"><b>{escape(tz)}</b>'
                     f'<div class="pista"><i style="width:{100 * vz / total:.1f}%"></i><u style="width:{100 * vr / total:.1f}%"></u></div>'
                     f'<b>{escape(tr)}</b></div></div>')
    rival = d["partido"]["rival"]
    cuerpo = f"""<p class="etiqueta">{escape(cab)}</p>
<h2 class="titulo" style="font-size:96px;margin-top:22px">Los números<br>del partido</h2>
<div class="cab"><span style="color:var(--senal)">{ZARAGOZA}</span><span>{escape(rival)}</span></div>
{''.join(filas)}<p class="nota">{escape(t['nota_estadisticas'])}</p>{pie(t['fuentes'])}"""
    return pagina(cuerpo, extra=extra)


def contexto(d, t, cab):
    extra = """
.rejilla{margin-top:56px;display:grid;grid-template-columns:1fr 1fr;gap:26px;flex:1;align-content:center}
.dato{background:rgba(244,247,241,.07);border:2px solid var(--linea);border-radius:20px;padding:34px 30px;min-height:330px;display:flex;flex-direction:column}
.dato b{font-family:Big;font-weight:900;font-size:110px;line-height:.9;color:var(--senal)}
.dato p{margin-top:auto;font-size:29px;line-height:1.35;font-weight:600}
"""
    datos = "".join(f'<div class="dato"><b>{escape(x["cifra"])}</b><p>{escape(x["texto"])}</p></div>' for x in t["destacados"])
    cuerpo = f"""<p class="etiqueta">{escape(cab)}</p>
<h2 class="titulo" style="font-size:96px;margin-top:22px">Lo que deja<br>la jornada</h2>
<div class="rejilla">{datos}</div>{pie(t['fuentes'])}"""
    return pagina(cuerpo, extra=extra)


def siguiente(d, t, cab, s):
    extra = """
.caja{margin:auto 0;padding:56px 50px;border:3px solid var(--senal);border-radius:26px;background:rgba(9,30,18,.55)}
.caja .equipos{font-family:Big;font-weight:900;font-size:118px;line-height:.95;text-transform:uppercase;margin-top:26px}
.caja .equipos span{color:var(--senal)}
.caja .cuando{margin-top:40px;font-size:40px;font-weight:800}
.caja .donde{margin-top:12px;font-size:30px;color:var(--suave)}
"""
    if s is None:
        return None
    comp = s["competicion"] + (f" · Jornada {s['jornada']}" if s["jornada"] else "")
    hora = s["inicio"].strftime("%H:%M")
    lugar = t["estadio"] if s["local"] == ZARAGOZA else ""
    donde = " · ".join(x for x in [lugar, s["tv"]] if x)
    cuerpo = f"""<p class="etiqueta">{escape(cab)}</p>
<div class="caja"><p class="etiqueta">Próximo partido · {escape(comp)}</p>
<p class="equipos">{escape(s['local'])}<br><span>–</span><br>{escape(s['visitante'])}</p>
<p class="cuando">{escape(fecha_larga(s['inicio']).capitalize())} · {hora} h</p>
<p class="donde">{escape(donde) if donde else 'Hora peninsular'}</p></div>{pie(t['fuentes'])}"""
    return pagina(cuerpo, extra=extra)


def web(d, t, cab):
    goles = [e for e in d["eventos"] if e["tipo"] == "gol"]
    def lista(equipo):
        return " · ".join(f"{escape(e['jugador'])} {e['minuto']}'" for e in goles if e["equipo"] == equipo) or "—"
    extra = """
.lienzo{padding:64px 84px}
.velo{background:radial-gradient(circle at 50% 34%,rgba(255,106,43,.26),rgba(255,106,43,0) 40%),linear-gradient(180deg,rgba(9,30,18,.45),rgba(9,30,18,.9))}
.fila{display:flex;align-items:center;justify-content:space-between;margin-top:46px}
.equipo{font-family:Big;font-weight:900;font-size:92px;text-transform:uppercase;width:520px;line-height:.95}
.equipo.der{text-align:right}
.goles{font-family:Big;font-weight:900;font-size:280px;line-height:.8;white-space:nowrap}
.goles i{font-style:normal;color:var(--senal);font-size:150px;margin:0 18px;vertical-align:middle}
.autores{display:flex;justify-content:space-between;margin-top:26px;font-size:26px;color:var(--suave)}
.titular{margin-top:70px;font-size:96px;text-align:center}
.lugar{margin-top:18px;text-align:center;font-size:30px;color:var(--claro);font-weight:600}
.pie{font-size:20px}
"""
    cuerpo = f"""<p class="etiqueta" style="text-align:center">{escape(cab)}</p>
<div class="fila"><div class="equipo">{escape(d['local'])}</div><div class="goles">{d['gl']}<i>–</i>{d['gv']}</div>
<div class="equipo der">{escape(d['visitante'])}</div></div>
<div class="autores"><span>{lista(d['local'])}</span><span>{lista(d['visitante'])}</span></div>
<h1 class="titulo titular">{sin_corte(t['titular'])}</h1>
<p class="lugar">{escape(fecha_larga(d['partido']['fecha']).capitalize())} · {escape(t['estadio'])}</p>{pie(t['fuentes'])}"""
    extra = con_ilustracion(extra, t, "ilustracion_web")
    return pagina(cuerpo, 1672, 941, extra)


def main():
    from playwright.sync_api import sync_playwright
    t = json.loads((CARPETA_TEXTOS / "resultado_jornada.json").read_text(encoding="utf-8"))
    d = datos_partido(t["partido_id"])
    p = d["partido"]
    cab = (f"{p['competicion']} · Jornada {int(p['jornada'])}" if pd.notna(p["jornada"])
           else str(p["competicion"])) + f" · {pd.Timestamp(p['fecha']).day} {MESES[pd.Timestamp(p['fecha']).month - 1][:3]}"
    s = siguiente_partido(p["fecha"])
    con_ia = bool(t.get("ilustracion")) and bool(t.get("ilustracion_web"))
    piezas = [("resultado_1_portada", cartel(d, t, cab) if con_ia else portada(d, t, cab)), ("resultado_2_cronologia", cronologia(d, t, cab)),
              ("resultado_3_numeros", numeros(d, t, cab)), ("resultado_4_contexto", contexto(d, t, cab)),
              ("resultado_5_siguiente", siguiente(d, t, cab, s)), ("resultado_web", cartel(d, t, cab, True) if con_ia else web(d, t, cab))]
    SALIDA.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        navegador = pw.chromium.launch()
        for nombre, html in piezas:
            if html is None:
                continue
            ancho, alto = (1672, 941) if nombre == "resultado_web" else (1080, 1350)
            ruta_html = SALIDA / f"{nombre}.html"
            ruta_html.write_text(html, encoding="utf-8")
            pagina_nav = navegador.new_page(viewport={"width": ancho, "height": alto})
            pagina_nav.goto(ruta_html.as_uri())
            pagina_nav.evaluate("document.fonts.ready")
            pagina_nav.wait_for_timeout(300)
            pagina_nav.screenshot(path=str(SALIDA / f"{nombre}.png"))
            pagina_nav.close()
            ruta_html.unlink()
        navegador.close()
    from PIL import Image
    Image.open(SALIDA / "resultado_web.png").convert("RGB").save(SALIDA / "resultado_web.webp", quality=86)
    resumen = {"partido_id": t["partido_id"], "local": d["local"], "visitante": d["visitante"],
               "marcador": f"{d['gl']}-{d['gv']}", "fecha": str(p["fecha"]),
               "eventos": [{k: v for k, v in e.items() if k != "orden"} for e in d["eventos"]],
               "numeros": [{"metrica": n[0], "zaragoza": n[1], "rival": n[2]} for n in d["numeros"]],
               "siguiente": None if s is None else {**{k: v for k, v in s.items() if k != "inicio"},
                                                    "inicio": s["inicio"].isoformat()},
               "textos": t}
    (SALIDA / "resultado.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Imágenes del resultado en", SALIDA)


if __name__ == "__main__":
    main()
