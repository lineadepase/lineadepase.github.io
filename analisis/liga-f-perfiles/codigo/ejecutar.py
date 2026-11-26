"""Punto de entrada único: de los eventos de StatsBomb a los perfiles, gráficos y textos.

    python codigo/ejecutar.py --cache <carpeta privada para los datos>

1. base.py     descarga fijada, variables por jugadora y xT neto  -> datos/salida/jugadoras_base.csv
2. perfiles.py estandarización, PCA, agrupamiento y estabilidad    -> datos/salida/jugadoras_perfiles.csv ...
3. graficos.py gráficos para web, LinkedIn, Facebook e Instagram    -> graficos/
4. web.py      página del estudio y textos de las redes

Con --solo-agrupar se parte de jugadoras_base.csv y no se descarga nada.
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import base  # noqa: E402
import graficos  # noqa: E402
import perfiles  # noqa: E402
import web  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cache', help='carpeta fuera del repositorio con los datos de StatsBomb')
    ap.add_argument('--solo-agrupar', action='store_true')
    args = ap.parse_args()
    if not args.solo_agrupar:
        if not args.cache:
            ap.error('--cache es obligatorio salvo con --solo-agrupar')
        base.construir(Path(args.cache))
    perfiles.ejecutar()
    graficos.crear_todo()
    web.main()


if __name__ == '__main__':
    main()
