"""Comprueba los canonicals de las páginas estáticas publicadas."""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://lineadepase.com/'
NO_CANONICAL = {'404.html'}
SPECIAL = {
    'contacto/index.html': BASE + 'sobre-mi/#contacto',
}


class Metadatos(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.og_urls = []
        self.robots = []

    def handle_starttag(self, tag, values):
        attrs = dict(values)
        if tag.lower() == 'link' and attrs.get('rel', '').lower() == 'canonical':
            self.canonicals.append(attrs.get('href', ''))
        if tag.lower() == 'meta' and attrs.get('property', '').lower() == 'og:url':
            self.og_urls.append(attrs.get('content', ''))
        if tag.lower() == 'meta' and attrs.get('name', '').lower() == 'robots':
            self.robots.append(attrs.get('content', ''))


def canonico_esperado(relative):
    if relative in SPECIAL:
        return SPECIAL[relative]
    if relative == 'proyectos/real-zaragoza/previa.html':
        entries = json.loads((ROOT / 'datos/previas.json').read_text(encoding='utf-8'))
        alias = next((item for item in entries
                      if relative in item.get('alias', [])), None)
        if alias is None:
            return None
        return BASE + alias['pagina']
    if relative == 'index.html':
        return BASE
    if relative.endswith('/index.html'):
        return BASE + relative[:-len('index.html')]
    return BASE + relative


def revisar_sitemap(indexables):
    errores = []
    path = ROOT / 'sitemap.xml'
    namespace = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as error:
        return [f'sitemap.xml: no se pudo leer ({error})']

    locations = [node.text or '' for node in root.iter(namespace + 'loc')]
    if len(locations) != len(set(locations)):
        errores.append('sitemap.xml: contiene URLs duplicadas')

    esperadas = set(indexables)
    incluidas = set(locations)
    for url in sorted(incluidas - esperadas):
        errores.append(f'sitemap.xml: URL no canónica o no indexable: {url}')
    for url in sorted(esperadas - incluidas):
        errores.append(f'sitemap.xml: falta la URL canónica indexable: {url}')

    for url in locations:
        if not url.startswith(BASE):
            errores.append(f'sitemap.xml: URL fuera del dominio canónico: {url}')
            continue
        relative = unquote(urlsplit(url).path).lstrip('/')
        if not relative:
            relative = 'index.html'
        elif relative.endswith('/'):
            relative += 'index.html'
        target = ROOT / relative
        if not target.is_file():
            errores.append(f'sitemap.xml: no existe el HTML de {url}')
    return errores


def revisar():
    paginas = [p for p in ROOT.rglob('*.html')
               if '.git' not in p.relative_to(ROOT).parts
               and 'analisis' not in p.relative_to(ROOT).parts]
    errores = []
    comprobadas = 0
    indexables = []
    for page in paginas:
        relative = page.relative_to(ROOT).as_posix()
        parser = Metadatos()
        parser.feed(page.read_text(encoding='utf-8'))
        if relative in NO_CANONICAL:
            if parser.canonicals:
                errores.append(f'{relative}: no debe declarar canonical')
            continue
        expected = canonico_esperado(relative)
        if expected is None:
            errores.append(f'{relative}: no se pudo resolver la ruta canónica esperada')
            continue
        comprobadas += 1
        if len(parser.canonicals) != 1:
            errores.append(f'{relative}: se esperaba 1 canonical y hay {len(parser.canonicals)}')
        elif parser.canonicals[0] != expected:
            errores.append(f'{relative}: canonical {parser.canonicals[0]!r}; esperado {expected!r}')
        if len(parser.og_urls) > 1:
            errores.append(f'{relative}: hay {len(parser.og_urls)} etiquetas og:url')
        elif parser.og_urls and parser.og_urls[0] != expected:
            errores.append(f'{relative}: og:url {parser.og_urls[0]!r}; esperado {expected!r}')
        directives = {directive.strip().lower() for value in parser.robots
                      for directive in value.split(',')}
        if 'noindex' not in directives:
            indexables.append(expected)
    errores.extend(revisar_sitemap(indexables))
    if errores:
        print(f'Canonicals: {len(errores)} problema(s) en {comprobadas} páginas comprobadas.')
        for error in errores:
            print(f'ERROR {error}')
        return 1
    print(f'Canonicals correctos: {comprobadas} páginas; sitemap correcto: {len(set(indexables))} URLs indexables; 404 sin canonical por diseño.')
    return 0


if __name__ == '__main__':
    sys.exit(revisar())
