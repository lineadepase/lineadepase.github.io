"""Audita nombres alternativos y peso estimado de imágenes por página."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json

ROOT = Path(__file__).resolve().parents[1]
IGNORE = {'.git', 'analisis', 'node_modules', '.codex', 'work'}
PAGE_BUDGET_BYTES = 1_200 * 1024
WARNING_BUDGET_BYTES = int(PAGE_BUDGET_BYTES * .8)
FOCUS_PAGES = {
    'index.html',
    'proyectos/real-zaragoza/goles-en-video.html',
    'proyectos/real-zaragoza/grupo-2.html',
}
VOID_ELEMENTS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class PageImages(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []
        self.stack: list[tuple[str, bool]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or '' for key, value in attrs}
        hidden = values.get('aria-hidden', '').lower() == 'true' or values.get('role', '').lower() == 'presentation'
        if tag == 'img':
            values['_hidden_context'] = str(hidden or any(item[1] for item in self.stack)).lower()
            self.images.append(values)
        if tag not in VOID_ELEMENTS:
            self.stack.append((tag, hidden))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID_ELEMENTS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


def pages(root: Path) -> list[Path]:
    return [page for page in root.rglob('*.html')
            if not any(part in IGNORE for part in page.relative_to(root).parts)]


def image_path(page: Path, value: str, root: Path) -> tuple[Path, str] | None:
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    target = (root / unquote(parsed.path).lstrip('/')) if parsed.path.startswith('/') else page.parent / unquote(parsed.path)
    target = target.resolve()
    if not target.is_relative_to(root.resolve()):
        return None
    return target, parsed.query


def requested_source(image: dict[str, str]) -> str:
    candidates: list[tuple[int, str]] = []
    for candidate in image.get('srcset', '').split(','):
        parts = candidate.strip().rsplit(None, 1)
        if len(parts) == 2 and parts[1].endswith('w') and parts[1][:-1].isdigit():
            candidates.append((int(parts[1][:-1]), parts[0]))
    if not candidates:
        return image.get('src', '')
    declared_width = image.get('width', '')
    target_width = min(int(declared_width), 800) if declared_width.isdigit() else 800
    ordered = sorted(candidates)
    return next((src for width, src in ordered if width >= target_width), ordered[-1][1])


def audit(root: Path = ROOT) -> dict[str, object]:
    counts = {'informative': 0, 'decorative': 0, 'review': 0, 'missing': 0}
    unresolved: list[str] = []
    estimates: list[dict[str, object]] = []
    for page in pages(root):
        parser = PageImages()
        parser.feed(page.read_text(encoding='utf-8'))
        requests: dict[tuple[str, str], tuple[int, bool]] = {}
        for image in parser.images:
            alt = image.get('alt')
            if alt is None:
                counts['missing'] += 1
                unresolved.append(f'{page.relative_to(root).as_posix()}: {image.get("src", "(sin src)")} no tiene alt')
            elif alt.strip():
                counts['informative'] += 1
            elif image.get('_hidden_context') == 'true':
                counts['decorative'] += 1
            else:
                counts['review'] += 1
                unresolved.append(f'{page.relative_to(root).as_posix()}: {image.get("src", "(sin src)")} usa alt vacío fuera de un contexto decorativo explícito')

            source = image_path(page, requested_source(image), root)
            if source is None:
                continue
            path, query = source
            key = (str(path), query)
            if path.is_file():
                immediate = image.get('loading', '').lower() != 'lazy' or image.get('fetchpriority', '').lower() == 'high'
                previous = requests.get(key)
                requests[key] = (path.stat().st_size, immediate or (previous[1] if previous else False))
        initial_bytes = sum(size for size, immediate in requests.values() if immediate)
        deferred_bytes = sum(size for size, immediate in requests.values() if not immediate)
        estimates.append({
            'path': page.relative_to(root).as_posix(),
            'bytes': initial_bytes + deferred_bytes,
            'initial_bytes': initial_bytes,
            'deferred_bytes': deferred_bytes,
            'initial_images': sum(1 for _, immediate in requests.values() if immediate),
            'deferred_images': sum(1 for _, immediate in requests.values() if not immediate),
            'images': len(parser.images),
        })

    largest = sorted(estimates, key=lambda item: int(item['bytes']), reverse=True)
    focus = [item for item in estimates if item['path'] in FOCUS_PAGES]
    near = [item for item in largest if int(item['bytes']) >= WARNING_BUDGET_BYTES]
    over = [item for item in largest if int(item['bytes']) > PAGE_BUDGET_BYTES]
    result: dict[str, object] = {
        'pages': len(estimates),
        'images': sum(int(item['images']) for item in estimates),
        'alt': counts,
        'page_budget_bytes': PAGE_BUDGET_BYTES,
        'warning_budget_bytes': WARNING_BUDGET_BYTES,
        'largest_pages': largest[:5],
        'focus_pages': focus,
        'near_budget_pages': near,
        'over_budget_pages': over,
        'initial_image_bytes': sum(int(item['initial_bytes']) for item in estimates),
        'deferred_image_bytes': sum(int(item['deferred_bytes']) for item in estimates),
        'issues': unresolved,
    }
    print(f"{result['pages']} páginas · {result['images']} imágenes: {counts['informative']} informativas, {counts['decorative']} decorativas, {counts['review']} por revisar, {counts['missing']} sin alt.")
    if largest:
        heaviest = largest[0]
        print(f"Peso estimado a un ancho máximo de 800 px: {int(heaviest['bytes']) / 1024:.0f} KiB en {heaviest['path']}; presupuesto {PAGE_BUDGET_BYTES / 1024:.0f} KiB.")
    print(f"{len(near)} páginas en zona preventiva (80 % del presupuesto); {len(over)} por encima del límite.")
    initial_total = int(result['initial_image_bytes'])
    deferred_total = int(result['deferred_image_bytes'])
    print(f"Carga inicial estimada: {initial_total / 1024:.0f} KiB; imágenes con loading=lazy: {deferred_total / 1024:.0f} KiB. Estimación por atributos, no medición de red.")
    for issue in unresolved:
        print('REVISAR ' + issue)
    for item in near[:5]:
        print(f"CERCA {int(item['bytes']) / 1024:.0f} KiB · {item['path']}")
    for item in focus:
        print(f"PRIORIDAD {int(item['bytes']) / 1024:.0f} KiB · inicial {int(item['initial_bytes']) / 1024:.0f} KiB · diferida {int(item['deferred_bytes']) / 1024:.0f} KiB · {item['path']}")
    if unresolved or over:
        raise RuntimeError(f"Auditoría de imágenes: {len(unresolved)} textos alternativos por resolver y {len(over)} páginas sobre presupuesto.")
    return result


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False))
