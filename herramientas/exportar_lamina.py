"""Exporta las variantes sociales SVG a PNG ligeros y una hoja PDF A4.

Uso: python herramientas/exportar_lamina.py
Necesita Chrome o Edge instalado y Pillow (ya usado por el generador del sitio).
"""
from __future__ import annotations

import base64
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from segunda_edicion import match_statistics

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets' / 'ilustraciones'


def browser_path() -> Path:
    candidates = [
        os.environ.get('CHROME_PATH'),
        shutil.which('chrome'),
        shutil.which('msedge'),
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/usr/bin/google-chrome',
        '/usr/bin/chromium',
        '/usr/bin/microsoft-edge',
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return Path(candidate)
    raise RuntimeError('Instala Chrome o Edge, o define CHROME_PATH para exportar los gráficos.')


def run_browser(browser: Path, profile: Path, *args: str) -> None:
    command = [
        str(browser), '--headless=new', '--disable-gpu', '--hide-scrollbars',
        '--no-first-run', '--no-default-browser-check', '--disable-extensions',
        f'--user-data-dir={profile}', *args,
    ]
    subprocess.run(command, check=True, timeout=90, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solo-jornada', action='store_true', help='Regenera únicamente los dos PNG del marcador más reciente.')
    parser.add_argument('--archivo-jornadas', action='store_true', help='Exporta PNG ligeros de cada jornada archivada y de las métricas validadas.')
    args = parser.parse_args()
    browser = browser_path()
    exports = [] if args.solo_jornada else [
        ('anuario-visual-2026-cuadrado', 1080, 1080),
        ('anuario-visual-2026-vertical', 1080, 1350),
        ('anuario-visual-2026-apaisado', 1200, 675),
    ]
    exports += [
        ('resultado-real-zaragoza-ultima-jornada', 1200, 630),
        ('resultado-real-zaragoza-ultima-jornada-cuadrado', 1080, 1080),
    ]
    stats_svg = ART / 'estadisticas-real-zaragoza-ultima-jornada.svg'
    stats_png = ART / 'estadisticas-real-zaragoza-ultima-jornada.png'
    data = json.loads((ROOT / 'datos' / 'zaragoza.json').read_text(encoding='utf-8'))
    archive_exports = []
    if args.archivo_jornadas:
        for record in data['partidos']:
            round_name = f'jornada-{int(record["jornada"]):02d}'
            archive_exports.append((record, ART / 'archivo-jornadas' / f'{round_name}.svg', ART / 'archivo-jornadas' / f'{round_name}.png', None))
            archived_stats = match_statistics(record, next((row for row in data.get('fichas', []) if str(row.get('partido_id')) == str(record.get('partido_id'))), None))
            if archived_stats:
                archive_exports.append((record, ART / 'estadisticas-jornadas' / f'{round_name}.svg', ART / 'estadisticas-jornadas' / f'{round_name}.png', archived_stats))
    latest = max(data['partidos'], key=lambda row: int(row['jornada']))
    fixture = next((row for row in data.get('fichas', []) if str(row.get('partido_id')) == str(latest.get('partido_id'))), None)
    match_stats = match_statistics(latest, fixture)
    if match_stats and stats_svg.is_file():
        exports.append(('estadisticas-real-zaragoza-ultima-jornada', 1200, 630))
    elif stats_png.exists():
        stats_png.unlink()
    with tempfile.TemporaryDirectory(prefix='linea-pase-export-') as temp:
        folder = Path(temp)
        profile = folder / 'perfil-chrome'
        for stem, width, height in exports:
            svg_path = ART / f'{stem}.svg'
            png_path = ART / f'{stem}.png'
            raw_path = folder / f'{stem}-raw.png'
            run_browser(browser, profile, '--force-device-scale-factor=1',
                        f'--window-size={width},{height}', f'--screenshot={raw_path}',
                        svg_path.resolve().as_uri())
            metadata = None
            if stem.startswith(('resultado-real-zaragoza-ultima-jornada', 'estadisticas-real-zaragoza-ultima-jornada')):
                metadata = PngInfo()
                metadata.add_text('jornada', str(latest['jornada']))
                metadata.add_text('fecha_partido', latest['fecha'])
                if stem.startswith('estadisticas-'):
                    metadata.add_text('posesion_pct', str(latest['posesion_pct']))
                    metadata.add_text('tiros_zaragoza', str(int(latest['tiros_zaragoza'])))
                    metadata.add_text('tiros_rival', str(int(latest['tiros_rival'])))
                    if 'a_puerta_zaragoza' in match_stats:
                        metadata.add_text('a_puerta_zaragoza', str(match_stats['a_puerta_zaragoza']))
                        metadata.add_text('a_puerta_rival', str(match_stats['a_puerta_rival']))
            with Image.open(raw_path) as image:
                if image.size != (width, height):
                    raise RuntimeError(f'{svg_path.name}: se esperaba {width}×{height}px y llegaron {image.width}×{image.height}px')
                image.convert('RGB').save(png_path, format='PNG', optimize=True, compress_level=9, pnginfo=metadata)

        for record, svg_path, png_path, archived_stats in archive_exports:
            raw_path = folder / f'{png_path.stem}-raw.png'
            run_browser(browser, profile, '--force-device-scale-factor=1', '--window-size=1200,630',
                        f'--screenshot={raw_path}', svg_path.resolve().as_uri())
            metadata = PngInfo()
            metadata.add_text('jornada', str(record['jornada']))
            metadata.add_text('fecha_partido', record['fecha'])
            metadata.add_text('rival', record['rival'])
            metadata.add_text('resultado', f"{record['goles_favor']}–{record['goles_contra']}")
            if archived_stats:
                metadata.add_text('posesion_pct', str(archived_stats['posesion_pct']))
                metadata.add_text('tiros_zaragoza', str(archived_stats['tiros_zaragoza']))
                metadata.add_text('tiros_rival', str(archived_stats['tiros_rival']))
                if 'a_puerta_zaragoza' in archived_stats:
                    metadata.add_text('a_puerta_zaragoza', str(archived_stats['a_puerta_zaragoza']))
                    metadata.add_text('a_puerta_rival', str(archived_stats['a_puerta_rival']))
            with Image.open(raw_path) as image:
                if image.size != (1200, 630):
                    raise RuntimeError(f'{svg_path.name}: se esperaba 1200×630px y llegaron {image.width}×{image.height}px')
                image.convert('RGB').save(png_path, format='PNG', optimize=True, compress_level=9, pnginfo=metadata)
        if args.archivo_jornadas:
            expected_archive_pngs = {path.name for _, _, path, _ in archive_exports}
            for folder_name in ('archivo-jornadas', 'estadisticas-jornadas'):
                for stale in (ART / folder_name).glob('jornada-*.png'):
                    if stale.name not in expected_archive_pngs:
                        stale.unlink()

        if not args.solo_jornada:
            source = (ART / 'anuario-visual-2026-vertical.svg').read_bytes()
            encoded = base64.b64encode(source).decode('ascii')
            printable = folder / 'lamina-a4.html'
            printable.write_text(
                '<!doctype html><meta charset="utf-8"><style>'
                '@page{size:A4;margin:0}*{box-sizing:border-box}html,body{margin:0;width:210mm;height:297mm}'
                'body{display:grid;place-items:center;background:#fff}'
                'img{display:block;width:200mm;height:250mm;object-fit:contain;print-color-adjust:exact}'
                '</style><img alt="Línea de pase, cuaderno visual 2026" '
                f'src="data:image/svg+xml;base64,{encoded}">', encoding='utf-8')
            pdf_path = ART / 'anuario-visual-2026-impresion.pdf'
            run_browser(browser, profile, '--no-pdf-header-footer', f'--print-to-pdf={pdf_path}',
                        printable.resolve().as_uri())

    paths=[ART / f'{stem}.png' for stem, _, _ in exports]
    if not args.solo_jornada:
        paths.append(ART / 'anuario-visual-2026-impresion.pdf')
    for path in paths:
        print(f'{path.name}: {path.stat().st_size:,} bytes')
    for _, _, path, _ in archive_exports:
        print(f'{path.relative_to(ART)}: {path.stat().st_size:,} bytes')


if __name__ == '__main__':
    main()
