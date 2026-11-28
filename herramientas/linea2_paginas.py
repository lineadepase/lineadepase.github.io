"""Entradas por área del prototipo. Comparte contenido con la vista continua."""
from html import escape
from html.parser import HTMLParser
import re


class Identifiers(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get('id'):
            self.ids.add(values['id'])


SCRIPTS = {
    'datalab': ['lab', 'laboratorios', 'escenarios', 'secuencia'],
    'museo': ['museo'],
    'play': ['reto'],
    'zaragoza': ['temporada'],
    'pro': ['investigacion'],
    'studio': ['studio', 'editorial'],
    'media': [],
    'pasaporte': [],
}


def build_pages(destination, sections, fragments):
    owners = {}
    for key, fragment in fragments.items():
        parser = Identifiers()
        parser.feed(fragment)
        owners.update({identifier: key for identifier in parser.ids})

    def reference(value, current):
        if value.startswith('../'):
            return '../' + value
        if value == '#indice-experiencias':
            return '../inicio/#indice-experiencias'
        if value.startswith('#'):
            target = value[1:]
            owner = owners.get(target)
            if owner and owner != current:
                return f'../{owner}/#{target}'
        return value

    def adapt(fragment, current):
        return re.sub(r'\b(href|src|action|poster)="([^"]*)"',
                      lambda m: f'{m[1]}="{reference(m[2], current)}"', fragment)

    def shell(key, title, body, scripts):
        navigation = ''.join(f'<a href="../{area}/"' + (' aria-current="page"' if key == area else '') +
                             f'>{escape(values[0])}</a>' for area, values in sections.items())
        js = ''.join(f'<script src="../../assets/linea2-{name}.js" defer></script>'
                     for name in ['core', *scripts, 'pasaporte', 'acceso'])
        return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><link rel="canonical" href="https://lineadepase.com/datalab-prototipo/{key}/"><title>{escape(title)} · Línea de Pase 2.0 · Prototipo</title><meta name="description" content="{escape(title)}: entrada de desarrollo de Línea de Pase 2.0."><link rel="icon" href="../../assets/icono.svg"><link rel="stylesheet" href="../../assets/linea2.css"><link rel="stylesheet" href="../../assets/linea2-areas.css"></head><body data-area-root="../" data-site-root="../../"><a class="skip" href="#contenido">Saltar al contenido</a><header><a class="brand" href="../inicio/"><img class="brand-original" src="../../assets/marca/logo-intro.webp" width="804" height="258" alt="Línea de Pase · Inicio del prototipo"></a><span class="edition">Del campo al dato.</span><a href="../pasaporte/">Mi pasaporte ↗</a></header><nav aria-label="Áreas de Línea de Pase">{navigation}</nav><main id="contenido" tabindex="-1"><div class="page-intro"><a href="../inicio/">← Inicio por recorridos</a><p class="prototype">Prototipo de desarrollo · sin publicar</p><h1 class="area-page-title">{escape(title)}</h1></div>{body}</main><footer><a href="../inicio/#indice-experiencias">Todas las experiencias</a> · <a href="../">Vista continua anterior</a> · <a href="../../">Web actual</a><p>Ángel Marqueta Alonso · Línea de Pase. Las páginas y datos históricos conservan sus direcciones.</p><a href="../../privacidad/">Privacidad</a></footer>{js}</body></html>'''

    for key, fragment in fragments.items():
        content = adapt(fragment, key)
        if key == 'zaragoza':
            content = content.replace('<button id="temporada-redaccion" type="button" hidden>',
                                      '<a id="temporada-redaccion" class="cta" href="../studio/" hidden>')
            content = content.replace('Preparar publicación con estas jornadas</button>',
                                      'Preparar publicación con estas jornadas</a>')
        if key == 'studio':
            data = re.search(r'<script type="application/json" id="temporada-datos">.*?</script>',
                             fragments['zaragoza'], re.S)
            if not data:
                raise ValueError('Studio necesita el catálogo real de jornadas')
            content += data[0]
        if key != 'pasaporte':
            content += '<p id="guardado" role="status" aria-live="polite"></p>'
        folder = destination / key
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'index.html').write_text(shell(key, sections[key][0], content, SCRIPTS[key]), encoding='utf-8')

    from linea2_experiencias import routes, experience_index
    # Reutiliza los tres recorridos e índice ya revisados, cambiando solo destinos.
    orientation = routes() + experience_index()
    orientation = re.sub(r'\bhref="#([^"]+)"',
                         lambda m: f'href="../{owners[m[1]]}/#{m[1]}"' if m[1] in owners else m[0], orientation)
    menu = ''.join(f'<article class="card"><h3><a href="../{area}/">{escape(values[0])} →</a></h3><p>{escape(values[2])}</p></article>'
                   for area, values in sections.items())
    body = '<section class="orientation"><p class="eyebrow">FÚTBOL · DATOS · PREGUNTAS</p><h2>No solo mires el fútbol. Experiméntalo.</h2><p>Elige un recorrido o entra directamente en un área. Cada herramienta tiene su espacio; puedes guardar las áreas exploradas en tu pasaporte.</p></section>' + orientation + '<div class="grid area-directory">' + menu + '</div>'
    folder = destination / 'inicio'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'index.html').write_text(shell('inicio', 'Elige tu recorrido', body, []), encoding='utf-8')
