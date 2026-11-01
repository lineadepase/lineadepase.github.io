"""
Ilustración generada con IA para las previas y los resultados (gratuita, sin cuenta).

Pide la imagen al servicio público de Pollinations (https://image.pollinations.ai),
que genera con modelos abiertos a partir de una descripción. El dominio
image.pollinations.ai tiene que estar permitido en el entorno.

Uso, desde la raíz del repositorio:
    python analisis/real-zaragoza/codigo/ilustracion_ia.py \
        --descripcion "un león con camiseta blanca y azul ..." \
        --formato vertical --salida analisis/real-zaragoza/codigo/recursos/ilustraciones/j10-vertical.jpg

Formatos: vertical (1080 × 1350, redes) y panoramica (1672 × 941, web).
Con --webp guarda además una copia .webp de menos de 600 KB para la web.

La descripción se completa siempre con el estilo de Línea de pase y con la
prohibición de texto, escudos, logotipos y personas reales. La imagen hay que
mirarla antes de usarla: el script no puede saber si tiene defectos.
"""

import argparse
import io
import random
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ESTILO = (" Editorial football illustration for a data-journalism website: night match in a big stadium "
          "with floodlights, dark green striped pitch, deep green colour palette with vivid orange accent light, "
          "cinematic lighting, high contrast, bold poster style, clean dark areas at the top and bottom for headline text. "
          "Absolutely no text, no letters, no numbers, no logos, no club crests, no badges, no watermarks, no real people.")
FORMATOS = {"vertical": (1080, 1350), "panoramica": (1672, 941)}


def generar(descripcion, ancho, alto, semilla, intentos=3):
    prompt = descripcion.strip() + ESTILO
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt) + "?"
           + urllib.parse.urlencode({"width": ancho, "height": alto, "seed": semilla,
                                     "model": "flux", "nologo": "true", "enhance": "false"}))
    ultimo = None
    for intento in range(1, intentos + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "lineadepase"}),
                                        timeout=180) as r:
                datos = r.read()
            imagen = Image.open(io.BytesIO(datos)).convert("RGB")
            return imagen
        except Exception as exc:          # servicio gratuito: puede fallar o tardar
            ultimo = exc
            time.sleep(10 * intento)
    raise SystemExit(f"No se pudo generar la ilustración: {ultimo}")


def ajustar(imagen, ancho, alto):
    """Recorta al centro y escala al tamaño exacto."""
    proporcion = ancho / alto
    w, h = imagen.size
    if w / h > proporcion:
        nuevo = int(h * proporcion)
        imagen = imagen.crop(((w - nuevo) // 2, 0, (w - nuevo) // 2 + nuevo, h))
    else:
        nuevo = int(w / proporcion)
        imagen = imagen.crop((0, (h - nuevo) // 2, w, (h - nuevo) // 2 + nuevo))
    return imagen.resize((ancho, alto), Image.LANCZOS)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--descripcion", required=True, help="Escena del partido, en inglés funciona mejor")
    p.add_argument("--formato", choices=FORMATOS, default="vertical")
    p.add_argument("--salida", required=True)
    p.add_argument("--semilla", type=int, default=None)
    p.add_argument("--webp", action="store_true")
    a = p.parse_args()
    ancho, alto = FORMATOS[a.formato]
    semilla = a.semilla if a.semilla is not None else random.randint(1, 999_999)
    imagen = ajustar(generar(a.descripcion, ancho, alto, semilla), ancho, alto)
    salida = Path(a.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    imagen.save(salida, quality=92)
    print(f"Ilustración guardada en {salida} (semilla {semilla})")
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
