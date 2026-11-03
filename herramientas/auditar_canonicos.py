"""Comprueba los canonicals de las páginas estáticas publicadas."""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys

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

    def handle_starttag(self, tag, values):
        attrs = dict(values)
        if tag.lower() == 'link' and attrs.get('rel', '').lower() == 'canonical':
            self.canonicals.append(attrs.get('href', ''))
        if tag.lower() == 'meta' and attrs.get('property', '').lower() == 'og:url':
            self.og_urls.append(attrs.get('content', ''))


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


def revisar():
    paginas = [p for p in ROOT.rglob('*.html')
               if '.git' not in p.relative_to(ROOT).parts
               and 'analisis' not in p.relative_to(ROOT).parts]
    errores = []
    comprobadas = 0
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
    if errores:
        print(f'Canonicals: {len(errores)} problema(s) en {comprobadas} páginas comprobadas.')
        for error in errores:
            print(f'ERROR {error}')
        return 1
    print(f'Canonicals correctos: {comprobadas} páginas; 404 sin canonical por diseño.')
    return 0


if __name__ == '__main__':
    sys.exit(revisar())
