"""
Portada de la previa para redes: el león de Línea de pase frente al rival.

Es la primera imagen del carrusel de Instagram; la segunda es la tarjeta de
datos de previa_redes.py. El fondo es la imagen del león facilitada por Ángel
(codigo/recursos/portada_previa.jpg, 1080 × 1350); no se usan escudos ni
logotipos de los clubes. Si falta, el script se detiene y la previa sale solo
con la tarjeta de datos.

Se ejecuta después de previa_redes.py, porque lee sus cifras:
    python analisis/real-zaragoza/codigo/previa_redes.py 9 --estadio "Can Dragó (Barcelona)"
    python analisis/real-zaragoza/codigo/previa_portada.py

Escribe datos/salida/previa_portada.png (1080 × 1350 px). La página se dibuja
en HTML y se fotografía con Chromium mediante Playwright.
"""

import base64
import json
from datetime import datetime
from html import escape
from pathlib import Path

from playwright.sync_api import sync_playwright

from cargar_datos import CARPETA_SALIDA
from previa_redes import DIAS, MESES

RECURSOS = Path(__file__).with_name("recursos")

PLANTILLA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { width: 1080px; height: 1350px; overflow: hidden; font-family: Inter, "DejaVu Sans", sans-serif;
         background: #12221d url("__FONDO__") center -80px / 1080px auto no-repeat; color: #f2f4ef; }
  .sombra-arriba { position: absolute; left: 0; right: 0; top: 0; height: 300px;
                   background: linear-gradient(#12221dcc, #12221d00); }
  .sombra-abajo { position: absolute; left: 0; right: 0; bottom: 0; height: 620px;
                  background: linear-gradient(#12221d00 0%, #12221de6 38%, #12221d 62%); }
  .cabecera { position: absolute; left: 80px; top: 70px; }
  .marca { font-size: 26px; font-weight: 700; letter-spacing: .02em; }
  .serie { margin-top: 18px; font-size: 23px; font-weight: 700; color: #a8d5b5; letter-spacing: .03em; }
  .partido { position: absolute; left: 80px; right: 80px; bottom: 190px; }
  .local, .visitante { font-weight: 800; line-height: 1.02; letter-spacing: -.02em; white-space: nowrap; }
  .local { color: #f2f4ef; }
  .visitante { color: #ff7a2f; }
  .cuando { margin-top: 22px; font-size: 32px; color: #f2f4ef; }
  .donde { margin-top: 6px; font-size: 26px; color: #9fb3a7; }
  .pie { position: absolute; left: 80px; right: 80px; bottom: 62px; }
  .raya { height: 2px; background: #3b5247; position: relative; }
  .raya::before { content: ""; position: absolute; left: 0; top: -2px; width: 80px; height: 6px; background: #ff7a2f; }
  .fila { margin-top: 22px; display: flex; justify-content: space-between; font-size: 27px; }
  .fila b { font-weight: 700; }
  .fila span { color: #9fb3a7; }
</style></head>
<body>
  <div class="sombra-arriba"></div>
  <div class="sombra-abajo"></div>
  <div class="cabecera">
    <p class="marca">LÍNEA DE PASE</p>
    <p class="serie">PREVIA · PRIMERA FEDERACIÓN · JORNADA __JORNADA__</p>
  </div>
  <div class="partido">
    <p class="local ajustar">__LOCAL__ –</p>
    <p class="visitante ajustar">__VISITANTE__</p>
    <p class="cuando">__CUANDO__</p>
    <p class="donde">__DONDE__</p>
  </div>
  <div class="pie">
    <div class="raya"></div>
    <p class="fila"><b>lineadepase.com</b><span>Desliza para ver los datos →</span></p>
  </div>
  <script>
    // Nombres largos: reduce el tamaño hasta que quepan en el ancho disponible
    const ancho = document.querySelector(".partido").clientWidth;
    let tam = 96;
    const filas = document.querySelectorAll(".ajustar");
    const cabe = () => [...filas].every(f => f.scrollWidth <= ancho);
    filas.forEach(f => f.style.fontSize = tam + "px");
    while (!cabe() && tam > 48) { tam -= 2; filas.forEach(f => f.style.fontSize = tam + "px"); }
  </script>
</body></html>
"""


def main():
    c = json.loads((CARPETA_SALIDA / "previa_redes.json").read_text(encoding="utf-8"))
    if not c["inicio_madrid"]:
        raise SystemExit("La hora del partido no está confirmada: no se genera la portada")
    inicio = datetime.fromisoformat(c["inicio_madrid"])
    cuando = f"{DIAS[inicio.weekday()].capitalize()} {inicio.day} de {MESES[inicio.month - 1]} · {inicio:%H:%M}"

    fondo = RECURSOS / "portada_previa.jpg"
    if not fondo.exists():
        raise SystemExit("Falta la imagen de fondo en codigo/recursos/portada_previa.jpg: no se genera la portada")
    fondo_uri = "data:image/jpeg;base64," + base64.b64encode(fondo.read_bytes()).decode("ascii")
    html = (PLANTILLA.replace("__JORNADA__", str(c["jornada"]))
            .replace("__FONDO__", fondo_uri)
            .replace("__LOCAL__", escape(c["local"]))
            .replace("__VISITANTE__", escape(c["visitante"]))
            .replace("__CUANDO__", escape(cuando))
            .replace("__DONDE__", escape(c["estadio"] or "")))

    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    pagina = CARPETA_SALIDA / "previa_portada.html"
    pagina.write_text(html, encoding="utf-8")
    salida = CARPETA_SALIDA / "previa_portada.png"
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        hoja = navegador.new_page(viewport={"width": 1080, "height": 1350})
        hoja.goto(pagina.resolve().as_uri())
        hoja.wait_for_timeout(300)
        hoja.screenshot(path=str(salida))
        navegador.close()
    pagina.unlink()
    print(f"Portada guardada en {salida}")


if __name__ == "__main__":
    main()
