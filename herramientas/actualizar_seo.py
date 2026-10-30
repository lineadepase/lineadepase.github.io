"""Actualiza metadatos, tarjetas sociales y sitemap sin cambiar el contenido.

Ejecutar tras regenerar las páginas: python herramientas/actualizar_seo.py
Requiere Pillow. No incluye fragmentos de análisis ni páginas de redirección.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape, unescape
import json
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit
from PIL import Image, ImageDraw, ImageFont
from google_analytics import incorporar_etiqueta

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://lineadepase.com'
START = '<!-- SEO: generado por herramientas/actualizar_seo.py -->'
END = '<!-- /SEO -->'


class Head(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ''
        self.description = ''
        self.in_title = False
        self.redirect = False
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag == 'meta':
            if a.get('name', '').lower() == 'description':
                self.description = a.get('content', '')
            if a.get('name', '').lower() == 'robots':
                self.noindex = 'noindex' in a.get('content', '').lower()
            if a.get('http-equiv', '').lower() == 'refresh':
                self.redirect = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, value):
        if self.in_title:
            self.title += value


def font(size, bold=False):
    names = (['C:/Windows/Fonts/arialbd.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
             if bold else ['C:/Windows/Fonts/arial.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    raise RuntimeError('Instala Arial o DejaVu Sans para generar las tarjetas.')


def wrap(draw, text, face, width):
    lines = []
    for word in text.split():
        if lines and draw.textlength(lines[-1] + ' ' + word, font=face) <= width:
            lines[-1] += ' ' + word
        else:
            lines.append(word)
    return lines


def card(title, category, output):
    im = Image.new('RGB', (1200, 630), '#10231e')
    d = ImageDraw.Draw(im)
    # Campo y recorrido de pase: elementos vectoriales de la identidad de la web.
    for x in range(900, 1200, 45):
        d.rectangle((x, 0, x + 22, 630), fill='#17362c')
    ink = '#36594a'
    d.rectangle((931, 54, 1250, 574), outline=ink, width=3)
    d.line((931, 314, 1200, 314), fill=ink, width=3)
    d.ellipse((1030, 233, 1192, 395), outline=ink, width=3)
    d.rectangle((1010, 54, 1200, 131), outline=ink, width=3)
    d.rectangle((1010, 497, 1200, 574), outline=ink, width=3)
    for i in range(11):
        x, y = 975 + i * 14, 458 - i * 21
        d.ellipse((x-3, y-3, x+3, y+3), fill='#83ad8f')
    d.ellipse((1118, 222, 1140, 244), fill='#ff7a2f')
    d.text((66, 45), 'LÍNEA DE PASE', font=font(27, True), fill='#f4f7f1')
    d.text((66, 111), category.upper(), font=font(22, True), fill='#b0d6b4')
    size = 58
    while True:
        face = font(size, True)
        lines = wrap(d, title, face, 800)
        if len(lines) <= 4 or size <= 38:
            break
        size -= 2
    y = 188
    for line in lines:
        d.text((62, y), line, font=face, fill='#f4f7f1')
        y += size + 11
    d.line((66, 521, 861, 521), fill='#507361', width=2)
    d.rectangle((66, 519, 139, 524), fill='#ff7a2f')
    d.text((66, 551), 'lineadepase.com', font=font(27, True), fill='#f4f7f1')
    d.text((488, 554), 'Fútbol · Datos · Contexto', font=font(23), fill='#b0c3b6')
    im.save(output, optimize=True)


def build():
    from actualizar_exploracion import build as exploracion
    exploracion()
    output = ROOT / 'assets' / 'compartir'
    output.mkdir(parents=True, exist_ok=True)
    files = [ROOT / 'index.html']
    for folder in ['proyectos', 'sobre-mi', 'videos', 'contacto', 'archivo', 'archivo-visual', 'conceptos', 'comparador', 'seleccion', 'novedades', 'mapa-grupo', 'herramientas', 'tras-la-jornada', 'privacidad', 'preguntas-del-partido', 'marcador-a-ciegas', 'datos-en-revision', 'partidos-espejo', 'reloj-del-marcador', 'pizarron-de-una-jugada', 'balance-de-preguntas', 'mapa-de-lo-que-cambio', 'esquemas-del-juego', 'galeria-visual']:
        files.extend(sorted((ROOT / folder).rglob('*.html')))
    urls = []
    manifest = []
    for file in files:
        with file.open('r', encoding='utf-8', newline='') as stream:
            raw = stream.read()
        nl = '\r\n' if '\r\n' in raw else '\n'
        head = Head()
        head.feed(raw.split('</head>', 1)[0])
        if head.redirect or head.noindex:
            continue
        path = file.relative_to(ROOT).as_posix()
        # GitHub Pages redirige /carpeta/index.html a /carpeta/. Declara y
        # publica siempre la URL limpia para evitar enviar redirecciones a Google.
        if path == 'index.html':
            url = BASE + '/'
        elif path.endswith('/index.html'):
            url = BASE + '/' + path[:-len('index.html')]
        else:
            url = BASE + '/' + path
        slug = 'inicio' if path == 'index.html' else path.removesuffix('.html').replace('/', '-')
        image_path = 'assets/compartir/' + slug + '.png'
        image_url = BASE + '/' + image_path
        editorial = re.search(r'<meta name="imagen-editorial" content="([^"]+)">', raw)
        if editorial:
            image_path = editorial[1]
            image_url = BASE + '/' + image_path
        title = head.title.strip()
        display = title.replace(' · Línea de pase', '').strip()
        if path == 'index.html':
            display = 'Entender el fútbol con datos'
        category = ('Real Zaragoza · 2026/27' if '/real-zaragoza/' in path else
                    'Fútbol femenino · Datos abiertos' if '/futbol-femenino/' in path else
                    'Analítica de fútbol')
        description = head.description.strip()
        if not description:
            raise ValueError(f'Falta descripción en {path}')
        if not editorial:
            card(display, category, ROOT / image_path)
        # Sustituir solo nuestro bloque mantiene intactos títulos y descripciones editoriales.
        raw = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\r?\n?', '', raw, flags=re.S)
        raw = re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>\s*', '', raw, flags=re.I)
        # Las plantillas antiguas enlazan a index.html aunque la ruta limpia
        # sea la que declaramos como canónica. Normaliza esos enlaces internos.
        def enlace_limpio(match):
            comilla, destino = match.group(1), match.group(2)
            if destino.startswith(('http://', 'https://')) and not destino.startswith(BASE + '/'):
                return match.group(0)
            partes = urlsplit(destino)
            ruta = partes.path
            if ruta == 'index.html':
                ruta = './'
            elif ruta.endswith('/index.html'):
                ruta = ruta[:-len('index.html')]
            else:
                return match.group(0)
            return f'href={comilla}{ruta}{("?" + partes.query) if partes.query else ""}{("#" + partes.fragment) if partes.fragment else ""}{comilla}'
        raw = re.sub(r"href=([\"'])(.*?)\1", enlace_limpio, raw, flags=re.I)
        e = lambda x: escape(x, quote=True)
        tags = [START,
                f'<link rel="canonical" href="{e(url)}">',
                '<meta property="og:type" content="website">',
                '<meta property="og:locale" content="es_ES">',
                '<meta property="og:site_name" content="Línea de pase">',
                f'<meta property="og:title" content="{e(title)}">',
                f'<meta property="og:description" content="{e(description)}">',
                f'<meta property="og:url" content="{e(url)}">',
                f'<meta property="og:image" content="{e(image_url)}">',
                '<meta property="og:image:type" content="image/png">',
                '<meta property="og:image:width" content="1200">',
                '<meta property="og:image:height" content="630">',
                f'<meta property="og:image:alt" content="{e(display + " · Línea de pase")}">',
                '<meta name="twitter:card" content="summary_large_image">',
                f'<meta name="twitter:title" content="{e(title)}">',
                f'<meta name="twitter:description" content="{e(description)}">',
                f'<meta name="twitter:image" content="{e(image_url)}">',
                f'<meta name="twitter:image:alt" content="{e(display + " · Línea de pase")}">',
                END]
        if path == 'index.html':
            schema = {'@context': 'https://schema.org', '@graph': [
                {'@type': 'WebSite', '@id': BASE + '/#website', 'url': BASE + '/',
                 'name': 'Línea de pase', 'inLanguage': 'es', 'description': description,
                 'author': {'@id': BASE + '/sobre-mi/#autor'}},
                {'@type': 'Person', '@id': BASE + '/sobre-mi/#autor',
                 'name': 'Ángel Marqueta Alonso', 'url': BASE + '/sobre-mi/',
                 'sameAs': ['https://www.linkedin.com/in/angel-marqueta-alonso-a8831164',
                            'https://www.youtube.com/@lineadepasefutbol']}]}
            tags.insert(-1, '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script>')
        else:
            crumbs = [('Inicio', BASE + '/')]
            if path.startswith('proyectos/') and path != 'proyectos/index.html':
                crumbs.append(('Proyectos', BASE + '/proyectos/'))
            if path.startswith('proyectos/real-zaragoza/') and path != 'proyectos/real-zaragoza/index.html':
                crumbs.append(('Real Zaragoza', BASE + '/proyectos/real-zaragoza/'))
            crumbs.append((title.replace(' · Línea de pase', ''), url))
            graph = [{
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': n, 'name': name, 'item': link}
                    for n, (name, link) in enumerate(crumbs, 1)]}]
            if path.startswith('proyectos/') and path not in ['proyectos/index.html', 'proyectos/real-zaragoza/index.html']:
                graph.append({
                    '@type': 'Article', '@id': url + '#analisis',
                    'headline': title.replace(' · Línea de pase', ''),
                    'description': description, 'image': [image_url],
                    'inLanguage': 'es', 'mainEntityOfPage': url,
                    'author': {'@type': 'Person', 'name': 'Ángel Marqueta Alonso',
                               'url': BASE + '/sobre-mi/'}})
            tags.insert(-1, '<script type="application/ld+json">' + json.dumps(
                {'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False) + '</script>')
        raw = raw.replace('</head>', nl.join(tags) + nl + '</head>', 1)
        raw = incorporar_etiqueta(raw)
        file.write_text(raw, encoding='utf-8', newline='')
        urls.append(url)
        manifest.append({'path': path, 'url': url, 'image': image_path})
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    root = ET.Element(ns + 'urlset')
    for url in sorted(urls):
        ET.SubElement(ET.SubElement(root, ns + 'url'), ns + 'loc').text = url
    ET.indent(root)
    ET.ElementTree(root).write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + BASE + '/sitemap.xml\n', encoding='utf-8')
    from previas import sincronizar
    sincronizar(ROOT)
    from calidad_web import build as mejorar_calidad
    mejorar_calidad(ROOT)
    from auditar_imagenes import audit as auditar_peso_y_alt
    image_audit = auditar_peso_y_alt(ROOT)
    print(json.dumps({'pages': len(urls), 'cards': len(manifest), 'urls': urls, 'image_audit': image_audit}, ensure_ascii=False))


if __name__ == '__main__':
    build()
