"""Exporta las variantes sociales SVG a PNG ligeros y una hoja PDF A4.

Uso: python herramientas/exportar_lamina.py
Necesita Chrome o Edge instalado y Pillow (ya usado por el generador del sitio).
"""
from __future__ import annotations

import base64
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image

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
    browser = browser_path()
    exports = [
        ('anuario-visual-2026-cuadrado', 1080, 1080),
        ('anuario-visual-2026-vertical', 1080, 1350),
        ('anuario-visual-2026-apaisado', 1200, 675),
    ]
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
            with Image.open(raw_path) as image:
                if image.size != (width, height):
                    raise RuntimeError(f'{svg_path.name}: se esperaba {width}×{height}px y llegaron {image.width}×{image.height}px')
                image.convert('RGB').save(png_path, format='PNG', optimize=True, compress_level=9)

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

    for path in [ART / f'{stem}.png' for stem, _, _ in exports] + [ART / 'anuario-visual-2026-impresion.pdf']:
        print(f'{path.name}: {path.stat().st_size:,} bytes')


if __name__ == '__main__':
    main()
