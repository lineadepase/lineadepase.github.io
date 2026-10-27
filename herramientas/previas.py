"""Publica las previas con imagen, URL estable y tarjeta en la portada."""
from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- previas-portada -->'
END = '<!-- /previas-portada -->'
BASE = 'https://lineadepase.com/'
CALENDAR = 'calendario'


def calendar_path(entry):
    return f'{CALENDAR}/{Path(entry["pagina"]).stem}.ics'


def partido_iniciado(entry, ahora=None):
    if not entry.get('fecha_partido') or not entry.get('hora'):
        return False
    inicio = datetime.fromisoformat(entry['fecha_partido']+'T'+entry['hora']).replace(
        tzinfo=ZoneInfo('Europe/Madrid'))
    return (ahora or datetime.now(ZoneInfo('Europe/Madrid'))) >= inicio


def escape_ics(value):
    return (str(value).replace('\\', '\\\\').replace(';', '\\;')
            .replace(',', '\\,').replace('\r\n', '\\n').replace('\n', '\\n'))


def calendar_event(entry):
    """Produce un evento RFC 5545 con horas UTC para evitar desfases de zona."""
    local = datetime.fromisoformat(entry['fecha_partido']+'T'+entry['hora']).replace(
        tzinfo=ZoneInfo('Europe/Madrid'))
    start = local.astimezone(timezone.utc)
    end = (local+timedelta(hours=2, minutes=30)).astimezone(timezone.utc)
    stamp = datetime.fromisoformat(entry.get('fecha_publicacion', entry['fecha_partido'])+'T12:00:00').replace(
        tzinfo=ZoneInfo('Europe/Madrid')).astimezone(timezone.utc)
    url = BASE+entry['pagina']
    description = escape_ics(entry.get('resumen', 'Previa del partido'))+'\\n'+url
    lines = [
        'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Linea de pase//Calendario de partidos//ES',
        'CALSCALE:GREGORIAN', 'METHOD:PUBLISH', 'BEGIN:VEVENT',
        'UID:'+Path(entry['pagina']).stem+'@lineadepase.com',
        'DTSTAMP:'+stamp.strftime('%Y%m%dT%H%M%SZ'),
        'DTSTART:'+start.strftime('%Y%m%dT%H%M%SZ'),
        'DTEND:'+end.strftime('%Y%m%dT%H%M%SZ'),
        'SUMMARY:'+escape_ics(entry['titulo']),
        'LOCATION:'+escape_ics(entry.get('estadio', '')),
        'DESCRIPTION:'+description, 'URL:'+url, 'STATUS:CONFIRMED',
        'END:VEVENT', 'END:VCALENDAR', ''
    ]
    return '\r\n'.join(lines)


def escribir_calendario(entry, root=ROOT):
    path = root/calendar_path(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(calendar_event(entry), encoding='utf-8', newline='')
    return path


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
        postmatch = entry.get('postpartido_url')
        if postmatch:
            post_page = (root/postmatch).resolve()
            if not post_page.is_relative_to(root.resolve()) or not post_page.is_file():
                raise ValueError('La crónica vinculada debe existir dentro de la web: '+str(postmatch))
        centro = entry.get('centro_partido')
        if centro:
            if not isinstance(centro, dict) or not centro.get('fuentes'):
                raise ValueError('El centro del partido necesita al menos una fuente oficial')
            for fuente in centro['fuentes']:
                if not fuente.get('nombre') or not re.match(r'^https://', fuente.get('url', '')):
                    raise ValueError('Cada fuente del centro debe tener nombre y URL HTTPS')
    return entries


def centro_partido_html(entry):
    """Genera un seguimiento editorial sin simular datos en directo."""
    centro = entry.get('centro_partido')
    if not centro:
        return ''
    def dato(value, pending):
        if not value:
            return pending
        if isinstance(value, list):
            return ', '.join(escape(str(item)) for item in value) or pending
        return escape(str(value))
    sources = ''.join(
        '<li><a href="'+escape(source['url'], quote=True)+'" target="_blank" rel="noopener">'
        +escape(source['nombre'])+'</a></li>'
        for source in centro['fuentes']
    )
    incidents = centro.get('incidencias') or []
    incident_markup = ('<ul>'+''.join('<li>'+escape(str(item))+'</li>' for item in incidents)+'</ul>'
                       if incidents else '<p class="nota">Aún no hay incidencias añadidas a esta ficha.</p>')
    return ('<!-- centro-partido --><section class="seccion lectura centro-partido" aria-labelledby="titulo-centro-partido">'
            '<p class="etiqueta">Seguimiento editorial</p><h2 id="titulo-centro-partido">Centro del partido</h2>'
            '<p class="aviso-centro">Esta ficha no ofrece actualización en directo. Los datos se incorporan cuando se confirman y se revisa la fuente.</p>'
            '<dl class="datos-centro">'
            '<div><dt>Marcador</dt><dd>'+dato(centro.get('marcador'), 'Pendiente de actualización editorial.')+'</dd></div>'
            '<div><dt>Alineaciones</dt><dd>'+dato(centro.get('alineaciones'), 'Pendientes de confirmación en esta ficha.')+'</dd></div>'
            '</dl><h3>Incidencias</h3>'+incident_markup+
            '<p class="etiqueta">Fuentes oficiales</p><ul>'+sources+'</ul>'
            '<p class="nota">Última comprobación editorial: '+escape(centro.get('fecha_verificacion', '27/10/2026'))+'.</p>'
            '</section><!-- /centro-partido -->')


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
    html = re.sub(r'<section class="seccion lectura" aria-labelledby="ficha-copa">[\s\S]*?</section>\s*', '', html)
    # Ficha práctica homogénea: solo muestra los datos confirmados disponibles.
    details = []
    if entry.get('fecha_partido'):
        try:
            date = datetime.fromisoformat(entry['fecha_partido']).strftime('%A %d de %B de %Y')
            months = {'October':'octubre','November':'noviembre','December':'diciembre'}
            for en, es in months.items(): date = date.replace(en, es)
            days = {'Monday':'lunes','Tuesday':'martes','Wednesday':'miércoles','Thursday':'jueves','Friday':'viernes','Saturday':'sábado','Sunday':'domingo'}
            for en, es in days.items(): date = date.replace(en, es)
        except ValueError:
            date = entry['fecha_partido']
        date = date[:1].upper()+date[1:]
        if entry.get('hora'):
            date += ', '+entry['hora']+' h (hora peninsular)'
        details.append('<li><strong>Cuándo:</strong> '+escape(date)+'</li>')
    if entry.get('estadio'):
        details.append('<li><strong>Dónde:</strong> '+escape(entry['estadio'])+'</li>')
    if entry.get('competicion'):
        details.append('<li><strong>Competición:</strong> '+escape(entry['competicion'])+'</li>')
    if details:
        block = '<!-- ficha-previa --><section class="seccion lectura ficha-previa" aria-labelledby="ficha-previa"><p class="etiqueta">La cita</p><h2 id="ficha-previa">'+escape(entry['titulo'])+'</h2>'
        if entry.get('fecha_partido'):
            today = datetime.now(ZoneInfo('Europe/Madrid')).date().isoformat()
            date = entry['fecha_partido']
            state = 'Partido disputado' if date < today else ('Hoy'+(' · '+entry['hora'] if entry.get('hora') else '') if date == today else 'Próxima cita · '+date[8:10]+'/'+date[5:7])
            block += '<p class="estado-previa estado-partido-detalle" data-fecha="'+escape(date)+'" data-hora="'+escape(entry.get('hora',''))+'">'+escape(state)+'</p>'
        block += '<ul class="claves">'+''.join(details)+'</ul>'
        if entry.get('fuente_partido'):
            block += '<p class="nota">Horario y estadio: <a href="'+escape(entry['fuente_partido'],quote=True)+'" rel="noopener" target="_blank">confirmación oficial del Real Zaragoza</a>.</p>'
        if entry.get('hora') and entry.get('fecha_partido'):
            postmatch = entry.get('postpartido_url', '')
            hidden = ' hidden' if entry['fecha_partido'] >= datetime.now(ZoneInfo('Europe/Madrid')).date().isoformat() else ''
            postmatch_link = f'<p class="nota postpartido-disponible" data-fecha="{escape(entry["fecha_partido"])}"{hidden}>Ya se ha disputado: <a class="enlace-postpartido" href="../../{escape(postmatch,quote=True)}">Leer la crónica o análisis →</a></p>' if postmatch else ''
            calendar_hidden = ' hidden' if partido_iniciado(entry) else ''
            block += ('<p class="calendario-partido" data-fecha="'+escape(entry['fecha_partido'])+'" data-hora="'+escape(entry['hora'])+'"'+calendar_hidden+'>'
                      '<a class="boton" href="../../'+escape(calendar_path(entry),quote=True)+'" download>Añadir al calendario (.ics)</a></p>')
            if postmatch_link:
                block += postmatch_link
        block += '</section><!-- /ficha-previa -->'
        if '<!-- ficha-previa -->' in html:
            html = re.sub(r'<!-- ficha-previa -->.*?<!-- /ficha-previa -->', lambda _: block, html, flags=re.S)
        else:
            html = html.replace('<!-- /imagen-previa -->', '<!-- /imagen-previa -->'+block, 1)
    center = centro_partido_html(entry)
    if center:
        if '<!-- centro-partido -->' in html:
            html = re.sub(r'<!-- centro-partido -->.*?<!-- /centro-partido -->', lambda _: center, html, flags=re.S)
        else:
            html = html.replace('<!-- /ficha-previa -->', '<!-- /ficha-previa -->'+center, 1)
    elif '<!-- centro-partido -->' in html:
        html = re.sub(r'<!-- centro-partido -->.*?<!-- /centro-partido -->', '', html, flags=re.S)
    share = ('<!-- compartir-previa --><div class="compartir-previa" aria-label="Compartir esta previa">'
             '<button class="boton" type="button" data-compartir-previa>Compartir</button>'
             '<button class="boton" type="button" data-copiar-previa>Copiar enlace</button>'
             '<span class="estado-compartir" data-estado-compartir role="status" aria-live="polite"></span>'
             '</div><!-- /compartir-previa -->')
    if '<!-- compartir-previa -->' in html:
        html = re.sub(r'<!-- compartir-previa -->.*?<!-- /compartir-previa -->', lambda _: share, html, flags=re.S)
    else:
        html = html.replace('<!-- /imagen-previa -->', '<!-- /imagen-previa -->'+share, 1)
    if 'assets/compartir-previa.js' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="../../assets/compartir-previa.css?v=20261027a">\n<script src="../../assets/compartir-previa.js?v=20261027" defer></script>\n</head>', 1)
    html = re.sub(r'(assets/compartir-previa\.css\?v=)[^"\s]+', r'\g<1>20261027a', html)
    if 'assets/estado-partido.js' not in html:
        html = html.replace('</head>', '<script src="../../assets/estado-partido.js?v=20261027b" defer></script>\n</head>', 1)
    html = re.sub(r'(assets/estado-partido\.js\?v=)[^"\s]+', r'\g<1>20261027b', html)
    html = re.sub(r'(assets/real-zaragoza\.css\?v=)[^"\s]+', r'\g<1>20261027c', html)
    # La fecha de publicación no cambia al editar; la actualización sí.
    published = entry.get('fecha_publicacion', entry.get('fecha_partido',''))
    modified = entry.get('fecha_actualizacion', published)
    published_label = datetime.fromisoformat(published).strftime('%d/%m/%Y') if published else ''
    modified_label = datetime.fromisoformat(modified).strftime('%d/%m/%Y') if modified else ''
    date_block = '<p class="fecha-datos">Publicado el '+published_label+((' · Revisado el '+modified_label) if modified else '')+' · Ángel Marqueta Alonso</p>'
    if re.search(r'<p class="fecha-datos">.*?</p>', html, flags=re.S):
        html = re.sub(r'<p class="fecha-datos">.*?</p>', lambda _: date_block, html, count=1, flags=re.S)
    else:
        html = re.sub(r'(</(?:section|header)>)(<!-- imagen-previa -->)', lambda m: m[1]+date_block+m[2], html, count=1)
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
                if published: item['datePublished'] = published
                if modified: item['dateModified'] = modified
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
        state = ('Hoy'+(' · '+entry['hora'] if entry.get('hora') else '')) if fecha == hoy else ('Partido disputado' if fecha < hoy else 'Próxima cita · '+dia)
        fact = dia+(' · '+entry['hora']+' h' if entry.get('hora') else '')+(' · '+entry['estadio'] if entry.get('estadio') else '')
        event_hidden = ' hidden' if partido_iniciado(entry) else ''
        event_link = (f'<a class="boton calendario-partido" data-fecha="{fecha}" data-hora="{escape(entry.get("hora", ""))}"{event_hidden} href="{escape(calendar_path(entry))}" download>Añadir al calendario</a>'
                      if entry.get('hora') else '')
        hidden = ' hidden' if fecha >= datetime.now(ZoneInfo('Europe/Madrid')).date().isoformat() else ''
        postmatch_link = (f'<a class="enlace-postpartido postpartido-disponible" data-fecha="{fecha}"{hidden} href="{escape(entry["postpartido_url"])}">Ver crónica o análisis →</a>'
                          if entry.get('postpartido_url') else '')
        center_link = (f'<a class="enlace-centro-partido" href="{escape(entry["pagina"])}#titulo-centro-partido">Centro del partido →</a>'
                       if entry.get('centro_partido') else '')
        cards.append(f'<article class="tarjeta-previa" data-fecha="{fecha}" data-hora="{escape(entry.get("hora", ""))}"><a href="{escape(entry["pagina"])}">'
                     f'<img src="{escape(entry["imagen"])}" alt="{escape(entry["alt"],quote=True)}" '
                     f'width="{entry["ancho"]}" height="{entry["alto"]}" loading="lazy"></a>'
                     f'<p class="estado-previa">{state}</p><p class="etiqueta">{escape(entry["etiqueta"])}</p><p class="datos-partido">{escape(fact)}</p><h3><a href="{escape(entry["pagina"])}">'
                     f'{escape(entry["titulo"])}</a></h3><p>{escape(entry["resumen"])}</p>'
                     f'<a class="enlace-editorial" href="{escape(entry["pagina"])}">Leer la previa</a>{event_link}{postmatch_link}{center_link}</article>')
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
    html = re.sub(r'(assets/previas\.css\?v=)[^"\s]+', r'\g<1>20261027e', html)
    if 'assets/previas.js' not in html:
        html = html.replace('</head>', '<script src="assets/previas.js?v=20261027" defer></script>\n</head>', 1)
    if 'assets/estado-partido.js' not in html:
        html = html.replace('</head>', '<script src="assets/estado-partido.js?v=20261027b" defer></script>\n</head>', 1)
    html = re.sub(r'(assets/estado-partido\.js\?v=)[^"\s]+', r'\g<1>20261027b', html)
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
        escribir_calendario(entry, root)
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
