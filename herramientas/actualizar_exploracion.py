"""Archivo, navegación y lecturas relacionadas. Se ejecuta antes del SEO."""
from pathlib import Path
from html import escape, unescape
import csv
from datetime import date as date_type
import json
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


def cronologia_partido(relative):
    match = re.fullmatch(r'proyectos/real-zaragoza/jornada-(\d+)\.html', relative)
    if not match:
        return ''
    moments = json.loads((ROOT/'datos/momentos-partido.json').read_text(encoding='utf-8')).get(match[1])
    if not moments:
        return ''
    items = ''.join('<li><span class="momento-minuto">'+escape(str(item['minuto']))+'’</span><div><strong>'+escape(item['marcador'])+'</strong><p>'+escape(item['hecho'])+'</p></div></li>' for item in moments['momentos'])
    sources = ' · '.join('<a href="'+escape(source['url'],quote=True)+'" target="_blank" rel="noopener">'+escape(source['nombre'])+'</a>' for source in moments.get('fuentes',[])[:2])
    source_note = '<p class="fuentes-cronologia">Fuentes: '+sources+'</p>' if sources else ''
    return ('<!-- cronologia-partido --><section class="seccion lectura cronologia-partido" aria-labelledby="titulo-cronologia-partido">'
            '<p class="etiqueta">La secuencia del encuentro</p><h2 id="titulo-cronologia-partido">El partido en tres momentos</h2>'
            '<ol class="momentos-partido">'+items+'</ol><aside class="fuera-de-plano"><h3>Lo que los datos no muestran</h3><p>'+escape(moments['limite'])+'</p></aside>'
            +source_note+
            '</section><!-- /cronologia-partido -->')


def incorporar_cronologia(raw, file):
    relative = file.relative_to(ROOT).as_posix()
    raw = re.sub(r'<!-- cronologia-partido -->[\s\S]*?<!-- /cronologia-partido -->', '', raw)
    block = cronologia_partido(relative)
    if block and '<!-- /tres-claves -->' in raw:
        raw = raw.replace('<!-- /tres-claves -->','<!-- /tres-claves -->'+block,1)
    if relative.startswith('proyectos/real-zaragoza/') and 'assets/ideas-editoriales.css' not in raw:
        path = relative.count('/')
        prefix = '../'*path
        raw = raw.replace('</head>','<link rel="stylesheet" href="'+prefix+'assets/ideas-editoriales.css?v=20261027a">\n</head>',1)
    return raw


def page(title, description, body, extra_head='', canonical=None):
    template = (ROOT / 'proyectos/index.html').read_text(encoding='utf-8')
    head = template[:template.index('<body>')]
    head = re.sub(r'<!-- SEO:[\s\S]*?<!-- /SEO -->', '', head)
    head = re.sub(r'<title>.*?</title>', '<title>' + escape(title) + ' · Línea de pase</title>', head)
    head = re.sub(r'<meta name="description"[^>]+>', '<meta name="description" content="' + escape(description, quote=True) + '">', head)
    if extra_head:
        head = head.replace('</head>', extra_head+'\n</head>', 1)
    if canonical:
        url = 'https://lineadepase.com/'+canonical.strip('/')+'/'
        social = ('<link rel="canonical" href="'+escape(url,quote=True)+'">'
                  '<meta property="og:type" content="website"><meta property="og:site_name" content="Línea de pase">'
                  '<meta property="og:title" content="'+escape(title+' · Línea de pase',quote=True)+'">'
                  '<meta property="og:description" content="'+escape(description,quote=True)+'">'
                  '<meta property="og:url" content="'+escape(url,quote=True)+'">'
                  '<meta name="twitter:card" content="summary"><meta name="twitter:title" content="'+escape(title+' · Línea de pase',quote=True)+'">'
                  '<meta name="twitter:description" content="'+escape(description,quote=True)+'">')
        head = head.replace('</head>',social+'\n</head>',1)
    header = re.search(r'<header class="cabecera">[\s\S]*?</header>', template)[0]
    header = header.replace(' aria-current="page"', '')
    footer = re.search(r'<footer class="pie">[\s\S]*?</footer>', template)[0]
    return head + '<body>' + header + '<main class="envoltorio"><section class="seccion primera"><p class="etiqueta">Explora Línea de pase</p><h1>' + escape(title) + '</h1><p class="entradilla">' + escape(description) + '</p>' + body + '</section></main>' + footer + '</body></html>'


def generate_archive():
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
    import json
    previews = json.loads((ROOT/'datos/previas.json').read_text(encoding='utf-8'))
    for item in previews:
        rival = item.get('rival', item['titulo'].replace('Real Zaragoza', '').strip(' –—-'))
        if item.get('resultado_confirmado'):
            topic = 'Análisis · Copa del Rey' if 'copa' in item['pagina'] else 'Análisis · Liga'
            title = 'Análisis · '+item['titulo']
        else:
            topic = 'Previas · Copa del Rey' if 'copa' in item['pagina'] else 'Previas · Liga'
            title = 'Previa · '+item['titulo']
        entries.append(('../'+item['pagina'], title, item['resumen'], '2026/27', rival, topic))
    sim = ROOT/'proyectos/real-zaragoza/simulacion.html'
    if sim.is_file():
        entries.append(('../proyectos/real-zaragoza/simulacion.html', 'Simulación del grupo 2 de Primera Federación', 'Probabilidades de ascenso, playoff y descenso con su fecha de corte, método y límites.', '2026/27', '', 'Investigación'))
    videos = (ROOT/'videos/index.html').read_text(encoding='utf-8')
    for block in re.findall(r'<article class="video-explicacion"[^>]*>.*?</article>', videos, flags=re.S):
        identifier = re.search(r'\bid="([^"]+)"', block)
        heading = re.search(r'<h2[^>]*>([\s\S]*?)</h2>', block)
        summary = re.search(r'<p>([\s\S]*?)</p>', re.search(r'<div class="lectura">([\s\S]*?)</div>', block)[1])
        if identifier and heading:
            entries.append(('../videos/#'+identifier[1], text(heading[1]), text(summary[1]) if summary else '', '', '', 'Vídeos'))
    concepts = (ROOT/'conceptos/index.html').read_text(encoding='utf-8')
    for block in re.findall(r'<article class="concepto"[^>]*>.*?</article>', concepts, flags=re.S):
        identifier = re.search(r'\bid="([^"]+)"', block)
        heading = re.search(r'<h2[^>]*>([\s\S]*?)</h2>', block)
        summary = re.search(r'<p>([\s\S]*?)</p>', block)
        if identifier and heading:
            entries.append(('../conceptos/#'+identifier[1], text(heading[1]), text(summary[1]) if summary else '', '', '', 'Conceptos'))
    controls = '<p class="nota">En las fichas del Zaragoza, el marcador se expresa siempre como goles a favor–goles en contra.</p><div class="archivo-controles" id="controles-archivo" role="search" aria-label="Filtrar el archivo" hidden><label for="buscar-archivo">Buscar en el archivo<input id="buscar-archivo" type="search" placeholder="Rival, jornada, vídeo o concepto"></label>'
    for key, label, values in [('temporada', 'Temporada', [v for v in sorted({e[3] for e in entries}) if v]), ('rival', 'Rival', sorted({e[4] for e in entries if e[4]})), ('tema', 'Tema', sorted({e[5] for e in entries}))]:
        controls += '<label for="filtro-' + key + '">' + label + '<select id="filtro-' + key + '"><option value="">Todos</option>' + ''.join('<option>' + escape(v) + '</option>' for v in values) + '</select></label>'
    controls += '<label for="filtro-tipo">Tipo de pieza<select id="filtro-tipo"><option value="">Todos</option><option>Partido</option><option>Previa</option><option>Análisis</option><option>Investigación</option><option>Vídeo</option><option>Concepto</option></select></label>'
    controls += '<button type="button" class="boton" id="limpiar-archivo">Limpiar filtros</button><button type="button" class="boton" id="compartir-filtros">Copiar enlace de búsqueda</button><span id="estado-compartir-archivo" role="status" aria-live="polite"></span></div>'
    cards = '<p class="nota">Cada carpeta reúne el contenido de una sección. La búsqueda y los filtros consultan análisis, vídeos y conceptos a la vez.</p><p id="recuento-archivo" role="status" aria-live="polite">' + str(len(entries)) + ' recursos</p><div class="archivo-carpetas">'
    for topic, label in [('Partidos','Real Zaragoza'),('Previas · Liga','Previas · Liga'),('Previas · Copa del Rey','Previas · Copa del Rey'),('Análisis · Liga','Análisis · Liga'),('Análisis · Copa del Rey','Análisis · Copa del Rey'),('Investigación','Investigaciones'),('Fútbol femenino','Fútbol femenino · Territorio'),('Vídeos','Vídeos explicativos'),('Conceptos','Conceptos aplicados')]:
        group=[entry for entry in entries if entry[5]==topic]
        if not group:
            continue
        quantity = 'recurso' if len(group)==1 else 'recursos'
        cards += '<details class="archivo-carpeta"><summary><span class="carpeta-nombre">'+escape(label)+'</span> <span class="carpeta-cantidad">'+str(len(group))+' '+quantity+'</span></summary><ul class="archivo-lista">'
        for href, title, desc, season, rival, topic in group:
            kind = {'Partidos': 'Partido', 'Previas · Liga': 'Previa', 'Previas · Copa del Rey': 'Previa', 'Análisis · Liga': 'Análisis', 'Análisis · Copa del Rey': 'Análisis', 'Investigación': 'Investigación', 'Fútbol femenino': 'Análisis', 'Vídeos': 'Vídeo', 'Conceptos': 'Concepto'}[topic]
            cards += '<li data-temporada="' + escape(season, quote=True) + '" data-rival="' + escape(rival, quote=True) + '" data-tema="' + escape(topic, quote=True) + '" data-tipo="' + kind + '"><article><p class="etiqueta">' + escape(topic + ' · ' + season) + '</p><h2><a href="' + href + '">' + escape(title) + '</a></h2><p>' + escape(desc) + '</p></article></li>'
        cards += '</ul></details>'
    cards += '</div><p id="archivo-vacio" role="status" aria-live="polite" hidden>No hay análisis con estos filtros. Prueba otro término o limpia los filtros.</p><script src="../assets/archivo.js?v=20261027b" defer></script>'
    (ROOT / 'archivo').mkdir(exist_ok=True)
    output = ROOT / 'archivo/index.html'
    html = page('Archivo de análisis', 'Busca por temporada, rival, tema o tipo de pieza y vuelve a los partidos y proyectos que te interesan.', controls + cards)
    if output.is_file():
        previous = output.read_text(encoding='utf-8')
        # La reconstrucción del contenido no elimina metadatos ni estilos ya publicados.
        html = previous[:previous.index('</head>')+7] + html[html.index('</head>')+7:]
        html = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Busca por rival, jornada, temporada, tema o tipo de pieza entre análisis, previas, vídeos y conceptos.">', html, count=1)
    output.write_text(html, encoding='utf-8')


def generate_preguntas():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    entries = json.loads((ROOT/'datos/previas.json').read_text(encoding='utf-8'))
    cards = []
    for entry in entries:
        question = entry.get('pregunta_abierta')
        if not question:
            continue
        href = '../'+entry['pagina']
        result = entry.get('resultado_confirmado') or {}
        answer = result.get('respuesta_pregunta')
        today = datetime.now(ZoneInfo('Europe/Madrid')).date().isoformat()
        status = 'Respondida' if answer else ('Pendiente de revisión editorial' if entry.get('fecha_partido', '') < today else 'Abierta')
        block = '<article class="pregunta-registro"><p class="etiqueta">'+escape(entry.get('competicion','Partido'))+' · '+escape(status)+'</p><h2><a href="'+escape(href,quote=True)+'">'+escape(entry['titulo'])+'</a></h2><p class="pregunta-registro-pregunta">'+escape(question)+'</p>'
        if answer:
            block += '<p><strong>Respuesta después del partido.</strong> '+escape(answer)+'</p>'
        else:
            block += '<p class="nota">La pregunta se mantiene abierta hasta que el partido y sus datos estén comprobados.</p>'
        block += '<a class="enlace-editorial" href="'+escape(href,quote=True)+'">'+('Volver a la pregunta y su respuesta →' if answer else 'Leer la previa →')+'</a></article>'
        cards.append(block)
    body = '<p>Una pregunta por partido. La respuesta se añade después, con una acción observada y datos disponibles; las cuestiones sin respuesta siguen visibles como abiertas.</p><div class="preguntas-registro">'+''.join(cards)+'</div>'
    folder = ROOT/'preguntas-del-partido'
    folder.mkdir(exist_ok=True)
    css = '<link rel="stylesheet" href="../assets/ideas-editoriales.css?v=20261027a">'
    (folder/'index.html').write_text(page('Las preguntas del partido','Preguntas previas que se revisan después del encuentro con acciones y datos comprobados.',body,css,'preguntas-del-partido/'),encoding='utf-8')


def generate_marcador_a_ciegas():
    season = json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    matches = [m for m in season['partidos'] if m.get('completo') and m.get('tiros_zaragoza') is not None and m.get('tiros_rival') is not None and m.get('posesion_pct') is not None]
    cards = []
    for match in sorted(matches,key=lambda m:int(m['jornada']),reverse=True):
        date = match['fecha']
        date_label = date[8:10]+'/'+date[5:7]+'/'+date[:4]
        zaragoza_first = match['sede'] == 'Casa'
        teams = ('Real Zaragoza',match['rival']) if zaragoza_first else (match['rival'],'Real Zaragoza')
        shots = (match['tiros_zaragoza'],match['tiros_rival']) if zaragoza_first else (match['tiros_rival'],match['tiros_zaragoza'])
        score = (match['goles_favor'],match['goles_contra']) if zaragoza_first else (match['goles_contra'],match['goles_favor'])
        local_name, away_name = escape(teams[0]), escape(teams[1])
        local_attr, away_attr = escape(teams[0],quote=True), escape(teams[1],quote=True)
        jornada = str(match['jornada'])
        stats = '<dl class="marcador-ciego-datos"><div><dt>Posesión del Zaragoza</dt><dd>'+escape(str(match['posesion_pct']).replace('.0',''))+' %</dd></div><div><dt>Tiros</dt><dd>'+escape(str(shots[0]))+' · '+escape(str(shots[1]))+'</dd></div></dl>'
        card = (f'<article class="reto-marcador" data-goles-local="{score[0]}" data-goles-visitante="{score[1]}" data-equipo-local="{local_attr}" data-equipo-visitante="{away_attr}" data-jornada="{jornada}">'
                f'<p class="etiqueta">Jornada {jornada} · {date_label}</p><h2>{local_name} – {away_name}</h2>{stats}'
                f'<form class="marcador-ciego-form"><fieldset><legend>¿Qué marcador crees que hubo?</legend><label>{local_name}<input type="number" name="local" min="0" max="20" inputmode="numeric" required></label><span aria-hidden="true">–</span><label>{away_name}<input type="number" name="visitante" min="0" max="20" inputmode="numeric" required></label></fieldset><button class="boton lleno" type="submit">Comprobar mi marcador</button></form><p class="marcador-ciego-feedback" role="status" aria-live="polite"></p><details class="marcador-ciego-revelar"><summary>Mostrar el marcador y consultar la ficha</summary><p class="marcador-ciego-resultado">Resultado: <strong>{score[0]}–{score[1]}</strong></p><a class="enlace-marcador-partido" href="../proyectos/real-zaragoza/jornada-{jornada}.html">Consultar ficha y fuente →</a></details><p class="nota">La posesión y los tiros describen el partido; por sí solos no permiten deducir el marcador.</p></article>')
        cards.append(card)
    body = '<p>El marcador queda oculto mientras se comparan posesión y tiros. La idea es comprobar cuánto cuentan esas cifras y cuánto deja fuera un resultado.</p><p class="nota">Solo entran partidos con posesión y tiros registrados de forma homogénea. La jornada 9 queda fuera mientras se aclara la discrepancia en el recuento de tiros.</p><div class="retos-marcador">'+''.join(cards)+'</div>'
    folder = ROOT/'marcador-a-ciegas'
    folder.mkdir(exist_ok=True)
    head = '<link rel="stylesheet" href="../assets/ideas-editoriales.css?v=20261027a"><script src="../assets/marcador-a-ciegas.js?v=20261027a" defer></script>'
    (folder/'index.html').write_text(page('El marcador a ciegas','Adivina el resultado a partir de la posesión y los tiros registrados en partidos del Real Zaragoza.',body,head,'marcador-a-ciegas/'),encoding='utf-8')


def generate_datos_revision():
    source = 'https://www.realzaragoza.com/partidos/temporada-2026-2027-primera-federacion-9-ce-europa-vs-real-zaragoza-3940'
    comparison = 'https://www.zerozero.pt/live-ao-minuto/2026-10-23-ce-europa-real-zaragoza/12323619'
    body = '''<p>Cuando dos fichas ofrecen cifras distintas, la diferencia queda a la vista y el análisis evita escoger una sin explicar por qué.</p>
<article class="discrepancia-registro" id="tiros-j9"><p class="etiqueta">Primera Federación · Jornada 9 · 23/10/2026</p><h2>CE Europa – Real Zaragoza</h2><p>El marcador final fue 0–1. El recuento de tiros no coincide entre las dos fichas consultadas:</p>
<div class="tabla-desbordable"><table><caption>Tiros registrados en la J9, según cada ficha</caption><thead><tr><th scope="col">Fuente</th><th scope="col">Tiros</th><th scope="col">A puerta</th></tr></thead><tbody>
<tr><th scope="row"><a href="''' + source + '''" target="_blank" rel="noopener">Real Zaragoza</a></th><td>9–8</td><td>2–1</td></tr>
<tr><th scope="row"><a href="''' + comparison + '''" target="_blank" rel="noopener">ZeroZero</a></th><td>10–8</td><td>3–1</td></tr>
</tbody></table></div>
<p><strong>Qué hace el análisis.</strong> Conserva el registro de la ficha del club, identifica su procedencia y deja la discrepancia abierta. No usa el recuento para calcular una tasa de acierto ni para afirmar que una versión sea la correcta.</p>
<p><strong>Qué queda por aclarar.</strong> La ficha del club muestra tiros totales, a puerta y fuera; su desglose visible no permite reconstruir por completo los totales. Eso no prueba por sí solo un error: la ficha no detalla todos los criterios de clasificación.</p>
<p class="nota">Estado: pendiente de resolución editorial · Revisado el 27/10/2026. El análisis no incluye xG para este encuentro.</p>
<a class="enlace-editorial" href="../proyectos/real-zaragoza/jornada-9.html">Volver al análisis de la J9 →</a></article>
<p class="nota">Este registro recoge diferencias concretas que afectan a una lectura publicada. No reúne discrepancias menores ni sustituye la ficha de cada partido.</p>'''
    folder = ROOT/'datos-en-revision'
    folder.mkdir(exist_ok=True)
    css = '<link rel="stylesheet" href="../assets/ideas-editoriales.css?v=20261027b">'
    (folder/'index.html').write_text(page('Cuando las cifras no coinciden','Registro de diferencias entre fuentes deportivas y criterio aplicado en los análisis de Línea de pase.',body,css,'datos-en-revision/'),encoding='utf-8')


def generate_partidos_espejo():
    season = json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    matches = [m for m in season['partidos'] if m.get('completo') and all(m.get(key) is not None for key in ('tiros_zaragoza','tiros_rival','posesion_pct','goles_favor','goles_contra'))]
    matches.sort(key=lambda m:int(m['jornada']))
    options = ''.join('<option value="'+str(m['jornada'])+'">J'+str(m['jornada'])+' · '+escape(m['rival'])+'</option>' for m in matches)
    profiles = []
    for m in matches:
        profiles.append('<article class="espejo-partido" data-jornada="'+str(m['jornada'])+'" data-rival="'+escape(m['rival'],quote=True)+'" data-posesion="'+str(m['posesion_pct'])+'" data-diferencia-tiros="'+str(m['tiros_zaragoza']-m['tiros_rival'])+'" data-gf="'+str(m['goles_favor'])+'" data-gc="'+str(m['goles_contra'])+'" data-tiros-z="'+str(m['tiros_zaragoza'])+'" data-tiros-r="'+str(m['tiros_rival'])+'"><p class="etiqueta">Jornada '+str(m['jornada'])+'</p><h3>Real Zaragoza – '+escape(m['rival'])+'</h3><p>Posesión: '+escape(str(m['posesion_pct']).replace('.0',''))+' % · Tiros: '+str(m['tiros_zaragoza'])+'–'+str(m['tiros_rival'])+'</p><p>Resultado: '+str(m['goles_favor'])+'–'+str(m['goles_contra'])+'</p></article>')
    body = '<p>Algunos partidos se parecen en posesión y balance de tiros y, aun así, terminan con marcadores distintos. Esta vista permite comparar esos perfiles en la temporada del Zaragoza.</p><div class="espejo-aviso"><strong>Cómo leerlo.</strong> La comparación usa seis partidos de liga con posesión, tiros y resultado completos. Encuentra el perfil más cercano por posesión y diferencia de tiros entre los que acabaron con otro marcador. Es una exploración descriptiva: no predice resultados ni explica por qué se produjeron.</div><section class="partidos-espejo" aria-labelledby="titulo-espejo"><h2 id="titulo-espejo">Elige un partido</h2><label for="selector-espejo">Partido de referencia<select id="selector-espejo">'+options+'</select></label><button class="boton lleno" type="button" id="comparar-espejo">Buscar un perfil parecido</button><p id="estado-espejo" role="status" aria-live="polite">Elige un partido para ver la comparación.</p><div id="resultado-espejo" class="espejo-comparacion"></div></section><details class="espejo-muestra"><summary>Ver los partidos incluidos</summary><div class="espejo-registros">'+''.join(profiles)+'</div></details><p class="nota">Los partidos con registros incompletos, incluida la J9 mientras siga abierta la discrepancia de tiros, quedan fuera.</p><a class="enlace-editorial" href="../datos-en-revision/">Consultar la discrepancia de la J9 →</a>'
    folder = ROOT/'partidos-espejo'
    folder.mkdir(exist_ok=True)
    head = '<link rel="stylesheet" href="../assets/ideas-editoriales.css?v=20261027b"><script src="../assets/partidos-espejo.js?v=20261027b" defer></script>'
    (folder/'index.html').write_text(page('Partidos espejo','Explora encuentros del Real Zaragoza con posesión y diferencia de tiros parecidas, pero marcadores distintos.',body,head,'partidos-espejo/'),encoding='utf-8')


def generate_reloj_marcador():
    season = json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    matches = []
    for match in season['partidos']:
        ficha = next((row for row in season['fichas'] if row['jornada'] == match['jornada']), None)
        if not ficha:
            continue
        matches.append({
            'jornada': match['jornada'], 'rival': match['rival'], 'sede': match['sede'],
            'golesFavor': match['goles_favor'], 'golesContra': match['goles_contra'],
            'goles': [{'minuto': g['minuto'], 'sentido': g['sentido'], 'jugador': g['jugador'], 'propiaPuerta': g['propia_puerta']} for g in ficha['goles']],
            'href': '../proyectos/real-zaragoza/jornada-'+str(match['jornada'])+'.html'
        })
    payload = json.dumps(matches, ensure_ascii=False).replace('<','\\u003c').replace('</script','<\\/script')
    body = '<p>El resultado también se entiende por cuánto tiempo se sostuvo. El reloj resume cómo estuvo el marcador del Zaragoza durante los 90 minutos reglamentarios.</p><div class="espejo-aviso"><strong>Criterio.</strong> El descuento no se convierte en minutos ficticios ni se suma a la barra: sus goles se muestran aparte. Los goles del 45+ se aplican al descanso; los del 90+ aparecen fuera de los 90 minutos. Así la gráfica no confunde el reloj reglamentario con la duración real del encuentro.</div><section class="reloj-marcador" aria-labelledby="titulo-reloj"><h2 id="titulo-reloj">Elige un partido</h2><label for="selector-reloj">Partido<select id="selector-reloj"></select></label><div id="reloj-resultado" aria-live="polite"></div></section><script type="application/json" id="datos-reloj">'+payload+'</script>'
    head = '<link rel="stylesheet" href="../assets/ideas-editoriales.css?v=20261027c"><script src="../assets/reloj-del-marcador.js?v=20261027c" defer></script>'
    folder = ROOT/'reloj-del-marcador'
    folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(page('El reloj del marcador','Compara cuánto tiempo estuvo el Real Zaragoza en ventaja, empate o desventaja durante los 90 minutos reglamentarios.',body,head,'reloj-del-marcador/'),encoding='utf-8')


def generate_pizarron_jugada():
    moments = json.loads((ROOT/'datos/momentos-partido.json').read_text(encoding='utf-8'))['9']
    goal = next(item for item in moments['momentos'] if str(item['minuto']) == '80')
    svg = '<figure class="pizarron-figura"><svg class="pizarron-secuencia" viewBox="0 0 960 250" role="img" aria-labelledby="titulo-secuencia descripcion-secuencia"><title id="titulo-secuencia">Secuencia del gol del Real Zaragoza en Can Dragó</title><desc id="descripcion-secuencia">Un saque de esquina, el remate de Diego González y el desvío de Álex Cano que terminó en gol en propia puerta.</desc><rect x="8" y="8" width="944" height="234" rx="18" fill="#17452e"/><path d="M28 125H932M320 20v210M640 20v210" stroke="#d5e5d8" stroke-opacity=".28" stroke-width="2"/><path d="M44 36v178m0-89h94m-94-49a49 49 0 0 1 49 49 49 49 0 0 1-49 49" fill="none" stroke="#d5e5d8" stroke-opacity=".35" stroke-width="2"/><path d="M350 125h110m38 0h110" stroke="#f2c34b" stroke-width="5" stroke-linecap="round" stroke-dasharray="3 11"/><circle data-paso="0" cx="180" cy="125" r="35" fill="#f2c34b"/><circle data-paso="1" cx="500" cy="125" r="35" fill="#f2c34b"/><circle data-paso="2" cx="820" cy="125" r="35" fill="#f2c34b"/><text x="180" y="137" text-anchor="middle" fill="#10291e" font-size="34" font-family="system-ui,sans-serif" font-weight="800">1</text><text x="500" y="137" text-anchor="middle" fill="#10291e" font-size="34" font-family="system-ui,sans-serif" font-weight="800">2</text><text x="820" y="137" text-anchor="middle" fill="#10291e" font-size="34" font-family="system-ui,sans-serif" font-weight="800">3</text><text x="180" y="194" text-anchor="middle" fill="#fff" font-size="18" font-family="system-ui,sans-serif">Córner</text><text x="500" y="194" text-anchor="middle" fill="#fff" font-size="18" font-family="system-ui,sans-serif">Remate de Diego González</text><text x="820" y="194" text-anchor="middle" fill="#fff" font-size="18" font-family="system-ui,sans-serif">Desvío y gol</text></svg><figcaption>Esquema de la secuencia; no representa posiciones ni distancias exactas.</figcaption></figure>'
    body = '<p>El único gol de la J9 llegó en una acción a balón parado. El esquema ordena los tres pasos que describe el resumen del partido:</p>'+svg+'<div class="jugada-inversa" data-jugada-inversa><div class="jugada-inversa-botones"><button class="boton" type="button" data-retroceder>Retroceder una acción</button><button class="boton" type="button" data-avanzar>Avanzar hacia el gol</button></div><p data-estado-jugada role="status" aria-live="polite">Paso 3 de 3: el desvío termina en gol.</p></div><ol class="pizarron-pasos"><li><strong>El saque.</strong> El Zaragoza puso el balón en juego desde un córner.</li><li><strong>El remate.</strong> Diego González cabeceó hacia la portería.</li><li><strong>El desvío.</strong> Álex Cano tocó el balón y lo introdujo en su propia portería en el minuto 80.</li></ol><aside class="fuera-de-plano"><h2>Lo que no muestra el esquema</h2><p>'+escape(moments['limite'])+' No hay coordenadas de seguimiento, así que el dibujo explica el orden de la acción, no la colocación exacta de los jugadores.</p></aside><p><a class="enlace-editorial" href="https://www.youtube.com/watch?v=gBB7ameQWbI" target="_blank" rel="noopener">Ver el resumen de la jugada →</a> · <a href="../proyectos/real-zaragoza/jornada-9.html">Análisis de la J9</a></p>'
    head = '<link rel="stylesheet" href="../assets/ideas-editoriales.css?v=20261027d"><script src="../assets/jugada-hacia-atras.js?v=20261027d" defer></script>'
    folder = ROOT/'pizarron-de-una-jugada'
    folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(page('El pizarrón de una jugada','Una secuencia esquemática del gol del Real Zaragoza ante el CE Europa: córner, remate y desvío.',body,head,'pizarron-de-una-jugada/'),encoding='utf-8')


def generate_mapa_cambios():
    moments = json.loads((ROOT/'datos/momentos-partido.json').read_text(encoding='utf-8'))['9']['momentos']
    changes = []
    with (ROOT/'analisis/real-zaragoza/datos/entrada/cambios.csv').open(encoding='utf-8-sig', newline='') as stream:
        import csv
        changes = [row for row in csv.DictReader(stream) if row['partido_id'] == '9']
    goal = next(item for item in moments if str(item['minuto']) == '80')
    minute_events = {}
    for row in changes:
        minute_events.setdefault(int(row['minuto']), []).append(row)
    items = []
    for minute in sorted(set(minute_events) | {80}):
        if minute == 80:
            fact = goal['hecho']
            marker = goal['marcador']
        else:
            actions = '; '.join(escape(row['entra'])+' por '+escape(row['sale']) for row in minute_events[minute])
            fact = 'Cambios del Zaragoza: '+actions+'.'
            marker = 'Sustituciones'
        items.append('<li><span class="momento-minuto">'+str(minute)+'’</span><div><strong>'+escape(marker)+'</strong><p><strong>Hecho.</strong> '+fact+'</p></div></li>')
    body = ('<p>La ficha del partido registra cinco sustituciones del Zaragoza entre los minutos 56 y 78. Dos minutos después llegó el gol que decidió el encuentro.</p>'
            '<ol class="momentos-partido mapa-cambios">'+''.join(items)+'</ol>'
            '<aside class="fuera-de-plano"><h2>Qué permite concluir</h2><p><strong>Lectura.</strong> La secuencia ordena los cambios y el gol. Que ocurrieran antes no demuestra que los cambios provocaran el gol: el registro no incluye posesiones, ocasiones ni posiciones por minuto.</p></aside>'
            '<p class="nota">Fuente: <a href="https://www.realzaragoza.com/partidos/temporada-2026-2027-primera-federacion-9-ce-europa-vs-real-zaragoza-3940" target="_blank" rel="noopener">ficha oficial del Real Zaragoza</a>.</p>'
            '<p><a class="enlace-editorial" href="../proyectos/real-zaragoza/jornada-9.html">Consultar el análisis de la J9 →</a> · <a href="../pizarron-de-una-jugada/">Ver la secuencia del gol</a></p>')
    head = '<link rel="stylesheet" href="../assets/ideas-editoriales.css?v=20261027d">'
    folder = ROOT/'mapa-de-lo-que-cambio'
    folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(page('El mapa de lo que cambió','Una cronología de las sustituciones y el gol de la J9, con los hechos separados de lo que puede interpretarse.',body,head,'mapa-de-lo-que-cambio/'),encoding='utf-8')


def generate_balance_preguntas():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    today = datetime.now(ZoneInfo('Europe/Madrid')).date().isoformat()
    previews = json.loads((ROOT/'datos/previas.json').read_text(encoding='utf-8'))
    records = []
    for item in previews:
        question = item.get('pregunta_abierta')
        if not question:
            continue
        answer = (item.get('resultado_confirmado') or {}).get('respuesta_pregunta')
        status = 'Respondida' if answer else ('Pendiente de revisión' if item.get('fecha_partido','') < today else 'Abierta')
        records.append((item, question, answer, status))
    answered = sum(1 for _,_,answer,_ in records if answer)
    open_count = sum(1 for _,_,answer,status in records if not answer and status == 'Abierta')
    pending = sum(1 for _,_,answer,status in records if not answer and status == 'Pendiente de revisión')
    stats = '<dl class="balance-preguntas-cifras"><div><dt>Registradas</dt><dd>'+str(len(records))+'</dd></div><div><dt>Respondidas</dt><dd>'+str(answered)+'</dd></div><div><dt>Abiertas</dt><dd>'+str(open_count)+'</dd></div><div><dt>Pendientes de revisión</dt><dd>'+str(pending)+'</dd></div></dl>'
    cards = []
    for item,question,answer,status in records:
        card = '<article class="pregunta-registro"><p class="etiqueta">'+escape(item.get('competicion','Partido'))+' · '+escape(status)+'</p><h2><a href="../'+escape(item['pagina'],quote=True)+'">'+escape(item['titulo'])+'</a></h2><p class="pregunta-registro-pregunta">'+escape(question)+'</p>'
        if answer:
            card += '<p><strong>Revisión:</strong> '+escape(answer)+'</p>'
        elif status == 'Pendiente de revisión':
            card += '<p class="nota">El partido ya ha pasado. La pregunta sigue pendiente hasta comprobar una acción y los datos disponibles.</p>'
        else:
            card += '<p class="nota">Se revisará después del partido, cuando el resultado y la acción relevante estén comprobados.</p>'
        cards.append(card+'</article>')
    body = '<p>Antes de cada partido se plantea una pregunta concreta. Después, la respuesta se incorpora solo cuando el encuentro y los datos están comprobados.</p>'+stats+'<div class="espejo-aviso"><strong>Qué cuenta este balance.</strong> Registra preguntas respondidas, abiertas o pendientes de revisión. No puntúa aciertos: son preguntas de observación sobre el juego, no pronósticos del marcador.</div><div class="preguntas-registro">'+''.join(cards)+'</div><p><a class="enlace-editorial" href="../preguntas-del-partido/">Ver el registro completo →</a></p>'
    head = '<link rel="stylesheet" href="../assets/ideas-editoriales.css?v=20261027c">'
    folder = ROOT/'balance-de-preguntas'
    folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(page('Balance de preguntas','Un registro de preguntas planteadas antes de los partidos y respuestas añadidas después de comprobar los hechos.',body,head,'balance-de-preguntas/'),encoding='utf-8')


def generate_esquemas_juego():
    field = '<rect x="10" y="10" width="740" height="280" rx="14" fill="#17452e"/><path d="M380 10v280m-370-140h740" stroke="#e1ece3" stroke-opacity=".38" stroke-width="2"/><circle cx="380" cy="150" r="44" fill="none" stroke="#e1ece3" stroke-opacity=".38" stroke-width="2"/><path d="M10 87h66v126H10m740-126h-66v126h66" fill="none" stroke="#e1ece3" stroke-opacity=".45" stroke-width="2"/>'
    def dot(x,y,color='#f4f7f1',radius=11):
        return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" stroke="#10291e" stroke-width="2"/>'
    diagrams = [
        ('amplitud','Amplitud','Abrir el campo','Los jugadores de banda ofrecen líneas exteriores para ensanchar la defensa. El dibujo muestra una idea de ocupación, no una estructura observada en un equipo.',
         dot(180,150)+dot(300,150)+dot(480,75)+dot(480,225)+dot(575,150)+dot(575,65,'#ff6a2b')+dot(575,235,'#ff6a2b')+
         '<path d="M315 146Q395 95 464 78M315 154Q395 205 464 222" fill="none" stroke="#ff6a2b" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 11"/>'),
        ('presion','Presión','Orientar la salida','Un grupo reduce líneas de pase y guía la salida rival hacia una zona. Las flechas indican una intención colectiva, no la presión exacta de un partido.',
         dot(150,105)+dot(180,200)+dot(300,150)+dot(450,80,'#ff6a2b')+dot(455,150,'#ff6a2b')+dot(450,220,'#ff6a2b')+dot(575,150)+
         '<path d="M425 88Q355 95 315 137M425 150H316M425 212Q355 205 315 163" fill="none" stroke="#ff6a2b" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 11"/>'),
        ('transicion','Transición','Avanzar tras recuperar','Después de recuperar el balón, una salida vertical y apoyos por delante pueden aprovechar el espacio. Es una secuencia didáctica, no una jugada reconstruida.',
         dot(210,90)+dot(240,210)+dot(355,150,'#ff6a2b',8)+dot(455,95)+dot(465,205)+dot(590,150)+
         '<path d="M365 146Q414 108 448 98M365 154Q414 192 456 202M365 150H562" fill="none" stroke="#ff6a2b" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 11"/>')]
    layers=[]
    cards=[]
    for key,title,heading,description,actions in diagrams:
        actions=actions.replace('fill="none" stroke="#ff6a2b"','fill="none" stroke="#ff6a2b" marker-end="url(#flecha-'+key+')"')
        layers.append('<g data-fase-campo="'+key+'"'+('' if key=='amplitud' else ' style="display:none"')+'>'+actions+'</g>')
        cards.append('<article class="tarjeta-lectura-campo"><p class="etiqueta">'+escape(title)+'</p><h2>'+escape(heading)+'</h2><p>'+escape(description)+'</p></article>')
    markers=''.join('<marker id="flecha-'+key+'" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 8 4 0 8z" fill="#ff6a2b"/></marker>' for key,_,_,_,_ in diagrams)
    field_view=('<section class="campo-lecturas" data-campo-lecturas aria-labelledby="titulo-campo-lecturas"><p class="etiqueta">Una misma cancha · tres lecturas</p><h2 id="titulo-campo-lecturas">Cambia de fase</h2>'
        '<p>Activa cada vista para comparar cómo cambia el esquema. Es un recurso didáctico: no representa una jugada ni una disposición de un equipo.</p>'
        '<div class="campo-lecturas-controles" data-campo-controles role="group" aria-label="Elegir una fase del juego" hidden>'+''.join('<button type="button" class="boton" data-elegir-fase="'+key+'" aria-pressed="'+('true' if i==0 else 'false')+'">'+escape(title)+'</button>' for i,(key,title,_,_,_) in enumerate(diagrams))+'</div>'
        '<figure><svg class="campo-lecturas-svg" viewBox="0 0 760 300" role="img" aria-labelledby="titulo-vista-campo descripcion-vista-campo"><title id="titulo-vista-campo">Vista de amplitud</title><desc id="descripcion-vista-campo">'+escape(diagrams[0][3])+'</desc><defs>'+markers+'</defs>'+field+''.join(layers)+'</svg>'
        '<figcaption><strong data-campo-nombre>Amplitud · Abrir el campo</strong><span data-campo-descripcion>'+escape(diagrams[0][3])+'</span></figcaption></figure></section>')
    body=('<p>Estos esquemas resumen tres ideas de juego en una imagen. Las flechas sirven para explicar relaciones y recorridos posibles; no son coordenadas de futbolistas ni una reconstrucción de un partido.</p>'
          '<div class="leyenda-visual-global" aria-label="Leyenda de los esquemas"><span><i class="marca-visual"></i>Círculo: jugador o elemento del esquema</span><span><i class="marca-visual destacado"></i>Naranja: balón o punto de atención</span><span><i class="marca-visual media"></i>Flecha punteada: recorrido ilustrativo</span></div>'
          +field_view+'<div class="lecturas-campo">'+''.join(cards)+'</div>'
          '<aside class="fuera-de-plano"><h2>Qué representan las marcas</h2><p>Los círculos y las trayectorias son ilustrativos. Solo se dibujarán posiciones observadas cuando una fuente aporte datos de seguimiento adecuados y la página lo indique.</p></aside>'
          '<p><a class="enlace-editorial" href="../conceptos/">Volver al glosario visual →</a></p><script src="../assets/campo-fases.js?v=20261027a" defer></script>')
    head='<link rel="stylesheet" href="../assets/ideas-editoriales.css?v=20261027f">'
    folder=ROOT/'esquemas-del-juego'
    folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(page('El juego en esquema','Tres esquemas tácticos didácticos: amplitud, presión y transición, sin atribuir posiciones no observadas.',body,head,'esquemas-del-juego/'),encoding='utf-8')


def generate_galeria_visual(page):
    from segunda_edicion import match_statistics, percentage_text, fixture_for
    season=json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    latest=max(season['partidos'],key=lambda row:int(row['jornada']))
    month_names=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
    date_parts=latest['fecha'].split('-')
    date_label=f"{int(date_parts[2])} {month_names[int(date_parts[1])-1]} {date_parts[0]}"
    score=(f"{latest['goles_contra']}–{latest['goles_favor']}" if latest['sede']=='Fuera' else f"{latest['goles_favor']}–{latest['goles_contra']}")
    rival_first=latest['sede']=='Fuera'
    match_title=(latest['rival']+' – Real Zaragoza' if rival_first else 'Real Zaragoza – '+latest['rival'])
    items=[
        ('temporada','Temporada · Real Zaragoza','Jornada a jornada','Resultados y evolución del equipo en Primera Federación.','../assets/compartir/proyectos-real-zaragoza-index.png','../proyectos/real-zaragoza/',['png']),
        ('jornada',f"Jornada {int(latest['jornada']):02d} · {date_label}",match_title+' · '+score,'Marcador final del último partido registrado. La ficha enlaza al análisis y a sus fuentes.','../assets/ilustraciones/resultado-real-zaragoza-ultima-jornada.png','../proyectos/real-zaragoza/ultimo-partido.html',['png','svg']),
        ('modelo','Simulación · Grupo 2','10.000 temporadas','Probabilidades de ascenso, playoff y descenso con método y corte publicados.','../assets/compartir/proyectos-real-zaragoza-simulacion.png','../proyectos/real-zaragoza/simulacion.html',['png']),
        ('modelo','Investigación · Liga F','El peligro empieza antes del último pase','Modelo propio de amenaza esperada con datos de 2023/24.','../assets/compartir/proyectos-liga-f-xt-index.png','../proyectos/liga-f-xt/',['png']),
        ('territorio','Fútbol femenino · Territorio','Una base más amplia','Mapa y tasas de licencias por comunidad autónoma.','../assets/compartir/proyectos-futbol-femenino-index.png','../proyectos/futbol-femenino/',['png']),
        ('concepto','Divulgación · xG','xG, sin líos','Una guía visual para interpretar la calidad de las ocasiones.','../assets/compartir/proyectos-xg-index.png','../proyectos/xg/',['png']),
        ('esquema','Esquemas de juego','Cambia de fase','Amplitud, presión y transición en un campo didáctico.','../assets/compartir/esquemas-del-juego-index.png','../esquemas-del-juego/',['png']),
        ('edicion','Edición visual 2026','Cuatro proyectos, una lámina','Resumen vectorial anual con formatos para redes y una copia lista para imprimir.','../assets/ilustraciones/anuario-visual-2026-cuadrado.png','../assets/ilustraciones/anuario-visual-2026.svg',['png','svg','pdf']),
    ]
    fixture=fixture_for(season,latest)
    stats=match_statistics(latest,fixture)
    if stats:
        extra=(f" A puerta: {stats['a_puerta_zaragoza']}–{stats['a_puerta_rival']}." if 'a_puerta_zaragoza' in stats else '')
        items.append(('estadistica',f"Estadísticas · J{int(latest['jornada']):02d}",'Posesión y tiros del partido',f"El Zaragoza tuvo {percentage_text(stats['posesion_pct'])} % de posesión y registró {stats['tiros_zaragoza']} tiros; {latest['rival']}, {stats['tiros_rival']}.{extra}",'../assets/ilustraciones/estadisticas-real-zaragoza-ultima-jornada.png','../proyectos/real-zaragoza/ultimo-partido.html',['png','svg']))
    category_counts={key:sum(item[0]==key for item in items) for key,_,_,_,_,_,_ in items}
    categories=[('todos','Todo',len(items))]+[(key,label,category_counts[key]) for key,label in [('temporada','Temporada'),('jornada','Jornadas'),('estadistica','Estadísticas'),('modelo','Modelos'),('territorio','Territorio'),('concepto','Conceptos'),('esquema','Esquemas'),('edicion','Edición')] if category_counts.get(key,0)>0]
    formats=[('todos','Todos',len(items))]+[(key,key.upper(),sum(key in item[6] for item in items)) for key in ['png','svg','pdf'] if any(key in item[6] for item in items)]
    category_buttons='<div class="filtros-galeria-visual" data-filtros-galeria="coleccion" role="group" aria-label="Filtrar por colección" hidden>'+''.join('<button type="button" data-filtro-coleccion="'+key+'" aria-pressed="'+('true' if i==0 else 'false')+'">'+label+' <span>'+str(count)+'</span></button>' for i,(key,label,count) in enumerate(categories))+'</div>'
    format_buttons='<div class="filtros-galeria-visual filtros-formato-galeria" data-filtros-galeria="formato" role="group" aria-label="Filtrar por formato" hidden>'+''.join('<button type="button" data-filtro-formato="'+key.lower()+'" aria-pressed="'+('true' if i==0 else 'false')+'">'+label+' <span>'+str(count)+'</span></button>' for i,(key,label,count) in enumerate(formats))+'</div>'
    def downloads(item):
        key,_,_,_,_,_,available=item
        if key!='edicion':
            path=item[4]
            if key=='jornada':
                return '<a href="'+path+'" download>Descargar PNG</a><a href="../assets/ilustraciones/resultado-real-zaragoza-ultima-jornada.svg" download>Descargar SVG</a>'
            if key=='estadistica':
                return '<a href="'+path+'" download>Descargar PNG</a><a href="../assets/ilustraciones/estadisticas-real-zaragoza-ultima-jornada.svg" download>Descargar SVG</a>'
            return '<a href="'+path+'" download>Descargar PNG</a>'
        links=[('PNG','../assets/ilustraciones/anuario-visual-2026-cuadrado.png'),('PNG vertical','../assets/ilustraciones/anuario-visual-2026-vertical.png'),('PNG apaisado','../assets/ilustraciones/anuario-visual-2026-apaisado.png'),('SVG','../assets/ilustraciones/anuario-visual-2026.svg'),('SVG vertical','../assets/ilustraciones/anuario-visual-2026-vertical.svg'),('SVG apaisado','../assets/ilustraciones/anuario-visual-2026-apaisado.svg'),('PDF A4','../assets/ilustraciones/anuario-visual-2026-impresion.pdf')]
        return ''.join('<a href="'+path+'" download>'+label+'</a>' for label,path in links)
    def update_metadata(item):
        return ' data-jornada="'+str(latest['jornada'])+'" data-fecha-partido="'+latest['fecha']+'"' if item[0] in ('jornada','estadistica') else ''
    cards='<div class="rejilla-galeria-visual" data-galeria-visual>'+''.join('<article class="tarjeta-galeria-visual" data-coleccion-visual="'+item[0]+'"'+update_metadata(item)+' data-formatos-visual="'+' '.join(item[6])+'"><a class="imagen-galeria-visual" href="'+item[4]+'"><img src="'+item[4]+'" width="'+('1080' if item[0]=='edicion' else '1200')+'" height="'+('1080' if item[0]=='edicion' else '630')+'" alt="Gráfico de '+escape(item[2].lower())+'" loading="lazy"></a><div><p class="etiqueta">'+escape(item[1])+'</p><h2>'+escape(item[2])+'</h2><p>'+escape(item[3])+'</p><a class="enlace-editorial" href="'+item[5]+'">Abrir análisis →</a><details class="descargas-galeria-visual"><summary>Ver formatos y descargas</summary><div>'+downloads(item)+'</div></details></div></article>' for item in items)+'</div>'
    body=('<p>Una selección de portadas y gráficos propios. Filtra por colección o formato, abre el análisis de origen o descarga la pieza.</p><p><a class="enlace-editorial" href="../archivo-visual/">Consultar el archivo de gráficos por jornada →</a></p>'+category_buttons+format_buttons+'<p class="recuento-galeria-visual" data-recuento-galeria role="status" aria-live="polite">'+str(len(items))+' piezas</p>'+cards+'<noscript><p>Se muestran todas las piezas y sus enlaces de descarga; los filtros requieren JavaScript.</p></noscript>')
    head='<link rel="stylesheet" href="../assets/ideas-editoriales.css?v=20261027f"><script src="../assets/galeria-visual.js?v=20261027b" defer></script>'
    folder=ROOT/'galeria-visual'
    folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(page('Galería visual de Línea de pase','Una colección ligera de gráficos, láminas y portadas de los proyectos de Línea de pase.',body,head,'galeria-visual/'),encoding='utf-8')


def generate_archivo_visual(page):
    from segunda_edicion import match_statistics, fixture_for, percentage_text, visual_season, archive_round_name
    data=json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    rows=[]
    month_names=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
    sorted_matches=sorted(data['partidos'],key=lambda item:int(item['jornada']),reverse=True)
    season_names=sorted({visual_season(match) for match in sorted_matches},reverse=True)
    results_path=ROOT/'analisis/real-zaragoza/datos/entrada/grupo2_resultados.csv'
    rival_aliases={'Cartagena':'FC Cartagena','Antequera':'Antequera CF','Gimnàstic':'Gimnàstic de Tarragona','Gimnastic':'Gimnàstic de Tarragona','Real Jaen':'Real Jaén','Hercules':'Hércules','Alcorcon':'Alcorcón'}
    rival_form={}
    if results_path.exists():
        with results_path.open(encoding='utf-8-sig',newline='') as source:
            for result in csv.DictReader(source):
                try:
                    home_goals=int(result['goles_local']); away_goals=int(result['goles_visitante']); round_num=int(result['jornada'])
                except (KeyError,TypeError,ValueError):
                    continue
                date=result.get('fecha','')
                home=rival_aliases.get(result.get('local',''),result.get('local',''))
                away=rival_aliases.get(result.get('visitante',''),result.get('visitante',''))
                try:
                    date_type.fromisoformat(date)
                except ValueError:
                    continue
                if round_num<1 or home_goals<0 or away_goals<0 or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',date) or not home or not away or home==away:
                    continue
                if home!='Real Zaragoza': rival_form.setdefault(home,[]).append({'jornada':round_num,'fecha':date,'rival':away,'goles_favor':home_goals,'goles_contra':away_goals})
                if away!='Real Zaragoza': rival_form.setdefault(away,[]).append({'jornada':round_num,'fecha':date,'rival':home,'goles_favor':away_goals,'goles_contra':home_goals})
    rival_form={team:sorted(matches,key=lambda match:(match['fecha'],match['jornada']),reverse=True)[:5] for team,matches in rival_form.items()}
    rival_form_json=json.dumps(rival_form,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    stats_by_season={season:[] for season in season_names}
    for match in sorted_matches:
        round_num=int(match['jornada']); round_name=archive_round_name(match,sorted_matches); season=visual_season(match)
        date_parts=match['fecha'].split('-'); date_label=f'{int(date_parts[2])} {month_names[int(date_parts[1])-1]} {date_parts[0]}'
        score=f"{match['goles_favor']}–{match['goles_contra']}"; stats=match_statistics(match,fixture_for(data,match))
        if stats: stats_by_season[season].append(stats)
        possession=percentage_text(stats['posesion_pct'])+' %' if stats else '—'
        shots=f"{stats['tiros_zaragoza']}–{stats['tiros_rival']}" if stats else '—'
        on_target=f"{stats['a_puerta_zaragoza']}–{stats['a_puerta_rival']}" if stats and 'a_puerta_zaragoza' in stats else '—'
        coverage=('<span class="estado-cobertura completa"><span aria-hidden="true">✓</span> Ficha completa</span>' if stats else '<span class="estado-cobertura incompleta">Sin métricas validadas</span>')
        image_links=('<a href="../assets/ilustraciones/archivo-jornadas/'+round_name+'.png" download>PNG</a> · <a href="../assets/ilustraciones/archivo-jornadas/'+round_name+'.svg" download>SVG</a>')
        if stats:
            image_links+=' · <a href="../assets/ilustraciones/estadisticas-jornadas/'+round_name+'.png" download>Datos PNG</a> · <a href="../assets/ilustraciones/estadisticas-jornadas/'+round_name+'.svg" download>Datos SVG</a>'
        if stats:
            possession_value=str(stats['posesion_pct']); zaragoza_shots=str(stats['tiros_zaragoza']); rival_shots=str(stats['tiros_rival'])
            on_target_z=str(stats.get('a_puerta_zaragoza','')); on_target_r=str(stats.get('a_puerta_rival',''))
        else:
            possession_value=zaragoza_shots=rival_shots=on_target_z=on_target_r=''
        comparison_id=f'{season}|{round_num}'
        rows.append('<tr data-jornada="'+str(round_num)+'" data-comparison-id="'+escape(comparison_id,quote=True)+'" data-asset-stem="'+round_name+'" data-fecha-partido="'+match['fecha']+'" data-temporada="'+escape(season,quote=True)+'" data-rival="'+escape(match['rival'],quote=True)+'" data-sede="'+escape(match['sede'],quote=True)+'" data-goles-zaragoza="'+str(match['goles_favor'])+'" data-goles-rival="'+str(match['goles_contra'])+'" data-completa="'+('1' if stats else '0')+'" data-posesion="'+possession_value+'" data-tiros-zaragoza="'+zaragoza_shots+'" data-tiros-rival="'+rival_shots+'" data-a-puerta-zaragoza="'+on_target_z+'" data-a-puerta-rival="'+on_target_r+'"><th scope="row">J'+f'{round_num:02d}'+'</th><td>'+date_label+'</td><td>'+escape(match['rival'])+'</td><td>'+('Casa' if match['sede']=='Casa' else 'Fuera')+'</td><td>'+score+'</td><td>'+possession+'</td><td>'+shots+'</td><td>'+on_target+'</td><td>'+coverage+'</td><td>'+image_links+'</td></tr>')
    season_options=''.join(f'<option value="{escape(season,quote=True)}">{escape(season)}</option>' for season in season_names)
    rival_options=''.join('<option value="'+escape(name,quote=True)+'">'+escape(name)+'</option>' for name in sorted({m['rival'] for m in sorted_matches},key=str.casefold))
    average_text=lambda value:f'{float(value):.1f}'.replace('.',',')
    summary_cards=[]
    for season_index,season in enumerate(season_names):
        complete_stats=stats_by_season[season]; count=len(complete_stats); heading_id=f'titulo-resumen-{season_index}'
        if not count:
            detail='<p class="nota">Todavía no hay fichas completas para resumir esta temporada.</p>'
        else:
            avg_pos=sum(float(stat['posesion_pct']) for stat in complete_stats)/count
            avg_team_shots=sum(int(stat['tiros_zaragoza']) for stat in complete_stats)/count
            avg_opponent_shots=sum(int(stat['tiros_rival']) for stat in complete_stats)/count
            avg_on_target_team=sum(int(stat['a_puerta_zaragoza']) for stat in complete_stats)/count if all('a_puerta_zaragoza' in stat for stat in complete_stats) else None
            detail=('<dl><div><dt>Posesión del Zaragoza</dt><dd>'+percentage_text(avg_pos)+' %</dd></div><div><dt>Tiros · Zaragoza–rival</dt><dd>'+average_text(avg_team_shots)+'–'+average_text(avg_opponent_shots)+'</dd></div>'+(('<div><dt>Tiros del Zaragoza a puerta</dt><dd>'+average_text(avg_on_target_team)+'</dd></div>') if avg_on_target_team is not None else '')+'</dl>')
        summary_cards.append('<section class="archivo-resumen" aria-labelledby="'+heading_id+'"><div><p class="etiqueta">Muestra disponible · '+escape(season)+'</p><h2 id="'+heading_id+'">La temporada, en números</h2><p>Medias por partido en '+str(count)+' jornadas con ficha completa.</p></div>'+detail+'</section>')
    summary='<div class="archivo-resumenes">'+''.join(summary_cards)+'</div>'
    first=sorted_matches[0]; second=sorted_matches[1] if len(sorted_matches)>1 else sorted_matches[0]
    first_stats=match_statistics(first,fixture_for(data,first)); second_stats=match_statistics(second,fixture_for(data,second))
    comparable_stats=bool(first_stats and second_stats)
    options_a=''.join(f'<option value="{escape(visual_season(match)+"|"+str(int(match["jornada"])),quote=True)}"'+(' selected' if match is first else '')+'>'+f'J{int(match["jornada"]):02d} · '+escape(match['rival'])+' · '+escape(visual_season(match))+'</option>' for match in sorted_matches)
    options_b=''.join(f'<option value="{escape(visual_season(match)+"|"+str(int(match["jornada"])),quote=True)}"'+(' selected' if match is second else '')+'>'+f'J{int(match["jornada"]):02d} · '+escape(match['rival'])+' · '+escape(visual_season(match))+'</option>' for match in sorted_matches)
    def comparison_card(match,slot):
        round_num=int(match['jornada']); round_name=archive_round_name(match,sorted_matches); stats=match_statistics(match,fixture_for(data,match))
        stats_copy=('<p class="comparacion-estadisticas">Posesión '+percentage_text(stats['posesion_pct'])+' % · tiros '+str(stats['tiros_zaragoza'])+'–'+str(stats['tiros_rival'])+'</p>') if comparable_stats and stats else '<p class="comparacion-estadisticas">Las métricas comparadas aparecerán cuando ambas jornadas tengan ficha completa.</p>'
        return '<figure class="comparacion-jornada" data-panel-comparacion="'+slot+'"><img src="../assets/ilustraciones/archivo-jornadas/'+round_name+'.png" width="1200" height="630" loading="lazy" alt="Marcador de J'+f'{round_num:02d} ante '+escape(match['rival'],quote=True)+'"><figcaption>J'+f'{round_num:02d} · '+escape(match['rival'])+' · '+match['fecha']+' · '+escape(visual_season(match))+'</figcaption>'+stats_copy+'</figure>'
    compare_controls=('<section class="archivo-comparar" aria-labelledby="titulo-comparar"><div><p class="etiqueta">Dos jornadas, frente a frente</p><h2 id="titulo-comparar">Comparar marcadores</h2><p>La comparación abre los gráficos históricos y añade métricas solo si ambas fichas están completas.</p></div><div class="archivo-comparar-controles"><label for="comparar-jornada-a">Primera jornada<select id="comparar-jornada-a">'+options_a+'</select></label><label for="comparar-jornada-b">Segunda jornada<select id="comparar-jornada-b">'+options_b+'</select></label><button type="button" class="boton" data-compartir-comparacion>Copiar enlace</button><button type="button" class="boton" data-guardar-comparacion aria-pressed="false">Guardar pareja</button></div><div class="archivo-opciones-tarjeta" data-controles-descarga hidden><label for="formato-comparacion">Formato<select id="formato-comparacion"><option value="apaisado">Apaisado · 1200 × 630</option><option value="cuadrado">Cuadrado · 1080 × 1080</option><option value="vertical">Vertical · 1080 × 1350</option><option value="historias">Historias · 1080 × 1920 · zonas seguras</option><option value="carrusel">Carrusel · 2 diapositivas cuadradas</option></select></label><label for="preset-visual">Plantilla visual<select id="preset-visual" data-preset-selector><option value="">Elegir una plantilla…</option><optgroup label="De Línea de pase"><option value="portada">Portada</option><option value="comparacion-limpia">Comparación limpia</option><option value="historia">Historia</option><option value="social-cuadrada">Social · cuadrada compacta</option><option value="social-vertical">Social · vertical compacta</option></optgroup></select></label><label for="paleta-visual">Paleta de color<select id="paleta-visual" data-paleta-visual><option value="clasica">Verde clásico</option><option value="contraste">Alto contraste</option><option value="papel">Papel cálido</option><option value="monocromo">Blanco y negro · impresión</option></select></label><label for="encuadre-visual">Encuadre<select id="encuadre-visual" data-encuadre-visual><option value="equilibrado">Equilibrado</option><option value="protagonista">Marcador protagonista</option></select></label><label for="densidad-visual">Densidad<select id="densidad-visual" data-densidad-visual><option value="completa">Completa</option><option value="resultado">Resultado y contexto</option><option value="esencial">Solo marcador</option></select></label><p class="archivo-aviso-contraste contraste-correcto" data-aviso-contraste role="status" aria-live="polite">Comprobando contraste…</p><div class="archivo-presets-personales"><label for="nombre-preset">Guardar mis opciones<input id="nombre-preset" type="text" maxlength="28" placeholder="Nombre de la plantilla"></label><button type="button" class="boton" data-guardar-preset>Guardar plantilla actual</button><button type="button" class="boton" data-borrar-preset disabled>Borrar plantilla personal</button><p class="nota">Hasta 6 plantillas guardadas en este navegador.</p></div><div class="archivo-miniaturas-formatos" data-miniaturas-formatos><p class="archivo-miniaturas-titulo">Elige formato con una vista previa</p><div class="archivo-miniaturas-grid"><button type="button" data-miniatura-formato="apaisado" aria-pressed="true"><img width="132" height="69" alt="Vista previa apaisada"><span>Apaisado</span><small>1200 × 630</small></button><button type="button" data-miniatura-formato="cuadrado" aria-pressed="false"><img width="132" height="132" alt="Vista previa cuadrada"><span>Cuadrado</span><small>1080 × 1080</small></button><button type="button" data-miniatura-formato="vertical" aria-pressed="false"><img width="132" height="165" alt="Vista previa vertical"><span>Vertical</span><small>1080 × 1350</small></button><button type="button" data-miniatura-formato="historias" aria-pressed="false"><span class="archivo-miniatura-marco" data-miniatura-zonas><img width="82" height="145" alt="Vista previa para historias"><span class="archivo-zonas-seguras" aria-hidden="true"></span></span><span>Historias</span><small>1080 × 1920</small></button><button type="button" data-miniatura-formato="carrusel" aria-pressed="false"><img width="132" height="132" alt="Vista previa del carrusel"><span>Carrusel</span><small>2 × 1080</small></button></div></div><section class="archivo-hoja-contacto" aria-labelledby="titulo-hoja-contacto"><p class="archivo-miniaturas-titulo" id="titulo-hoja-contacto">Hoja de contacto · compara las plantillas</p><div class="archivo-hoja-grid"><button type="button" data-hoja-plantilla="portada" aria-pressed="false"><img width="120" height="120" alt="Vista previa: Portada"><span>Portada</span></button><button type="button" data-hoja-plantilla="comparacion-limpia" aria-pressed="false"><img width="120" height="120" alt="Vista previa: Comparación limpia"><span>Comparación limpia</span></button><button type="button" data-hoja-plantilla="historia" aria-pressed="false"><img width="120" height="120" alt="Vista previa: Historia"><span>Historia</span></button><button type="button" data-hoja-plantilla="social-cuadrada" aria-pressed="false"><img width="120" height="120" alt="Vista previa: Social cuadrada"><span>Social cuadrada</span></button><button type="button" data-hoja-plantilla="social-vertical" aria-pressed="false"><img width="120" height="120" alt="Vista previa: Social vertical"><span>Social vertical</span></button></div><p class="nota">Pulsa una miniatura para aplicar sus opciones de formato.</p></section><section class="archivo-comparar-estilos" data-comparar-estilos aria-label="Comparar encuadres y densidad"><p class="archivo-miniaturas-titulo">Compara dos estilos antes de descargar</p><p class="nota">La comparación no cambia tus opciones de descarga.</p><div class="archivo-vistas-estilo"><figure><figcaption>Opción A</figcaption><div class="archivo-controles-estilo"><label for="vista-a-encuadre">Encuadre<select id="vista-a-encuadre" data-vista-encuadre="a"><option value="equilibrado" selected>Equilibrado</option><option value="protagonista">Marcador protagonista</option></select></label><label for="vista-a-densidad">Densidad<select id="vista-a-densidad" data-vista-densidad="a"><option value="completa" selected>Completa</option><option value="resultado">Resultado y contexto</option><option value="esencial">Solo marcador</option></select></label></div><img data-vista-estilo="a" width="240" height="180" alt="Vista previa de la opción A"></figure><figure><figcaption>Opción B</figcaption><div class="archivo-controles-estilo"><label for="vista-b-encuadre">Encuadre<select id="vista-b-encuadre" data-vista-encuadre="b"><option value="equilibrado">Equilibrado</option><option value="protagonista" selected>Marcador protagonista</option></select></label><label for="vista-b-densidad">Densidad<select id="vista-b-densidad" data-vista-densidad="b"><option value="completa">Completa</option><option value="resultado">Resultado y contexto</option><option value="esencial" selected>Solo marcador</option></select></label></div><img data-vista-estilo="b" width="240" height="180" alt="Vista previa de la opción B"></figure></div></section><div class="archivo-texto-alternativo"><label for="texto-alternativo">Texto alternativo<textarea id="texto-alternativo" data-texto-alternativo maxlength="240" rows="3" aria-describedby="ayuda-texto-alternativo"></textarea></label><div class="archivo-acciones-preferencias"><button type="button" class="boton" data-generar-texto-alternativo>Actualizar desde el marcador</button><button type="button" class="boton" data-copiar-texto-alternativo>Copiar texto alternativo</button></div><p class="nota" id="ayuda-texto-alternativo">El SVG guarda este texto y el ZIP social incluye un archivo de texto para acompañar las imágenes.</p></div><label class="archivo-incluir-metricas"><input type="checkbox" data-incluir-metricas checked> Incluir métricas completas en la tarjeta</label><label class="archivo-incluir-metricas"><input type="checkbox" data-incluir-pie checked> Añadir pie con competición y marcadores</label><label class="archivo-incluir-metricas"><input type="checkbox" data-sin-cabecera> Diseño sin cabecera</label><label class="archivo-incluir-metricas"><input type="checkbox" data-mostrar-marca checked> Mostrar marca Línea de pase</label><div class="archivo-acciones-preferencias"><button type="button" class="boton" data-copiar-imagen>Copiar imagen</button><button type="button" class="boton" data-restablecer-opciones>Restablecer opciones</button></div><p class="nota archivo-aviso-stories" data-aviso-stories hidden>La composici&#243;n reserva el 17 % superior y el 17 % inferior para la interfaz de las historias. <label class="archivo-guia-zonas"><input type="checkbox" data-guia-zonas> Mostrar las zonas que puede cubrir la interfaz en la miniatura (no se exportan)</label></p><p class="nota archivo-aviso-carrusel" data-aviso-carrusel hidden>El ZIP contiene dos diapositivas cuadradas: una por partido, en el orden seleccionado.</p><div class="archivo-contexto-carrusel" data-controles-contexto-carrusel hidden><label for="frase-carrusel">Frase opcional para la primera diapositiva<input id="frase-carrusel" type="text" maxlength="72" placeholder="Dos jornadas, cara a cara"></label><div><label for="ejemplos-frase-carrusel">Ejemplos neutrales</label><select id="ejemplos-frase-carrusel"><option value="">Elegir una frase…</option><option value="Dos jornadas, cara a cara">Dos jornadas, cara a cara</option><option value="El marcador de un vistazo">El marcador de un vistazo</option><option value="Comparación de resultados">Comparación de resultados</option></select><p data-contador-frase-carrusel>0/72 caracteres</p></div></div><figure class="archivo-preview-carrusel" data-preview-carrusel hidden><figcaption>Vista previa · primera diapositiva</figcaption><img data-preview-carrusel-img width="320" height="320" alt="Vista previa de la primera diapositiva del carrusel"></figure><section class="archivo-mapa-temporada" aria-labelledby="titulo-mapa-temporada"><div><p class="archivo-miniaturas-titulo">Una vista del curso</p><h3 id="titulo-mapa-temporada">Mapa de la temporada</h3><p>Todos los marcadores disponibles, en orden de jornada. Las métricas solo se incluyen en partidos con ficha validada; si la campaña es larga, se reparte en varias láminas.</p></div><div class="archivo-kit-controles"><label for="temporada-mapa">Temporada<select id="temporada-mapa" data-temporada-mapa></select></label><label for="rival-mapa">Rival<select id="rival-mapa" data-rival-mapa><option value="">Todos los rivales</option></select></label><label for="desde-mapa">Desde<input id="desde-mapa" data-desde-mapa type="date"></label><label for="hasta-mapa">Hasta<input id="hasta-mapa" data-hasta-mapa type="date"></label><label for="formato-mapa">Tamaño<select id="formato-mapa" data-formato-mapa><option value="cuadrado">Cuadrado · 1080 × 1080</option><option value="vertical">Vertical · 1080 × 1350</option><option value="historias">Historias · 1080 × 1920</option></select></label><label for="tipo-mapa">Archivo<select id="tipo-mapa" data-tipo-mapa><option value="png">PNG</option><option value="webp" selected>WebP · ligero</option><option value="svg">SVG</option></select></label><button type="button" class="boton" data-descargar-mapa>Descargar mapa</button><button type="button" class="boton" data-descargar-carrusel-temporada>Descargar carrusel de temporada · 3 láminas</button></div><p class="nota">Los filtros afectan a las jornadas del mapa. El balance y el carrusel usan todos los resultados publicados.</p><section class="archivo-forma-temporada" aria-labelledby="titulo-forma-temporada"><h4 id="titulo-forma-temporada">Forma reciente</h4><div class="archivo-forma-comparada"><div><h5>Real Zaragoza · últimos 5</h5><ol data-forma-reciente aria-label="Últimos cinco resultados del Real Zaragoza"></ol><p data-racha-temporada role="status" aria-live="polite"></p></div><div><h5 data-forma-rival-titulo>Rival seleccionado</h5><ol data-forma-rival aria-label="Últimos resultados publicados del rival"></ol><p data-forma-rival-estado role="status" aria-live="polite">Selecciona un rival para comparar la muestra disponible.</p></div></div></section><div class="archivo-compartir-mapa"><button type="button" class="boton" data-compartir-mapa>Copiar enlace a esta selección</button><p data-estado-compartir-mapa role="status" aria-live="polite"></p></div><section class="archivo-enlaces-guardados" aria-labelledby="titulo-enlaces-guardados"><h4 id="titulo-enlaces-guardados">Enlaces guardados</h4><div><label for="nombre-enlace-mapa">Nombre breve<input id="nombre-enlace-mapa" data-nombre-enlace-mapa type="text" maxlength="28" placeholder="Por ejemplo, Real Murcia"></label><button type="button" class="boton" data-guardar-enlace-mapa>Guardar selección</button></div><ul data-enlaces-guardados aria-label="Enlaces de mapa guardados" hidden></ul><div class="archivo-enlaces-herramientas"><button type="button" class="boton" data-exportar-enlaces-mapa>Exportar paquete de selecciones</button><button type="button" class="boton" data-importar-enlaces-mapa>Importar JSON o ZIP</button><input type="file" data-archivo-enlaces-mapa accept=".json,.zip,application/json,application/zip" aria-label="Archivo JSON o ZIP de selecciones" hidden></div><div class="archivo-qr-enlace"><label for="nombre-qr-enlace">Pie opcional para el QR<input id="nombre-qr-enlace" data-nombre-qr-enlace type="text" maxlength="28" placeholder="Por ejemplo, Mapa de temporada"></label><label for="color-qr-enlace">Color<select id="color-qr-enlace" data-color-qr-enlace><option value="marca">Verde de Línea de pase</option><option value="tinta">Tinta oscura</option></select></label><label for="tamano-qr-enlace">Tamaño SVG<select id="tamano-qr-enlace" data-tamano-qr-enlace><option value="px">Digital · píxeles</option><option value="40mm">Impresión · 40 mm</option><option value="60mm">Impresión · 60 mm</option></select></label><label for="fondo-qr-pdf">Fondo PDF<select id="fondo-qr-pdf" data-papel-impresion-qr><option value="blanco">Papel blanco · ahorra tinta</option><option value="suave">Verde suave</option></select></label><button type="button" class="boton" data-generar-qr-enlace>Generar QR del enlace</button><button type="button" class="boton" data-descargar-qr-enlace disabled>Descargar QR SVG</button><button type="button" class="boton" data-copiar-qr-enlace disabled>Copiar imagen QR</button><button type="button" class="boton" data-descargar-qr-a4 disabled>Descargar hoja A4 &middot; QR de 40 y 60 mm</button><button type="button" class="boton" data-descargar-qr-a4-apaisado disabled>Hoja A4 apaisada &middot; QR y marcadores</button><button type="button" class="boton" data-descargar-qr-a5 disabled>Descargar QR en hoja A5</button><figure hidden><figcaption>Código QR de la selección actual</figcaption><img data-vista-qr-enlace width="176" height="176" alt="Código QR para abrir la selección del mapa" hidden></figure><p class="nota archivo-qr-calidad" data-calidad-qr role="status" aria-live="polite">Comprobando contraste y margen de lectura&hellip;</p></div><section class="archivo-qr-hoja" aria-labelledby="titulo-hoja-qr"><div><p class="etiqueta">Vista de impresi&oacute;n</p><h5 id="titulo-hoja-qr">Hojas A4 a tama&ntilde;o real</h5><p>En m&oacute;vil, abre la maqueta cuando quieras verla completa. El PDF conserva las medidas del QR; selecciona escala 100 % al imprimir. El fondo blanco reduce el uso de tinta.</p></div><details class="archivo-qr-vistas" data-detalles-vista-qr open><summary data-resumen-vistas-qr>Mostrar las maquetas A4</summary><div class="archivo-qr-a4-preview" data-vista-hoja-qr data-estado="cargando" data-papel="blanco"><header><span>L&Iacute;NEA DE PASE / ARCHIVO VISUAL</span><strong>Una temporada, dos formas de verla</strong><p data-qr-hoja-titulo>Selecci&oacute;n actual del mapa</p></header><div class="archivo-qr-a4-codigos"><figure><div data-qr-hoja-codigo data-tamano="60"></div><figcaption><strong>60 mm</strong><span>Gran formato</span></figcaption></figure><figure><div data-qr-hoja-codigo data-tamano="40"></div><figcaption><strong>40 mm</strong><span>Formato compacto</span></figcaption></figure></div><div class="archivo-qr-a4-pie">IMPRIMIR AL 100 % <span>&middot;</span> PAPEL A4</div></div><div class="archivo-qr-a4-horizontal" data-vista-hoja-qr-horizontal data-papel="blanco"><header><span>L&Iacute;NEA DE PASE / COMPARACI&Oacute;N</span><strong>Dos jornadas, una lectura</strong><p data-qr-hoja-horizontal-titulo>Selecci&oacute;n actual del mapa</p></header><div class="archivo-qr-horizontal-cuerpo"><div class="archivo-qr-horizontal-codigo" data-qr-hoja-codigo data-tamano="60"></div><div class="archivo-qr-horizontal-partidos"><article><span data-qr-hoja-partido-titulo="a">Primera jornada</span><strong data-qr-hoja-partido-marcador="a">Selecciona una jornada</strong><small data-qr-hoja-partido-sede="a"></small></article><article><span data-qr-hoja-partido-titulo="b">Segunda jornada</span><strong data-qr-hoja-partido-marcador="b">Selecciona una jornada</strong><small data-qr-hoja-partido-sede="b"></small></article></div></div><div class="archivo-qr-a4-pie">60 mm &middot; IMPRIMIR AL 100 % &middot; PAPEL A4</div></div></details><label class="archivo-qr-confirmacion"><input type="checkbox" data-confirmar-escala-qr> He seleccionado tama&ntilde;o real o escala 100 % en el cuadro de impresi&oacute;n</label></section><p class="nota" data-estado-enlaces-guardados role="status" aria-live="polite">Hasta seis selecciones, guardadas solo en este navegador.</p></section><div class="archivo-kit-controles" data-controles-lamina hidden><label for="lamina-mapa">Lámina<select id="lamina-mapa" data-lamina-mapa></select></label></div><div class="archivo-texto-alternativo archivo-alt-mapa"><label for="texto-mapa">Texto alternativo del póster<textarea id="texto-mapa" data-texto-mapa maxlength="1000" rows="3"></textarea></label><button type="button" class="boton" data-restablecer-texto-mapa>Actualizar desde los resultados</button></div><figure class="archivo-preview-mapa"><figcaption data-preview-mapa-caption>Vista previa · lámina 1</figcaption><img data-preview-mapa-img width="320" height="320" alt="Vista previa del mapa de temporada"></figure><p class="nota" data-estado-mapa role="status" aria-live="polite"></p></section><section class="archivo-pesos-kit" aria-labelledby="titulo-pesos-kit"><h3 id="titulo-pesos-kit">Peso de las exportaciones</h3><p class="nota">Tamaño exacto calculado en este navegador para el diseño actual.</p><div data-kit-estimaciones role="status" aria-live="polite">Calculando tamaños…</div></section><div class="archivo-kit-social"><label for="formato-kit">Formato del kit<select id="formato-kit" data-formato-kit><option value="png" selected>PNG · compatible</option><option value="webp">WebP · ligero</option><option value="svg">SVG · vectorial</option></select></label><button type="button" class="boton" data-descargar-kit>Descargar kit social</button><button type="button" class="boton" data-imprimir-social>Plantilla imprimible &middot; SVG A4</button><label for="variante-hoja-contacto">Variante A4<select id="variante-hoja-contacto" data-variante-hoja-contacto><option value="todos" selected>Todas · 3 formatos</option><option value="cuadrado">Cuadrada</option><option value="vertical">Vertical</option><option value="historias">Historias</option></select></label><button type="button" class="boton" data-imprimir-hoja-contacto>Hoja de contacto &middot; 3 formatos</button><button type="button" class="boton" data-imprimir-hoja-contacto-pdf>Hoja de contacto &middot; PDF vectorial</button><button type="button" class="boton" data-imprimir-hoja-directa>Imprimir hoja A4</button><label for="modo-impresion-a5">Salida A5<select id="modo-impresion-a5" data-modo-impresion-a5><option value="color" selected>Color</option><option value="monocromo">Monocromo &middot; bajo consumo</option><option value="fotocopia">Alto contraste &middot; fotocopia</option></select></label><button type="button" class="boton" data-imprimir-comparacion-a5>Comparaci&oacute;n compacta &middot; PDF A5</button><button type="button" class="boton" data-imprimir-a5-directa>Imprimir A5</button><details class="archivo-a5-preview"><summary>Previsualizar ficha A5</summary><figure><figcaption data-caption-a5>A5 · color · escala real</figcaption><img data-preview-a5 width="296" height="420" loading="lazy" alt="Vista previa de la comparación A5 para imprimir"></figure><p class="nota">Revisa la legibilidad y el acabado elegido antes de imprimir.</p></details><button type="button" class="boton" data-restablecer-impresion>Restablecer preferencias de impresión</button><p class="nota" data-estado-preferencias-impresion role="status" aria-live="polite">Las opciones de papel y salida se guardan en este navegador.</p><label for="orientacion-hoja-social">Orientaci&oacute;n A4<select id="orientacion-hoja-social" data-orientacion-hoja-social><option value="vertical" selected>Vertical</option><option value="apaisado">Apaisada</option></select></label><label for="papel-impresion-social">Papel<select id="papel-impresion-social" data-papel-impresion-social><option value="normal" selected>Normal &middot; margen 10 mm</option><option value="fotografico">Fotogr&aacute;fico &middot; margen 6 mm</option></select></label><details class="archivo-hoja-impresion-preview"><summary>Vista previa compacta de la hoja A4</summary><figure><figcaption data-caption-hoja-contacto>A4 vertical &middot; papel normal, margen de 10 mm</figcaption><img data-preview-hoja-contacto alt="Vista previa de la hoja A4 con tres formatos sociales, marcas de corte y l&iacute;mite seguro discontinuo"></figure><p class="nota">La l&iacute;nea discontinua naranja indica el &aacute;rea segura. El espacio exterior reserva sitio para el margen y las marcas de corte.</p></details><p class="nota">Puedes ampliar una sola variante en el A4 y comprobar el tama&ntilde;o con la regla de 10 mm. La impresi&oacute;n directa abre el di&aacute;logo del navegador.</p><p class="nota" data-estado-impresion-social role="status" aria-live="polite">Vectorial, con marcas de corte, escala de 10 mm y límite de 300 KB.</p><p class="nota" data-estado-kit role="status" aria-live="polite">Incluye versiones cuadrada, vertical e historias.</p></div><div class="archivo-descargas-individuales" data-descargas-individuales><button type="button" class="boton" data-descargar-comparacion="svg">Descargar SVG</button><button type="button" class="boton" data-descargar-comparacion="png">Descargar PNG</button><button type="button" class="boton" data-descargar-comparacion="webp">Descargar WebP</button></div><div class="archivo-descargas-carrusel" data-descargas-carrusel hidden><button type="button" class="boton" data-descargar-comparacion="svg">Carrusel ZIP · SVG</button><button type="button" class="boton" data-descargar-comparacion="png">Carrusel ZIP · PNG</button><button type="button" class="boton" data-descargar-comparacion="webp">Carrusel ZIP · WebP</button></div></div><div class="archivo-comparar-paneles" data-paneles-comparacion aria-live="polite">'+comparison_card(first,'a')+comparison_card(second,'b')+'</div><p class="archivo-comparar-estado" data-estado-comparacion role="status" aria-live="polite"></p></section>')
    controls=('<div class="archivo-filtros" data-filtros-archivo hidden><label for="archivo-temporada">Temporada<select id="archivo-temporada"><option value="">Todas las temporadas</option>'+season_options+'</select></label><label for="archivo-rival">Rival<select id="archivo-rival"><option value="">Todos los rivales</option>'+rival_options+'</select></label><button type="button" class="boton" data-limpiar-archivo>Limpiar filtros</button><p data-recuento-archivo role="status" aria-live="polite">'+str(len(rows))+' jornadas</p></div>')
    body=('<p>Consulta los resultados, filtra por temporada o rival y compara dos jornadas sin cambiar el marcador vigente de portada.</p>'+summary+compare_controls+controls+'<div class="tabla-comparador"><table><caption>Real Zaragoza · Primera Federación</caption><thead><tr><th scope="col">Jornada</th><th scope="col">Fecha</th><th scope="col">Rival</th><th scope="col">Sede</th><th scope="col">Resultado</th><th scope="col">Posesión</th><th scope="col">Tiros · Zaragoza–rival</th><th scope="col">A puerta</th><th scope="col">Cobertura</th><th scope="col">Gráficos</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div><p class="nota">Los tiros a puerta se muestran solo cuando están disponibles para ambos equipos y cuadran con los tiros totales y los goles. Los filtros y la comparación requieren JavaScript; toda la tabla permanece visible sin él.</p><p><a class="enlace-editorial" href="../">Volver a la portada →</a></p><script type="application/json" id="datos-forma-rivales">'+rival_form_json+'</script>')
    folder=ROOT/'archivo-visual'; folder.mkdir(exist_ok=True)
    head='<script src="../assets/vendor/qrcodegen.js" defer></script><link rel="stylesheet" href="../assets/archivo-visual.css?v=20261028y"><script src="../assets/archivo-visual.js?v=20261028y" defer></script>'
    (folder/'index.html').write_text(page('Archivo visual por jornada','Marcadores y estadísticas del Real Zaragoza, con comparación de jornadas y filtros por temporada y rival.',body,head,'archivo-visual/'),encoding='utf-8')


def generate():
    from experiencia import generate_comparator, generate_selection, generate_news
    generate_comparator(page)
    generate_selection(page)
    generate_news(page)
    from entregas import generate_tools, generate_delivery
    generate_tools(page)
    generate_delivery(page)
    generate_preguntas()
    generate_marcador_a_ciegas()
    generate_datos_revision()
    generate_partidos_espejo()
    generate_reloj_marcador()
    generate_pizarron_jugada()
    generate_mapa_cambios()
    generate_balance_preguntas()
    generate_esquemas_juego()
    from segunda_edicion import generate_map, generate_home, generate_anual_visual, generate_matchday_visual
    generate_map(page)
    generate_anual_visual()
    generate_matchday_visual()
    generate_archivo_visual(page)
    generate_galeria_visual(page)
    generate_home()
    generate_archive()
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
    body += '</div><aside class="entrada-esquemas"><p class="etiqueta">Glosario visual</p><h2>El juego, en tres esquemas</h2><p>Amplitud, presión y transición, explicadas con dibujos didácticos que no simulan posiciones reales.</p><a class="enlace-editorial" href="../esquemas-del-juego/">Ver los esquemas →</a></aside>'
    (ROOT / 'conceptos').mkdir(exist_ok=True)
    concepts_head='<link rel="stylesheet" href="../assets/ideas-editoriales.css?v=20261027e">'
    (ROOT / 'conceptos/index.html').write_text(page('Conceptos para leer el fútbol con datos', 'Una guía breve para entender las cifras, sus límites y cómo se utilizan en los análisis de esta web.', body, concepts_head), encoding='utf-8')


def enrich(raw, file):
    from experiencia import enrich as experiencia
    raw = experiencia(raw, file)
    raw = incorporar_cronologia(raw, file)
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
            links.insert(0, ('reloj-del-marcador/index.html', 'Ver el tiempo de marcador'))
            if file.name == 'jornada-9.html':
                links.insert(1, ('pizarron-de-una-jugada/index.html', 'Ver el pizarrón del gol de la J9'))
                links.insert(2, ('mapa-de-lo-que-cambio/index.html', 'Ver los cambios y el gol de la J9'))
                links.insert(3, ('datos-en-revision/index.html', 'Consultar la discrepancia de tiros de la J9'))
            links.insert(0, ('marcador-a-ciegas/index.html', 'Probar el marcador a ciegas'))
            links.insert(1, ('partidos-espejo/index.html', 'Explorar partidos espejo'))
            links.insert(2, ('balance-de-preguntas/index.html', 'Ver el balance de preguntas'))
            links.insert(3, ('preguntas-del-partido/index.html', 'Revisar las preguntas del partido'))
            links.insert(4, ('proyectos/real-zaragoza/evolucion.html' if file.name != 'evolucion.html' else 'proyectos/real-zaragoza/grupo-2.html', 'Poner el partido en contexto'))
        section = START + '<aside class="envoltorio lecturas" aria-labelledby="lecturas-relacionadas"><h2 id="lecturas-relacionadas">Sigue explorando</h2><div class="enlaces">' + ''.join('<a class="boton" href="' + relative(url, file) + '">' + label + '</a>' for url, label in links) + '</div></aside>' + END
        raw = raw.replace('</main>', section + '</main>', 1)
    return raw


def build():
    generate()
    for folder in ['proyectos', 'videos', 'sobre-mi', 'archivo', 'archivo-visual', 'conceptos', 'comparador', 'seleccion', 'novedades', 'mapa-grupo', 'herramientas', 'tras-la-jornada', 'preguntas-del-partido', 'marcador-a-ciegas', 'datos-en-revision', 'partidos-espejo', 'reloj-del-marcador', 'pizarron-de-una-jugada', 'balance-de-preguntas', 'mapa-de-lo-que-cambio', 'esquemas-del-juego', 'galeria-visual']:
        for file in (ROOT / folder).rglob('*.html'):
            raw = file.read_text(encoding='utf-8')
            if '<main' in raw:
                file.write_text(enrich(raw, file), encoding='utf-8')
    file = ROOT / 'index.html'
    file.write_text(enrich(file.read_text(encoding='utf-8'), file), encoding='utf-8')


if __name__ == '__main__':
    build()
