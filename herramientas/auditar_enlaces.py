"""Comprueba rutas, anclas, imágenes y alt en las páginas estáticas del sitio."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
IGNORAR = {'.git', 'analisis', 'node_modules', '.codex', 'work'}

class Pagina(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.refs = []
        self.images = []
        self.duplicated = set()
        self._seen = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        identifier = a.get('id')
        if identifier:
            if identifier in self._seen:
                self.duplicated.add(identifier)
            self._seen.add(identifier)
            self.ids.add(identifier)
        if tag == 'a' and a.get('href'):
            self.refs.append(a['href'])
        if a.get('src'):
            self.refs.append(a['src'])
        if a.get('srcset'):
            self.refs.extend(part.strip().split()[0] for part in a['srcset'].split(',') if part.strip())
        if tag == 'img':
            self.images.append(a)

def pages():
    return [p for p in ROOT.rglob('*.html')
            if not any(part in IGNORAR for part in p.relative_to(ROOT).parts)]

def local_target(page, path):
    decoded = unquote(path)
    target = (ROOT / decoded.lstrip('/')) if decoded.startswith('/') else (page.parent / decoded)
    target = target.resolve()
    if not target.is_relative_to(ROOT):
        return None
    if target.is_dir():
        target = target / 'index.html'
    return target

def audit():
    all_pages = pages()
    parsed = {}
    errors = []
    image_count = 0
    ref_count = 0
    for page in all_pages:
        parser = Pagina()
        parser.feed(page.read_text(encoding='utf-8'))
        parsed[page.resolve()] = parser
        for identifier in sorted(parser.duplicated):
            errors.append((page, f'duplicate id #{identifier}'))
        for image in parser.images:
            image_count += 1
            if 'alt' not in image:
                errors.append((page, f'img without alt: {image.get("src", "(no src)")}'))
    for page in all_pages:
        for ref in parsed[page.resolve()].refs:
            ref_count += 1
            url = urlsplit(ref)
            if url.scheme or url.netloc or ref.startswith('//'):
                continue
            target = local_target(page, url.path) if url.path else page.resolve()
            if target is None:
                errors.append((page, f'local URL escapes site root: {ref}'))
                continue
            if not target.exists():
                errors.append((page, f'missing local target: {ref}'))
                continue
            fragment = unquote(url.fragment)
            if fragment and target.suffix.lower() == '.html':
                target_page = parsed.get(target.resolve())
                if target_page is None:
                    target_page = Pagina()
                    target_page.feed(target.read_text(encoding='utf-8'))
                    parsed[target.resolve()] = target_page
                if fragment not in target_page.ids:
                    errors.append((page, f'missing anchor: {ref}'))
    print(f'{len(all_pages)} páginas · {ref_count} enlaces y recursos locales · {image_count} imágenes')
    if errors:
        for page, message in errors:
            print(f'ERROR {page.relative_to(ROOT)}: {message}')
        raise SystemExit(f'{len(errors)} problemas encontrados')
    print('Sin rutas, anclas, atributos alt ni IDs duplicados problemáticos.')

if __name__ == '__main__':
    audit()
