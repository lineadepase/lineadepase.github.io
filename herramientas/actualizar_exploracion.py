"""Archivo, navegación y lecturas relacionadas. Se ejecuta antes del SEO."""
from pathlib import Path
from html import escape, unescape
import os
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- exploracion -->'
END = '<!-- /exploracion -->'


def relative(target, page):
    return os.path.relpath(ROOT / target, page.parent).replace('\\', '/')


def text(value):
    return unescape(re.sub('<[^>]+>', '', value)).strip()


def page(title, description, body):
    template = (ROOT / 'proyectos/index.html').read_text(encoding='utf-8')
    head = template[:template.index('<body>')]
    head = re.sub(r'<!-- SEO:[\s\S]*?<!-- /SEO -->', '', head)
    head = re.sub(r'<title>.*?</title>', '<title>' + escape(title) + ' · Línea de pase</title>', head)
    head = re.sub(r'<meta name="description"[^>]+>', '<meta name="description" content="' + escape(description, quote=True) + '">', head)
    header = re.search(r'<header class="cabecera">[\s\S]*?</header>', template)[0]
    header = header.replace(' aria-current="page"', '')
    footer = re.search(r'<footer class="pie">[\s\S]*?</footer>', template)[0]
    return head + '<body>' + header + '<main class="envoltorio"><section class="seccion primera"><p class="etiqueta">Explora Línea de pase</p><h1>' + escape(title) + '</h1><p class="entradilla">' + escape(description) + '</p>' + body + '</section></main>' + footer + '</body></html>'


def generate():
    from experiencia import generate_comparator, generate_selection, generate_news
    generate_comparator(page)
    generate_selection(page)
    generate_news(page)
    from entregas import generate_tools, generate_delivery
    generate_tools(page)
    generate_delivery(page)
    from segunda_edicion import generate_map, generate_home
    generate_map(page)
    generate_home()
    entries = []
    source = (ROOT / 'proyectos/real-zaragoza/jornadas.html').read_text(encoding='utf-8')
    for href, content in re.findall(r'<a class="tarjeta-jornada [^"]+" href="([^"]+)">([\s\S]*?)</a>', source):
        spans = re.findall(r'<span[^>]*>([\s\S]*?)</span>', content)
        rival = text(spans[1])
        match = f'{rival} – Real Zaragoza' if 'Fuera' in text(spans[0]) else f'Real Zaragoza – {rival}'
        entries.append((f'../proyectos/real-zaragoza/{href}', f'{text(spans[0]).split(" · ")[0]} · {match}', text(spans[0]) + ' · ' + text(spans[2]) + ' · ' + text(spans[3]), '2026/27', rival, 'Partidos'))
    for folder, season, topic in [('futbol-femenino', '2023–2025', 'Fútbol femenino'), ('xg', 'Sin temporada', 'Conceptos'), ('liga-f-xt', '2023/24', 'Investigación')]:
        path = ROOT / 'proyectos' / folder / 'index.html'
        if not path.exists():
            continue
        raw = path.read_text(encoding='utf-8')
        title = text(re.search(r'<h1[^>]*>([\s\S]*?)</h1>', raw)[1])
        desc = re.search(r'<meta name="description" content="([^"]*)"', raw)
        entries.append((f'../proyectos/{folder}/index.html', title, unescape(desc[1]) if desc else '', season, '', topic))
    controls = '<p class="nota">En las fichas del Zaragoza, el marcador se expresa siempre como goles a favor–goles en contra.</p><div class="archivo-controles" id="controles-archivo" hidden><label for="buscar-archivo">Buscar análisis<input id="buscar-archivo" type="search" placeholder="Rival, jornada o concepto"></label>'
    for key, label, values in [('temporada', 'Temporada', sorted({e[3] for e in entries})), ('rival', 'Rival', sorted({e[4] for e in entries if e[4]})), ('tema', 'Tema', sorted({e[5] for e in entries}))]:
        controls += '<label for="filtro-' + key + '">' + label + '<select id="filtro-' + key + '"><option value="">Todos</option>' + ''.join('<option>' + escape(v) + '</option>' for v in values) + '</select></label>'
    controls += '<button type="button" class="boton" id="limpiar-archivo">Limpiar filtros</button></div>'
    cards = '<p class="nota">Cada carpeta reúne los análisis de una sección. La búsqueda y los filtros consultan todas las carpetas a la vez.</p><p id="recuento-archivo" role="status" aria-live="polite">' + str(len(entries)) + ' análisis</p><div class="archivo-carpetas">'
    for topic, label in [('Partidos','Real Zaragoza'),('Investigación','Investigaciones'),('Fútbol femenino','Fútbol femenino · Territorio'),('Conceptos','Conceptos aplicados')]:
        group=[entry for entry in entries if entry[5]==topic]
        if not group:
            continue
        cards += '<details class="archivo-carpeta"><summary><span class="carpeta-nombre">'+escape(label)+'</span> <span class="carpeta-cantidad">'+str(len(group))+' análisis</span></summary><ul class="archivo-lista">'
        for href, title, desc, season, rival, topic in group:
            cards += '<li data-temporada="' + escape(season, quote=True) + '" data-rival="' + escape(rival, quote=True) + '" data-tema="' + escape(topic, quote=True) + '"><article><p class="etiqueta">' + escape(topic + ' · ' + season) + '</p><h2><a href="' + href + '">' + escape(title) + '</a></h2><p>' + escape(desc) + '</p></article></li>'
        cards += '</ul></details>'
    cards += '</div><p id="archivo-vacio" hidden>No hay análisis con estos filtros. Prueba otro término o limpia los filtros.</p><script src="../assets/archivo.js?v=20261021e" defer></script>'
    (ROOT / 'archivo').mkdir(exist_ok=True)
    (ROOT / 'archivo/index.html').write_text(page('Archivo de análisis', 'Busca por temporada, rival o tema y vuelve a los partidos y proyectos que te interesan.', controls + cards), encoding='utf-8')
    concepts = [
        ('xt', 'Amenaza esperada (xT)', 'Asigna un valor a cada zona del campo y mide cómo cambia ese valor cuando un pase o una conducción mueve el balón entre zonas.', 'Si una acción completada pasa de una zona con valor 0,02 a otra con 0,08, añade 0,06 xT en ese modelo. Es un ejemplo ilustrativo, no un dato de partido. La investigación de Liga F valora acciones completadas; no mide por sí sola la calidad global de una jugadora ni ajusta el contexto de su equipo.', '../proyectos/liga-f-xt/index.html#metodo', 'Ver el modelo aplicado a la Liga F', 'https://karun.in/blog/expected-threat.html', 'Karun Singh'),
        ('xg', 'Goles esperados (xG)', 'Estiman la probabilidad de que un tiro acabe en gol a partir de sus características. La suma describe la calidad de las ocasiones rematadas.', 'Un tiro de 0,20 xG equivale a una probabilidad estimada del 20 %. No garantiza un gol ni determina quién mereció ganar. Los modelos de distintos proveedores pueden dar valores diferentes.', '../proyectos/xg/index.html', 'Ver xG, sin líos', 'https://www.hudl.com/blog/expected-goals-xg-explained', 'Hudl Statsbomb'),
        ('posesion', 'Posesión y peligro', 'La posesión describe cuánto balón tiene un equipo según el método del proveedor. Para entender su ataque conviene acompañarla de tiros y calidad de las ocasiones.', 'Tener más balón no asegura generar mejores oportunidades. La página del grupo permite comparar estas dimensiones por separado.', '../proyectos/real-zaragoza/grupo-2.html', 'Comparar los equipos del grupo', '', ''),
        ('presion', 'Presión y PPDA', 'El PPDA relaciona los pases del rival con las acciones defensivas en una zona definida del campo. Un valor menor suele asociarse con una presión más intensa.', 'No mide por sí solo la eficacia de la presión. La zona y las acciones que cuentan dependen del proveedor. El seguimiento actual no publica PPDA: el vídeo aporta contexto visual, no una medición de esta métrica.', '../proyectos/real-zaragoza/jornadas.html', 'Consultar las fichas de partido', 'https://dataglossary.wyscout.com/ppda/', 'Wyscout'),
        ('pases-progresivos', 'Pases progresivos', 'Son pases que acercan de forma relevante el balón a la portería rival. Los umbrales y las zonas de inicio y destino cambian según la definición utilizada.', 'Un pase hacia delante no es necesariamente progresivo. Para comparar jugadores hay que usar el mismo criterio y proveedor. No se publica todavía esta métrica en el panel del Zaragoza.', '../videos/index.html#modelo-xg', 'Ver cómo se construye un modelo con datos', 'https://dataglossary.wyscout.com/progressive_pass/', 'Wyscout'),
        ('por-90', 'Estadísticas por 90 minutos', 'Permiten expresar una acción en una misma escala de tiempo: acciones divididas entre minutos jugados, multiplicadas por 90.', 'Ayudan a comparar participación, pero pocos minutos pueden producir valores extremos. Conviene mostrar siempre los minutos y considerar el rol del jugador.', '../proyectos/real-zaragoza/plantilla.html', 'Consultar minutos y participación', '', ''),
        ('tasas', 'Tasas y denominadores', 'Una tasa relaciona un recuento con la población a la que se refiere. Las licencias por cada 1.000 mujeres permiten comparar territorios de distinto tamaño.', 'Una licencia no equivale necesariamente a una persona. La tasa tampoco demuestra demanda de programas deportivos: hace falta contexto y trabajo de campo.', '../proyectos/futbol-femenino/index.html', 'Leer el análisis de fútbol femenino', '', ''),
    ]
    concepts.sort(key=lambda item: ''.join(c for c in unicodedata.normalize('NFD',item[1]) if not unicodedata.combining(c)).casefold())
    body = '<nav class="enlaces indice-conceptos" aria-label="Índice de conceptos">' + ''.join('<a class="boton" href="#' + c[0] + '">' + c[1] + '</a>' for c in concepts) + '</nav><div class="conceptos-rejilla">'
    for anchor, title, definition, limit, link, label, source, provider in concepts:
        body += '<article class="concepto" id="' + anchor + '"><h2>' + title + '</h2><p>' + definition + '</p><p><strong>Cómo leerlo:</strong> ' + limit + '</p><p><a href="' + link + '">' + label + '</a>' + (' · <a href="' + source + '">Definición de ' + provider + '</a>' if source else '') + '</p></article>'
    body += '</div>'
    (ROOT / 'conceptos').mkdir(exist_ok=True)
    (ROOT / 'conceptos/index.html').write_text(page('Conceptos para leer el fútbol con datos', 'Una guía breve para entender las cifras, sus límites y cómo se utilizan en los análisis de esta web.', body), encoding='utf-8')


def enrich(raw, file):
    from experiencia import enrich as experiencia
    raw = experiencia(raw, file)
    if file == ROOT / 'proyectos/index.html':
        def complete_xt(match):
            card=match[0]
            if 'ficha-proyecto' in card:
                return card
            facts='<dl class="ficha-proyecto"><dt>Pregunta</dt><dd>¿Qué jugadoras acercan el balón a las zonas de gol antes del tiro?</dd><dt>Método</dt><dd>Modelo propio de xT sobre pases y conducciones, con validación fuera de muestra.</dd><dt>Resultado</dt><dd>Clasificación por 90 minutos, intervalos y resultados descargables de la Liga F 2023/24.</dd><dt>Aportación</dt><dd>Preparación de datos, implementación del modelo, comprobaciones y comunicación del análisis.</dd></dl>'
            return card.replace('<span class="ver">',facts+'<span class="ver">',1)
        raw=re.sub(r'<a class="tarjeta-proyecto" href="liga-f-xt/index.html">[\s\S]*?</a>',complete_xt,raw,count=1)
    raw = re.sub(r'<!-- exploracion -->[\s\S]*?<!-- /exploracion -->', '', raw)
    def nav(match):
        links = ''
        # El menú conserva siete entradas; Novedades permanece en el pie.
        for folder,label in [('', 'Inicio'),('proyectos','Proyectos'),('herramientas','Herramientas'),('videos','Vídeos'),('archivo','Archivo'),('conceptos','Conceptos'),('sobre-mi','Sobre mí')]:
            target=folder+'/index.html' if folder else 'index.html'
            current=' aria-current="page"' if file==ROOT/target else ''
            marker=' data-explorar="'+folder+'"' if folder in ('herramientas','archivo','conceptos') else ''
            links+='<a'+marker+' href="'+relative(target,file)+'"'+current+'>'+label+'</a>'
        return re.sub(r'(<nav[^>]*>)[\s\S]*</nav>',lambda m:m[1]+links+'</nav>',match[0])
    raw = re.sub(r'<nav class="nav"[\s\S]*?</nav>', nav, raw)
    def footer(match):
        value=re.sub(r'<a[^>]+data-novedades-pie[^>]*>.*?</a>\s*·\s*','',match[0])
        link='<a data-novedades-pie href="'+relative('novedades/index.html',file)+'">Novedades</a> · '
        return value.replace('© 2026',link+'© 2026',1)
    raw=re.sub(r'<footer class="pie">[\s\S]*?</footer>',footer,raw)
    raw = re.sub(r'(assets/explorar\.css\?v=)[^"\s]+',r'\g<1>20261021e',raw)
    stylesheet = '<link rel="stylesheet" href="' + relative('assets/explorar.css', file) + '?v=20261021e">'
    if 'assets/explorar.css' not in raw:
        raw = raw.replace('</head>', stylesheet + '\n</head>')
    if ('proyectos' in file.relative_to(ROOT).parts and file.name != 'index.html') or file.parent.name in ('futbol-femenino', 'xg', 'liga-f-xt', 'real-zaragoza'):
        links = [('archivo/index.html', 'Más análisis en el archivo'), ('conceptos/index.html', 'Entender los conceptos')]
        if file.parent.name == 'real-zaragoza':
            links.insert(0, ('proyectos/real-zaragoza/evolucion.html' if file.name != 'evolucion.html' else 'proyectos/real-zaragoza/grupo-2.html', 'Poner el partido en contexto'))
        section = START + '<aside class="envoltorio lecturas" aria-labelledby="lecturas-relacionadas"><h2 id="lecturas-relacionadas">Sigue explorando</h2><div class="enlaces">' + ''.join('<a class="boton" href="' + relative(url, file) + '">' + label + '</a>' for url, label in links) + '</div></aside>' + END
        raw = raw.replace('</main>', section + '</main>', 1)
    return raw


def build():
    generate()
    for folder in ['proyectos', 'videos', 'sobre-mi', 'archivo', 'conceptos', 'comparador', 'seleccion', 'novedades', 'mapa-grupo', 'herramientas', 'tras-la-jornada']:
        for file in (ROOT / folder).rglob('*.html'):
            raw = file.read_text(encoding='utf-8')
            if '<main' in raw:
                file.write_text(enrich(raw, file), encoding='utf-8')
    file = ROOT / 'index.html'
    file.write_text(enrich(file.read_text(encoding='utf-8'), file), encoding='utf-8')


if __name__ == '__main__':
    build()
