"""
Ilustración generada con IA para las previas y los resultados (gratuita).

Pide la imagen a Pollinations a partir de una descripción escrita para cada partido.
Con la variable de entorno POLLINATIONS_KEY (clave gratuita de https://enter.pollinations.ai)
usa gen.pollinations.ai y un modelo de calidad (por defecto zimage). Sin clave usa el
servicio anónimo image.pollinations.ai, de calidad mucho menor. El dominio usado tiene
que estar permitido en el entorno. La clave no se guarda nunca en el repositorio.

Cada partido lleva su propia idea visual, sacada de lo que pasó (resultado) o de lo que
está en juego (previa), y distinta de la idea de la imagen de su previa. Los colores y
símbolos contrastados de cada rival están en textos/temas_ilustracion.json.

Uso, desde la raíz del repositorio:
    python analisis/real-zaragoza/codigo/ilustracion_ia.py \
        --descripcion "a giant hourglass on a floodlit football pitch ..." \
        --formato vertical --salida analisis/real-zaragoza/codigo/recursos/ilustraciones/j10-vertical.jpg
Conviene probar varias semillas, de una en una, y quedarse con la mejor.

Formatos: vertical (1080 × 1350, redes) y panoramica (1672 × 941, web).
Con --webp guarda además una copia .webp de menos de 600 KB para la web.

La descripción se completa con la prohibición de texto, escudos, logotipos y personas
reales. La imagen hay que mirarla antes de usarla: el script no puede saber si tiene defectos.
"""

import argparse
import io
import os
import random
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ESTILO = (" Highly detailed cinematic digital illustration, vivid colours, dramatic lighting, sharp focus, "
          "clear readable main subject, darker area at the bottom for headline text. "
          "No text, no letters, no numbers, no logos, no club crests, no badges, no watermarks, no real people.")
FORMATOS = {"vertical": (1080, 1350), "panoramica": (1672, 941)}


def generar(descripcion, ancho, alto, semilla, modelo, intentos=3):
    prompt = urllib.parse.quote(descripcion.strip() + ESTILO)
    clave = os.environ.get("POLLINATIONS_KEY", "").strip()
    parametros = {"width": ancho, "height": alto, "seed": semilla, "nologo": "true"}
    cabeceras = {"User-Agent": "lineadepase"}
    if clave:
        url = f"https://gen.pollinations.ai/image/{prompt}?" + urllib.parse.urlencode({**parametros, "model": modelo})
        cabeceras["Authorization"] = f"Bearer {clave}"
    else:
        url = f"https://image.pollinations.ai/prompt/{prompt}?" + urllib.parse.urlencode(
            {**parametros, "model": "flux", "enhance": "false"})
    ultimo = None
    for intento in range(1, intentos + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=cabeceras), timeout=240) as r:
                datos = r.read()
            return Image.open(io.BytesIO(datos)).convert("RGB"), bool(clave)
        except Exception as exc:          # servicio gratuito: puede fallar o tardar
            ultimo = exc
            time.sleep(15 * intento)
    raise SystemExit(f"No se pudo generar la ilustración: {ultimo}")


def ajustar(imagen, ancho, alto, con_marca):
    """Quita la franja inferior si trae la marca del servicio anónimo, recorta al centro y escala."""
    proporcion = ancho / alto
    w, h = imagen.size
    if con_marca:
        h = int(h * 0.92)
        imagen = imagen.crop((0, 0, w, h))
    if w / h > proporcion:
        nuevo = int(h * proporcion)
        imagen = imagen.crop(((w - nuevo) // 2, 0, (w - nuevo) // 2 + nuevo, h))
    else:
        nuevo = int(w / proporcion)
        imagen = imagen.crop((0, (h - nuevo) // 2, w, (h - nuevo) // 2 + nuevo))
    return imagen.resize((ancho, alto), Image.LANCZOS)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--descripcion", required=True, help="Escena del partido, en inglés")
    p.add_argument("--formato", choices=FORMATOS, default="vertical")
    p.add_argument("--salida", required=True)
    p.add_argument("--semilla", type=int, default=None)
    p.add_argument("--modelo", default="zimage", help="Modelo de gen.pollinations.ai (solo con clave)")
    p.add_argument("--webp", action="store_true")
    a = p.parse_args()
    ancho, alto = FORMATOS[a.formato]
    semilla = a.semilla if a.semilla is not None else random.randint(1, 999_999)
    imagen, con_clave = generar(a.descripcion, ancho, alto, semilla, a.modelo)
    imagen = ajustar(imagen, ancho, alto, con_marca=not con_clave)
    salida = Path(a.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    imagen.save(salida, quality=92)
    print(f"Ilustración guardada en {salida} (semilla {semilla}, {'con clave' if con_clave else 'sin clave'})")
    if a.webp:
        calidad = 86
        ruta = salida.with_suffix(".webp")
        while True:
            imagen.save(ruta, quality=calidad)
            if ruta.stat().st_size < 600_000 or calidad <= 50:
                break
            calidad -= 8
        print(f"Copia web en {ruta} ({ruta.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    sys.exit(main())
