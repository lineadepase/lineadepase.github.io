"""Publica las previas con imagen, URL estable y tarjeta en la portada."""
from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- previas-portada -->'
END = '<!-- /previas-portada -->'
BASE = 'https://lineadepase.com/'


def guardar(path, text):
    path.write_text(text, encoding='utf-8', newline='\n')


def registro(root=ROOT):
    entries = json.loads((root / 'datos/previas.json').read_text(encoding='utf-8'))
    for entry in entries:
        image = (root / entry['imagen']).resolve()
        if not image.is_relative_to(root.resolve()) or not image.is_file():
            raise ValueError('Falta la imagen editorial de la previa: ' + entry['imagen'])
        page = (root / entry['pagina']).resolve()
        if not page.is_relative_to(root.resolve()):
            raise ValueError('La página de la previa debe estar dentro de la web')
    return entries


def con_imagen(html, entry):
    """Añade el recurso editorial sin alterar el análisis de datos existente."""
    image = entry['imagen'].removeprefix('proyectos/real-zaragoza/')
    figure = ('<!-- imagen-previa --><figure class="foto imagen-editorial-previa">'
              f'<img src="{escape(image)}" width="{entry["ancho"]}" height="{entry["alto"]}" '
              f'alt="{escape(entry["alt"], quote=True)}" style="width:100%;height:auto;border-radius:12px">'
              '<figcaption>Ilustración editorial generada con IA.</figcaption></figure><!-- /imagen-previa -->')
    if '<!-- imagen-previa -->' in html:
        html = re.sub(r'<!-- imagen-previa -->.*?<!-- /imagen-previa -->', lambda _: figure, html, flags=re.S)
    else:
        # Siempre después de la cabecera, antes de tablas y gráficos.
        html, count = re.subn(r'(<(?:section|header) class="cab-proyecto">.*?</(?:section|header)>)', lambda m: m[0]+figure, html, count=1, flags=re.S)
        if count != 1:
            raise ValueError('No se encontró la cabecera de la previa')
    if entry.get('noticia_html'):
        news = '<!-- noticia-previa -->'+entry['noticia_html']+'<!-- /noticia-previa -->'
        if '<!-- noticia-previa -->' in html:
            html = re.sub(r'<!-- noticia-previa -->.*?<!-- /noticia-previa -->', lambda _: news, html, flags=re.S)
        else:
            html = html.replace('<!-- /imagen-previa -->', '<!-- /imagen-previa -->'+news, 1)
    # Metadatos explícitos: el generador SEO los conserva en las siguientes pasadas.
    html = re.sub(r'<meta name="imagen-editorial"[^>]*>\s*', '', html)
    html = html.replace('</head>', f'<meta name="imagen-editorial" content="{entry["imagen"]}">\n</head>', 1)
    canonical = BASE + entry['pagina']
    html = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m[1]+canonical, html)
    html = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m[1]+canonical, html)
    for key in ('og:image', 'twitter:image'):
        html = re.sub(r'(<meta (?:property|name)="'+key+r'" content=")[^"]*', lambda m: m[1]+BASE+entry['imagen'], html)
    html = re.sub(r'(<meta property="og:image:type" content=")[^"]*', lambda m: m[1]+'image/webp', html)
    for key in ('ancho', 'alto'):
        prop = 'width' if key == 'ancho' else 'height'
        html = re.sub(r'(<meta property="og:image:'+prop+r'" content=")[^"]*', lambda m: m[1]+str(entry[key]), html)
    def schema(match):
        value = json.loads(match[1])
        for item in value.get('@graph', [value]):
            if item.get('@type') == 'Article':
                item['image'] = [BASE+entry['imagen']]
                item['mainEntityOfPage'] = canonical
                item['@id'] = canonical+'#analisis'
            if item.get('@type') == 'BreadcrumbList' and item.get('itemListElement'):
                item['itemListElement'][-1]['item'] = canonical
        return '<script type="application/ld+json">'+json.dumps(value,ensure_ascii=False)+'</script>'
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', schema, html, flags=re.S)


def ordenar(entries, hoy):
    upcoming = sorted((x for x in entries if x['fecha_partido'] >= hoy), key=lambda x: x['fecha_partido'])
    past = sorted((x for x in entries if x['fecha_partido'] < hoy), key=lambda x: x['fecha_partido'], reverse=True)
    return upcoming+past


def portada(root=ROOT, hoy=None):
    entries = registro(root)
    hoy = hoy or datetime.now(ZoneInfo('Europe/Madrid')).date().isoformat()
    cards = []
    for entry in ordenar(entries, hoy)[:4]:
        if not (root / entry['pagina']).is_file():
            raise ValueError('Publica primero la noticia: '+entry['pagina'])
        fecha = entry['fecha_partido']
        dia = fecha[8:10]+'/'+fecha[5:7]
        state = ('Hoy'+(' · '+entry['hora'] if entry.get('hora') else '')) if fecha == hoy else ('Previa del '+dia if fecha < hoy else 'Próxima cita · '+dia)
        cards.append(f'<article class="tarjeta-previa" data-fecha="{fecha}" data-hora="{escape(entry.get("hora", ""))}"><a href="{escape(entry["pagina"])}">'
                     f'<img src="{escape(entry["imagen"])}" alt="{escape(entry["alt"],quote=True)}" '
                     f'width="{entry["ancho"]}" height="{entry["alto"]}" loading="lazy"></a>'
                     f'<p class="estado-previa">{state}</p><p class="etiqueta">{escape(entry["etiqueta"])}</p><h3><a href="{escape(entry["pagina"])}">'
                     f'{escape(entry["titulo"])}</a></h3><p>{escape(entry["resumen"])}</p>'
                     f'<a class="enlace-editorial" href="{escape(entry["pagina"])}">Leer la previa →</a></article>')
    block = START+'<section class="previas-portada" aria-labelledby="titulo-previas"><p class="etiqueta">Antes del partido</p><h2 id="titulo-previas">Las previas, con contexto</h2><div class="previas-rejilla">'+''.join(cards)+'</div></section>'+END
    path = root / 'index.html'
    html = path.read_text(encoding='utf-8')
    if START in html:
        html = re.sub(re.escape(START)+'.*?'+re.escape(END), lambda _: block, html, flags=re.S)
    else:
        marker = '<section class="actualidad-editorial actualidad-compacta">'
        if marker not in html:
            raise ValueError('No se encontró el bloque editorial de la portada')
        html = html.replace(marker, block+marker, 1)
    if 'assets/previas.css' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="assets/previas.css?v=20261027">\n</head>', 1)
    html = re.sub(r'(assets/previas\.css\?v=)[^"\s]+', r'\g<1>20261027b', html)
    if 'assets/previas.js' not in html:
        html = html.replace('</head>', '<script src="assets/previas.js?v=20261027" defer></script>\n</head>', 1)
    news_path = root / 'datos/novedades.json'
    if news_path.is_file():
        news = json.loads(news_path.read_text(encoding='utf-8'))
        items = ''.join(f'<li><time datetime="{n["fecha"]}">{n["fecha"][8:10]}/{n["fecha"][5:7]}</time>'
                        f'<span>{escape(n["tipo"])}</span><a href="{escape(n["url"])}">{escape(n["titulo"])}</a></li>'
                        for n in news[:3])
        html = re.sub(r'(<section class="actualizaciones-breves">.*?<ul>).*?(</ul>)',
                      lambda m: m[1]+items+m[2], html, count=1, flags=re.S)
    guardar(path, html)


def publicar_liga(jornada, html, root=ROOT):
    entries = registro(root)
    entry = next((x for x in entries if x.get('jornada') == jornada), None)
    if entry is None:
        raise ValueError(f'Antes de publicar la previa J{jornada}, añade su noticia e imagen a datos/previas.json')
    for item in entries:
        item['alias'] = ['proyectos/real-zaragoza/previa.html'] if item is entry else []
    guardar(root / 'datos/previas.json', json.dumps(entries, ensure_ascii=False, indent=2)+'\n')
    html = con_imagen(html, entry)
    # Guardar una URL que no cambiará al generar la siguiente jornada.
    archived = html.replace(BASE+'proyectos/real-zaragoza/previa.html', BASE+entry['pagina'])
    guardar(root / entry['pagina'], archived)
    portada(root)
    if root == ROOT:
        from actualizar_exploracion import generate_archive
        generate_archive()
    return html


def sincronizar(root=ROOT):
    for entry in registro(root):
        for page in [entry['pagina']]+entry.get('alias', []):
            path = root / page
            if path.is_file():
                guardar(path, con_imagen(path.read_text(encoding='utf-8'), entry))
    portada(root)
    path = root / 'sitemap.xml'
    tree = ET.parse(path)
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    existing = {x.text for x in tree.getroot().iter(ns+'loc')}
    for entry in registro(root):
        if BASE+entry['pagina'] not in existing:
            ET.SubElement(ET.SubElement(tree.getroot(), ns+'url'), ns+'loc').text = BASE+entry['pagina']
    ET.register_namespace('', ns[1:-1])
    ET.indent(tree)
    tree.write(path, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    sincronizar()
