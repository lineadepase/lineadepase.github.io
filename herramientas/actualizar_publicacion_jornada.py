"""Sincroniza las páginas y el marcador gráfico tras actualizar los datos de liga.

Uso independiente: python herramientas/actualizar_publicacion_jornada.py
El proceso requiere Chrome o Edge para renderizar los PNG desde el SVG.
"""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def main() -> None:
    run(str(ROOT / 'herramientas' / 'actualizar_seo.py'))
    run(str(ROOT / 'herramientas' / 'exportar_lamina.py'), '--solo-jornada', '--archivo-jornadas')
    run(str(ROOT / 'herramientas' / 'verificar_marcador_visual.py'))


if __name__ == '__main__':
    main()
