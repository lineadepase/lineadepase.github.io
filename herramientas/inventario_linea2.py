"""Inventario de rutas existentes para cerrar Línea de Pase 2.0, sin modificar la web."""
from collections import Counter
import csv
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'documentacion'


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.head = False
        self.title = False
        self.name = ''
        self.canonical = ''
        self.robots = ''
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'head':
            self.head = True
        if tag == 'title' and self.head:
            self.title = True
        if self.head and tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href', '')
        if self.head and tag == 'meta' and attrs.get('name') == 'robots':
            self.robots = attrs.get('content', '')
        if tag == 'script' and attrs.get('src'):
            self.scripts.append(attrs['src'])

    def handle_endtag(self, tag):
        if tag == 'title':
            self.title = False
        if tag == 'head':
            self.head = False

    def handle_data(self, data):
        if self.title:
            self.name += data


def area(path):
    first = path.split('/')[0]
    if first == 'datalab-prototipo':
        return 'Prototipo'
    if path.startswith('proyectos/real-zaragoza/') or first in {
        'comparador', 'mapa-grupo', 'datos-en-revision', 'tras-la-jornada'
    }:
        return 'Zaragoza'
    if first in {'marcador-a-ciegas', 'partidos-espejo', 'reloj-del-marcador',
                 'balance-de-preguntas', 'preguntas-del-partido',
                 'mapa-de-lo-que-cambio', 'esquemas-del-juego'}:
        return 'Play'
    if first in {'archivo-visual', 'pizarron-de-una-jugada'}:
        return 'Studio'
    if first == 'galeria-visual' or path.startswith('proyectos/espana-eurocopa-redes/'):
        return 'Museo'
    if path.startswith(('proyectos/liga-f-', 'proyectos/futbol-femenino/', 'proyectos/xg/')) or first == 'conceptos':
        return 'DataLab'
    if first in {'videos', 'archivo', 'novedades'}:
        return 'Media'
    if first in {'seleccion', 'herramientas'} or path == 'proyectos/index.html':
        return 'Pro'
    return 'Transversal'


def build():
    sitemap = {node.text for node in ET.parse(ROOT / 'sitemap.xml').iter()
               if node.tag.endswith('}loc')}
    records = []
    for path in sorted(ROOT.rglob('*.html')):
        relative = path.relative_to(ROOT)
        if any(part in {'.git', 'node_modules', 'analisis', 'playwright-report', 'test-results'}
               for part in relative.parts):
            continue
        page = Page()
        page.feed(path.read_text(encoding='utf-8'))
        name = relative.as_posix()
        url = '/' + (name[:-10] if name.endswith('index.html') else name)
        records.append({'archivo': name, 'ruta': url, 'area_principal': area(name),
                        'titulo': ' '.join(page.name.split()), 'canonical': page.canonical,
                        'robots': page.robots, 'en_sitemap': 'https://lineadepase.com' + url in sitemap,
                        'scripts': page.scripts})
    payload = {'descripcion': 'Inventario local; clasificación editorial para 2.0, no auditoría de contenidos ni de producción.',
               'paginas': len(records), 'urls_sitemap': len(sitemap),
               'por_area': dict(sorted(Counter(r['area_principal'] for r in records).items())),
               'rutas': records}
    OUT.mkdir(exist_ok=True)
    (OUT / 'linea2-inventario.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    buffer = io.StringIO(newline='')
    fields = ['archivo', 'ruta', 'area_principal', 'titulo', 'canonical', 'robots', 'en_sitemap']
    writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction='ignore', lineterminator='\n')
    writer.writeheader()
    writer.writerows(records)
    (OUT / 'linea2-inventario.csv').write_text(buffer.getvalue(), encoding='utf-8-sig')
    lines = ['# Inventario de rutas para Línea de Pase 2.0', '',
             'Generado con `python herramientas/inventario_linea2.py`. Clasificación editorial de archivos locales; no certifica vigencia, datos ni publicación.', '',
             f'**{len(records)} páginas HTML · {len(sitemap)} URLs en sitemap.** Se excluyen fragmentos de análisis, dependencias e informes de pruebas.', '',
             'Cada ruta se asigna a un área principal para planificar; puede aparecer enlazada desde otras. Todas se conservan. El prototipo queda separado del catálogo público.', '',
             '| Área principal | Páginas existentes |', '| --- | ---: |']
    lines += [f'| {name} | {count} |' for name, count in payload['por_area'].items()]
    lines += ['', '| Ruta que se conserva | Área principal | Título | Sitemap |', '| --- | --- | --- | --- |']
    for record in records:
        title = record['titulo'].replace('|', '&#124;')
        lines.append(f"| `{record['ruta']}` | {record['area_principal']} | {title} | {'Sí' if record['en_sitemap'] else 'No'} |")
    (OUT / 'linea2-inventario.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({key: payload[key] for key in ('paginas', 'urls_sitemap', 'por_area')}, ensure_ascii=False))


if __name__ == '__main__':
    build()
