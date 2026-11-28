"""Catálogo editorial compartido de recursos existentes; no duplica sus páginas."""
from html import escape
import json
from pathlib import Path
from urllib.parse import urlencode, urlsplit


def load_catalogue(root):
    data = json.loads((root / 'datos/linea2-catalogo.json').read_text(encoding='utf-8'))
    resources = data['recursos']
    ids = [item['id'] for item in resources]
    if data.get('version') != 1 or len(ids) != len(set(ids)):
        raise ValueError('Catálogo inválido o con identificadores repetidos')
    allowed = {'datalab', 'museo', 'play', 'zaragoza', 'pro', 'studio', 'media'}
    for item in resources:
        if not item['areas'] or not set(item['areas']) <= allowed:
            raise ValueError('Área del catálogo desconocida')
        for field in ['titulo', 'url', 'tipo', 'instruccion', 'contexto', 'limite']:
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f'Falta {field} en {item["id"]}')
        url = urlsplit(item['url'])
        if url.scheme or url.netloc or url.query or url.path.startswith('/'):
            raise ValueError('El catálogo solo acepta rutas locales sin parámetros')
        target = (root / url.path).resolve()
        if not target.is_relative_to(root.resolve()):
            raise ValueError('Ruta fuera del sitio')
        if target.is_dir():
            target /= 'index.html'
        if not target.is_file():
            raise ValueError(f'Recurso no disponible: {item["url"]}')
    return resources


def catalogue(area, resources):
    selected = [item for item in resources if area in item['areas']]
    if not selected:
        return ''
    headings = {'datalab': 'Investigaciones y guías', 'museo': 'Continúa la visita',
                'play': 'Elige cómo explorar el partido', 'zaragoza': 'Todo el seguimiento',
                'pro': 'Trabajos, métodos y herramientas', 'studio': 'Talleres y piezas existentes',
                'media': 'Vídeos y lecturas disponibles'}
    cards = ''
    for item in selected:
        parts = urlsplit(item['url'])
        href = '../' + parts.path + '?' + urlencode({'ldp_origen': area})
        if parts.fragment:
            href += '#' + parts.fragment
        cards += f'''<article class="resource-entry" data-resource="{escape(item['id'])}"><p class="resource-kind">{escape(item['tipo'])}</p><h4>{escape(item['titulo'])}</h4><p>{escape(item['instruccion'])}</p><details><summary>Contexto y límites</summary><p><strong>Contexto:</strong> {escape(item['contexto'])}</p><p><strong>Límite:</strong> {escape(item['limite'])}</p></details><a href="{escape(href, quote=True)}">Abrir {escape(item['titulo'])} →</a></article>'''
    notes = ''
    if area == 'datalab':
        notes = '<p class="catalogue-note">Los experimentos de esta área son modelos didácticos. Los proyectos de abajo tienen sus propios datos, fuentes y métodos. «Los puntos engañan» y el xG universal entrenado siguen pendientes de investigación y validación; no se presentan como resultados disponibles.</p>'
    if area == 'play':
        notes = '<p class="catalogue-note">El trivial y Marcador a ciegas ofrecen respuestas que comprobar. Los comparadores y esquemas permiten explorar; las lecturas y registros editoriales no asignan puntuación.</p>'
    if area == 'pro':
        notes = '<p class="catalogue-note">Pro reúne trabajos y recursos para analizar con criterio. Cada proyecto permite valorar su método y sus límites. <a href="https://github.com/lineadepase/lineadepase.github.io">Consultar el código de los proyectos</a>.</p>'
    return f'<div id="catalogo-{area}" class="resource-catalogue"><h3>{headings[area]}</h3>{notes}<div class="resource-list">{cards}</div></div>'
