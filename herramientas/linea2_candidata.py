"""Prepara una copia de publicación revisable. Nunca publica ni modifica main."""
import argparse
import hashlib
from html import escape, unescape
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

BASE = 'https://lineadepase.com'
AREAS = ['datalab', 'museo', 'play', 'zaragoza', 'pro', 'studio', 'media', 'pasaporte']
MARKER = '.linea2-publicada.json'


def public_html(html, area, description):
    source = f'{BASE}/datalab-prototipo/{area}/'
    destinations = {f'/datalab-prototipo/{key}/': '/' if key == 'inicio' else f'/{key}/'
                    for key in ['inicio', *AREAS]}

    def reference(value):
        url = urlsplit(urljoin(source, value))
        if url.netloc != 'lineadepase.com':
            return value
        route = destinations.get(url.path, url.path)
        if route == '/datalab-prototipo/':
            route = '/sobre-mi/'
        query = dict(parse_qsl(url.query))
        if query.get('ldp_origen') in AREAS:
            query['ldp_vista'] = 'publica'
        return urlunsplit(('', '', route, urlencode(query), url.fragment))

    html = re.sub(r'\b(href|src|action|poster)="([^"]*)"',
                  lambda m: f'{m[1]}="{escape(reference(unescape(m[2])),quote=True)}"', html)
    route = '/' if area == 'inicio' else f'/{area}/'
    html = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{BASE}{route}">', html)
    html = html.replace('noindex,nofollow', 'noindex,follow' if area == 'pasaporte' else 'index,follow')
    html = html.replace(' · Línea de Pase 2.0 · Prototipo</title>', ' · Línea de Pase</title>')
    html = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{escape(description, quote=True)}">', html)
    html = html.replace('data-area-root="../" data-site-root="../../"',
                        'data-area-root="/" data-site-root="/" data-release="2"')
    html = html.replace('Prototipo de desarrollo · sin publicar', 'Línea de Pase · Del campo al dato.')
    html = html.replace('Inicio del prototipo', 'Inicio').replace('Vista continua anterior', 'Sobre el proyecto').replace('Web actual', 'Inicio')
    html = html.replace('Las páginas y datos históricos conservan sus direcciones.', 'Fútbol, datos y preguntas con fuentes y límites explícitos.')
    title=re.search(r'<title>(.*?)</title>',html,re.S)[1]
    metadata = f'<meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{route}"><meta property="og:description" content="{escape(description, quote=True)}"><meta name="twitter:card" content="summary_large_image"><meta property="og:image" content="{BASE}/assets/compartir/inicio.png">'
    return html.replace('</head>', metadata + '</head>')


def render_release(root, destination):
    from linea2 import sections
    descriptions = {key: values[2] for key, values in sections.items()}
    descriptions['inicio'] = 'Experimenta con la ciencia del fútbol, visita el Museo, juega, sigue al Zaragoza y crea con datos en Línea de Pase.'
    for area in ['inicio', *AREAS]:
        html = (root / 'datalab-prototipo' / area / 'index.html').read_text(encoding='utf-8')
        target = destination / ('index.html' if area == 'inicio' else f'{area}/index.html')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(public_html(html, area, descriptions[area]), encoding='utf-8')
    tree = ET.parse(destination / 'sitemap.xml')
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    existing = {node.text for node in tree.getroot().iter(ns + 'loc')}
    for area in AREAS:
        url = f'{BASE}/{area}/'
        if area != 'pasaporte' and url not in existing:
            element = ET.SubElement(tree.getroot(), ns + 'url')
            ET.SubElement(element, ns + 'loc').text = url
    ET.register_namespace('', ns[1:-1])
    ET.indent(tree)
    tree.write(destination / 'sitemap.xml', encoding='utf-8', xml_declaration=True)


def prepare(root, destination):
    root, destination = root.resolve(), destination.resolve()
    if destination.is_relative_to(root) or root.is_relative_to(destination):
        raise ValueError('La candidata debe estar en una carpeta independiente del repositorio')
    if destination.exists() and any(destination.iterdir()):
        raise ValueError('La carpeta de candidata debe estar vacía; no se sobrescriben entregas')
    destination.mkdir(parents=True, exist_ok=True)
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode('utf-8').split('\0')
    for name in names:
        if name and (root / name).is_file():
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / name, target)
    baseline = json.loads((root / 'documentacion/linea2-inventario.json').read_text(encoding='utf-8'))
    hashes = {item['archivo']: hashlib.sha256((root / item['archivo']).read_bytes()).hexdigest()
              for item in baseline['rutas'] if item['en_sitemap'] and item['ruta'] != '/'}
    render_release(root, destination)
    for name, digest in hashes.items():
        if hashlib.sha256((destination / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'Una página histórica se ha modificado: {name}')
    (destination / MARKER).write_text(json.dumps({'version': 2, 'descripcion': 'Edición preparada; publicar requiere aprobación explícita.'}, ensure_ascii=False) + '\n', encoding='utf-8')
    result = subprocess.run([sys.executable, 'herramientas/actualizar_seo.py'], cwd=destination, capture_output=True)
    (destination.parent / (destination.name+'-regeneracion.log')).write_bytes(result.stdout+result.stderr)
    if result.returncode:
        raise RuntimeError('La actualización habitual falló en la candidata: '+result.stderr.decode('utf-8',errors='replace')[-2000:])
    report = {'estado': 'Candidata local, sin publicar', 'rutas_nuevas': [f'/{a}/' for a in AREAS],
              'paginas_historicas_conservadas': len(hashes), 'indexables_previas': baseline['urls_sitemap'],
              'sitemap_preparado': 65, 'pasaporte': 'noindex,follow', 'aprobacion_publicacion': 'Pendiente'}
    (destination / 'candidata-linea2.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(Path(__file__).resolve().parents[1], args.destino), ensure_ascii=False))
