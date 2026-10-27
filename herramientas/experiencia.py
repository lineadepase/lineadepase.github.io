"""Mejoras editoriales y herramientas de lectura; se integran al generar la web."""
from pathlib import Path
from html import escape as e
import csv
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with (ROOT / path).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def summaries():
    base = 'proyectos/real-zaragoza/'
    items = {}
    matches = read_csv('analisis/real-zaragoza/datos/salida/partidos_liga.csv')
    for row in matches:
        score = row['goles_favor'] + '–' + row['goles_contra']
        items[base + 'jornada-' + row['jornada'] + '.html'] = [
            ('Resultado', row['resultado'] + ' ante ' + row['rival'] + ': ' + score + ', con el marcador desde el punto de vista del Zaragoza.'),
            ('El dato', row['puntos_acumulados'] + ' puntos acumulados después de la jornada ' + row['jornada'] + '.'),
            ('Cómo leerlo', 'La ficha permite contrastar el marcador con los remates y la participación. El resultado por sí solo no resume el desarrollo del partido.')]
    items[base + 'jornada-8.html'] = [
        ('La conclusión', 'El Zaragoza conservó el empate en Murcia, pero le faltó continuidad para crear peligro.'),
        ('El dato', 'Nueve tiros por equipo; xG de 0,47 para el Zaragoza y 0,79 para el Murcia.'),
        ('La lectura', 'La expulsión de Ademo cambió el final: resistir permitió sumar, aunque el larguero de Moyita mostró lo ajustado del margen.')]
    latest = max(matches,key=lambda row:int(row['jornada']))
    items[base + 'ultimo-partido.html'] = items[base + 'jornada-'+latest['jornada']+'.html']
    items[base + 'grupo-2.html'] = [
        ('La conclusión', 'El Villarreal B y el Zaragoza encabezan el grupo con 17 puntos tras ocho jornadas.'),
        ('El dato', 'La diferencia de goles separa a ambos: +8 para el Villarreal B y +6 para el Zaragoza.'),
        ('La lectura', 'Para valorar el rendimiento conviene comparar también las ocasiones generadas y concedidas, atendiendo a la cobertura de xG.')]
    ranking = sorted(read_csv('analisis/real-zaragoza/datos/salida/grupo2_equipos.csv'),key=lambda row:int(row['posicion']))
    first, second = ranking[:2]
    items[base+'grupo-2.html'][:2] = [
        ('La clasificación',first['equipo']+' encabeza el grupo con '+first['puntos']+' puntos; '+second['equipo']+' es segundo con '+second['puntos']+'.'),
        ('El dato','Diferencia de goles: '+str(int(first['gf'])-int(first['gc']))+' para '+first['equipo']+' y '+str(int(second['gf'])-int(second['gc']))+' para '+second['equipo']+'.')]
    items['proyectos/futbol-femenino/index.html'] = [
        ('La propuesta', 'Andalucía y la Comunidad Valenciana son el punto de partida propuesto para un programa piloto de iniciación.'),
        ('El dato', 'Reúnen el 28,6 % de las mujeres de España y el 23,4 % de las licencias femeninas de fútbol.'),
        ('La lectura', 'Las tasas ayudan a elegir dónde estudiar un piloto; la demanda debe contrastarse con clubes, municipios y participantes.')]
    items['proyectos/liga-f-xt/index.html'] = [
        ('La conclusión', 'Graham Hansen destaca al medir el peligro que añaden los pases y las conducciones antes del tiro.'),
        ('El dato', '0,593 xT neto por 90 minutos, con un mínimo de 900 minutos; ocho de las diez primeras juegan en el Barcelona.'),
        ('La lectura', 'El contexto del equipo influye: dividir por 90 minutos no ajusta por posesión, posición, rival o marcador.')]
    items['proyectos/xg/index.html'] = [
        ('La idea', 'Los goles esperados estiman la calidad de los tiros, no deciden el resultado de un partido.'),
        ('El ejemplo', 'Un tiro de 0,20 xG tiene una probabilidad estimada del 20 % de acabar en gol.'),
        ('La lectura', 'Sumar las ocasiones ayuda a interpretar el ataque; conviene usar el mismo proveedor y modelo al comparar.')]
    data = json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    gf = sum(int(row['goles_favor']) for row in matches)
    gc = sum(int(row['goles_contra']) for row in matches)
    season = [('El balance', latest['puntos_acumulados']+' puntos después de '+latest['jornada']+' jornadas de liga.'),
              ('El dato',str(gf)+' goles a favor y '+str(gc)+' en contra en los encuentros registrados.'),
              ('La lectura','Las fichas y los gráficos permiten contrastar los resultados con las ocasiones y la participación, con sus fuentes y límites visibles.')]
    items[base+'index.html'] = season
    items[base+'informe-completo.html'] = season
    home = [row for row in matches if row['sede']=='Casa']
    away = [row for row in matches if row['sede']=='Fuera']
    items[base+'evolucion.html'] = [('La comparación','Separar casa y fuera ayuda a interpretar la evolución del equipo.'),
        ('El dato',str(sum(int(r['puntos']) for r in home))+' puntos en '+str(len(home))+' partidos en casa y '+str(sum(int(r['puntos']) for r in away))+' en '+str(len(away))+' fuera.'),
        ('La lectura','Conviene mirar puntos, goles y tiros conjuntamente; los filtros cambian la muestra y deben acompañar cualquier comparación.')]
    leader = max(data['jugadores'],key=lambda row:row['minutos'])
    items[base+'plantilla.html'] = [('La pregunta','Quién está jugando y cómo se reparte la participación en el equipo.'),
        ('El dato',leader['jugador']+' acumula '+str(int(leader['minutos']))+' minutos en los registros de liga hasta la jornada '+str(data['jornada'])+'.'),
        ('La lectura','Los minutos, las titularidades y el rol dan contexto a los goles y asistencias; las asistencias tienen cobertura incompleta.')]
    items[base+'goles-en-video.html'] = [('La pregunta','Cómo se construyen y terminan las jugadas de gol seleccionadas en los resúmenes.'),
        ('El dato',str(gf+gc)+' goles en los partidos de liga registrados: '+str(gf)+' a favor y '+str(gc)+' en contra.'),
        ('La lectura','Las anotaciones manuales permiten describir esas jugadas; no representan todas las acciones ofensivas ni defensivas del partido.')]
    items[base+'previa.html'] = [('La comparación','La previa contrasta clasificación, forma y rendimiento según la sede antes del próximo encuentro.'),
        ('El dato','El Zaragoza suma '+latest['puntos_acumulados']+' puntos hasta la jornada '+latest['jornada']+'; la tabla del rival y el corte aparecen en la comparativa.'),
        ('La lectura','La muestra describe el inicio de temporada y los rivales comunes aportan contexto, pero no permiten predecir el resultado.')]
    editorial=json.loads((ROOT/'datos/claves-editoriales.json').read_text(encoding='utf-8'))
    for jornada,entry in editorial.items():
        items[base+'jornada-'+jornada+'.html']=[('La conclusión',entry['conclusion']),('El dato',entry['dato']),('La lectura',entry['lectura'])]
    items[base+'ultimo-partido.html']=items[base+'jornada-'+latest['jornada']+'.html']
    return items


def enrich(raw, file):
    relative = file.relative_to(ROOT).as_posix()
    for asset, tag in [('assets/experiencia.css', 'css'), ('assets/experiencia.js', 'js')]:
        version = '20261021audit' if tag == 'js' else '20261021g'
        url = os.path.relpath(ROOT/asset, file.parent).replace('\\', '/') + '?v=' + version
        markup = '<link rel="stylesheet" href="'+url+'">' if tag == 'css' else '<script src="'+url+'" defer></script>'
        if asset not in raw:
            raw = raw.replace('</head>',markup+'\n</head>',1)
    for extension, version in [('css', '20261021g'), ('js', '20261021audit')]:
        raw = re.sub(r'(assets/experiencia\.' + extension + r'\?v=)[^"\s]+', lambda m: m[1] + version, raw)
    raw = re.sub(r'(assets/mejoras\.js\?v=)[^"\s]+', r'\g<1>20261021audit', raw)
    raw = re.sub(r'<meta name="grafico-contexto"[^>]*>\s*', '', raw)
    context = None
    if relative == 'index.html':
        data = json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
        context = 'Liga 2026/27 · Datos hasta '+data['corte']+' · Goles del Real Zaragoza, contrastados con las fuentes públicas del seguimiento. Elaboración propia.'
    elif relative.startswith('proyectos/real-zaragoza/'):
        data = json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
        date = data['corte']
        found = re.match(r'jornada-(\d+)\.html', file.name)
        if found:
            match = next((r for r in data['partidos'] if str(r['jornada']) == found[1]), None)
            if match:
                date = match['fecha']
        if file.name == 'grupo-2.html':
            context = 'Datos hasta '+date+' · Sofascore y fuentes complementarias de xG; cobertura y método en el análisis.'
        else:
            context = 'Datos hasta '+date+' · Estadísticas de Sofascore y fuentes del club; goles anotados a partir de resúmenes. Detalle y límites en el análisis.'
    elif relative == 'proyectos/futbol-femenino/index.html':
        context = 'Fuentes: CSD, licencias 2023 y 2025; INE, población a 1 de enero de 2025. Elaboración propia.'
    elif relative == 'proyectos/liga-f-xt/index.html':
        context = 'Fuente: StatsBomb Open Data · Liga F 2023/24 · Modelo propio de xT. Elaboración propia.'
    if context:
        raw = raw.replace('</head>','<meta name="grafico-contexto" content="'+e(context,quote=True)+'">\n</head>',1)
    raw = re.sub(r'<!-- tres-claves -->[\s\S]*?<!-- /tres-claves -->', '', raw)
    clues = summaries().get(relative)
    if clues and '<main' in raw:
        block = '<!-- tres-claves --><aside class="tres-claves" aria-labelledby="titulo-claves"><p class="etiqueta">Antes de entrar en detalle</p><h2 id="titulo-claves">Tres claves del análisis</h2><ol>' + ''.join('<li><strong>' + title + '</strong><p>' + e(value) + '</p></li>' for title, value in clues) + '</ol></aside><!-- /tres-claves -->'
        main = raw.index('<main')
        end = raw.find('</section>', main)
        if end != -1:
            raw = raw[:end+10] + block + raw[end+10:]
    raw = re.sub(r'<!-- acceso-herramienta -->[\s\S]*?<!-- /acceso-herramienta -->', '', raw)
    if relative in ['proyectos/real-zaragoza/grupo-2.html', 'proyectos/real-zaragoza/index.html']:
        href = os.path.relpath(ROOT/'comparador/index.html', file.parent).replace('\\', '/')
        block = '<!-- acceso-herramienta --><section class="seccion llamada-comparador" id="compara-equipos"><h2>Dos equipos, frente a frente</h2><p>Compara resultados, ocasiones generadas y concedidas, con filtros de casa y fuera y cobertura visible.</p><a class="boton lleno" href="'+href+'">Abrir el comparador del Grupo 2</a></section><!-- /acceso-herramienta -->'
        raw = raw.replace('<!-- /tres-claves -->', '<!-- /tres-claves -->'+block, 1) if '<!-- /tres-claves -->' in raw else raw.replace('</main>',block+'</main>',1)
    raw = re.sub(r'<!-- seleccion-profesional -->[\s\S]*?<!-- /seleccion-profesional -->', '', raw)
    if relative in ['proyectos/index.html', 'sobre-mi/index.html']:
        href = os.path.relpath(ROOT/'seleccion/index.html', file.parent).replace('\\', '/')
        block = '<!-- seleccion-profesional --><section class="seccion envoltorio llamada-seleccion"><p class="etiqueta">Para clubes, medios y proyectos deportivos</p><h2>Tres trabajos para conocer su enfoque</h2><p>Del seguimiento de un equipo a un modelo propio: las preguntas, las decisiones y los resultados de una selección de proyectos.</p><a class="boton lleno" href="'+href+'">Ver la selección de trabajos</a></section><!-- /seleccion-profesional -->'
        if relative == 'index.html':
            marker = re.search(r'<section class="seccion" aria-labelledby="t-videos">', raw)
            raw = raw[:marker.start()] + block + raw[marker.start():] if marker else raw.replace('</main>',block+'</main>',1)
        else:
            raw = raw.replace('</main>',block+'</main>',1)
    raw = re.sub(r'<!-- novedades-portada -->[\s\S]*?<!-- /novedades-portada -->', '', raw)
    if relative == 'index.html' and 'apertura-editorial' not in raw:
        news = json.loads((ROOT/'datos/novedades.json').read_text(encoding='utf-8'))
        block = '<!-- novedades-portada --><section class="seccion novedades-portada" aria-labelledby="titulo-novedades"><div class="envoltorio"><p class="etiqueta">Qué ha cambiado</p><h2 id="titulo-novedades">Novedades de Línea de pase</h2>'+news_list(news[:3], '')+'<a class="boton" href="novedades/index.html">Ver todas las novedades</a></div></section><!-- /novedades-portada -->'
        raw = raw.replace('<section class="seccion" aria-labelledby="t-metodo">',block+'<section class="seccion" aria-labelledby="t-metodo">',1)
    return raw


def generate_comparator(page):
    rows = read_csv('analisis/real-zaragoza/datos/entrada/grupo2_partidos.csv')
    fields = ['jornada', 'fecha', 'equipo', 'rival', 'sede', 'goles_favor', 'goles_contra', 'xg', 'xg_rival', 'ocasiones_claras', 'ocasiones_claras_rival', 'tiros', 'posesion_pct', 'fuente_url', 'fuente_xg']
    numeric = set(fields) - {'fecha', 'equipo', 'rival', 'sede', 'fuente_url', 'fuente_xg'}
    records = [{key: (float(row[key]) if row[key] else None) if key in numeric else row[key] for key in fields} for row in rows]
    assert len({(r['equipo'], r['jornada']) for r in records}) == len(records)
    data = {'jornada': int(max(r['jornada'] for r in records)), 'fecha': max(r['fecha'] for r in records), 'partidos': records}
    (ROOT/'datos/comparador-grupo2.json').write_text(json.dumps(data, ensure_ascii=False, allow_nan=False, indent=1), encoding='utf-8')
    teams = sorted({r['equipo'] for r in records})
    controls = '<div class="archivo-controles" id="controles-comparador" hidden>'
    for key, label, selected in [('a', 'Primer equipo', 'Real Zaragoza'), ('b', 'Segundo equipo', 'Villarreal B')]:
        controls += '<label for="equipo-' + key + '">' + label + '<select id="equipo-' + key + '">' + ''.join('<option' + (' selected' if team == selected else '') + '>' + e(team) + '</option>' for team in teams) + '</select></label>'
    controls += '<label for="sede-comparador">Dónde juega<select id="sede-comparador"><option value="">Casa y fuera</option><option>Casa</option><option>Fuera</option></select></label><label for="fuentes-comparador">Fuente de xG<select id="fuentes-comparador"><option value="sofascore">Solo Sofascore</option><option value="todas">Todas las fuentes documentadas</option></select></label><label for="modo-comparador">Mostrar<select id="modo-comparador"><option value="promedio">Por partido</option><option value="totales">Totales</option></select></label><label for="periodo-comparador">Periodo<select id="periodo-comparador"><option value="toda">Toda la temporada</option><option value="ultimas5">Últimas cinco jornadas</option></select></label></div>'
    art = '<figure class="comparador-hero"><img src="../assets/ilustraciones/comparador-grupo2.webp" width="1672" height="941" fetchpriority="high" alt="Dos equipos enfrentados en un campo, con trayectorias y datos representados como líneas de juego"><figcaption>La vista reúne resultados, ocasiones y contexto para los dos equipos.</figcaption></figure>'
    body = art + '<p class="nota">Primera Federación · Grupo 2 · Temporada 2026/27. Datos hasta la jornada ' + str(data['jornada']) + '. Los indicadores por partido se calculan solo con los encuentros que tienen ese dato.</p>' + controls
    body += '<div class="acciones-comparador"><button class="boton" id="intercambiar-equipos" type="button">Intercambiar equipos</button><button class="boton" id="copiar-comparacion" type="button">Copiar comparación</button><button class="boton" id="descargar-comparacion" type="button">Descargar comparativa (PNG)</button><a class="boton" id="ir-mapa" href="../mapa-grupo/index.html">Ver el mapa del grupo</a></div><p id="estado-compartir" role="status"></p><input id="enlace-comparacion" aria-label="Enlace de la comparación" readonly hidden>'
    body += '<p id="estado-comparador" role="status" aria-live="polite">Cargando comparación…</p><p class="nota">Las barras utilizan una escala común para los veinte equipos del filtro. La marca vertical señala la media del grupo. En móvil, la tabla se puede desplazar horizontalmente.</p><div id="resultado-comparador"></div><p class="nota">Por partido, la referencia se calcula con todos los registros disponibles del grupo tras aplicar los filtros; en totales, se muestra la media de los equipos. La posesión siempre conserva su media porcentual. El selector de fuente afecta únicamente a xG. Las fuentes complementarias pueden utilizar modelos diferentes.</p><details class="desplegable"><summary>Consultar cobertura y procedencia de los xG</summary><div id="fuentes-comparadas"></div></details><noscript><p>La tabla del <a href="../proyectos/real-zaragoza/grupo-2.html">análisis del grupo</a> está disponible sin JavaScript.</p></noscript><p><a href="../datos/comparador-grupo2.json" download>Descargar los datos del comparador (JSON)</a> · <a href="../proyectos/real-zaragoza/grupo-2.html#metodo-grupo">Método y límites del análisis</a></p><script src="../assets/metricas-grupo.js?v=20261021g" defer></script><script src="../assets/comparador.js?v=20261021g" defer></script>'
    (ROOT/'comparador').mkdir(exist_ok=True)
    (ROOT/'comparador/index.html').write_text(page('Compara dos equipos del Grupo 2', 'Elige dos equipos y explora sus resultados, la producción ofensiva y las ocasiones que conceden.', body), encoding='utf-8')


def generate_selection(page):
    cases = [
        ('seguimiento', 'Seguimiento del Real Zaragoza', 'Resultados, evolución y contexto de los rivales en Primera Federación.',
         'Entender cómo evoluciona el equipo y qué diferencias hay entre los resultados y las ocasiones que genera.',
         'Reunir fuentes con coberturas distintas, contrastar discrepancias y mantener las jornadas actualizadas sin tratar los datos ausentes como ceros.',
         'Preparación de tablas, comprobaciones con Python y R, visualización en la web y libro de Tableau con extracciones.',
         'Panel de temporada, fichas de partido, comparación del grupo y materiales descargables.',
         'El registro de incidencias documenta decisiones; el método identifica las fuentes de xG y los límites de la muestra.',
         '../proyectos/real-zaragoza/index.html', '../analisis/real-zaragoza/datos/entrada/incidencias.csv', 'Registro de decisiones (CSV)'),
        ('modelo', 'Amenaza esperada en la Liga F', 'Un modelo propio para estudiar lo que ocurre antes del último pase.',
         'Medir qué jugadoras acercan el balón a las zonas desde las que se marca mediante pases y conducciones.',
         'Separar los partidos de entrenamiento y valoración para no evaluar una jugadora con un modelo que ya ha visto ese encuentro.',
         'Modelo de xT con Python, pandas y NumPy; visualizaciones con Matplotlib y documentación del procedimiento.',
         'Investigación de la Liga F 2023/24, clasificación de jugadoras con mínimo de minutos y resultados descargables.',
         'Validación fuera de muestra y límites explícitos: el valor por 90 minutos no ajusta el contexto del equipo.',
         '../proyectos/liga-f-xt/index.html', '../proyectos/liga-f-xt/jugadoras_xt.csv', 'Resultados por jugadora (CSV)'),
        ('territorio', 'Dónde ampliar la base del fútbol femenino', 'Datos públicos para orientar una decisión territorial.',
         'Elegir dónde estudiar un programa piloto de iniciación con criterios comparables y explícitos.',
         'Relacionar licencias del CSD y población del INE, evitando confundir el tamaño de una comunidad con su tasa de participación.',
         'Cálculo de tasas, evolución y criterios de selección con Python; mapa y documentos explicativos. Trabajo en el marco de una actividad colaborativa del máster.',
         'Propuesta inicial para Andalucía y la Comunidad Valenciana, acompañada de indicadores y materiales de consulta.',
         'Comprobación de totales nacionales y distinción entre una propuesta basada en tasas y la demanda real por contrastar.',
         '../proyectos/futbol-femenino/index.html', '../analisis/futbol-femenino/datos/salida/indicadores.csv', 'Indicadores territoriales (CSV)')]
    body = '<div class="enlaces descargas-profesionales"><a class="boton lleno" href="../assets/documentos/dossier-linea-de-pase.pdf">Dossier de proyectos (PDF)</a><a class="boton" href="../assets/documentos/cv-angel-marqueta.pdf">CV (PDF)</a><a class="boton" href="#english-profile">English profile</a></div><nav class="enlaces" aria-label="Selección de casos">'+''.join('<a class="boton" href="#'+c[0]+'">'+e(c[1])+'</a>' for c in cases)+'</nav>'
    for anchor, title, subtitle, question, challenge, method, output, proof, href, data, label in cases:
        body += '<article class="caso-seleccion" id="'+anchor+'"><p class="etiqueta">Caso de trabajo</p><h2>'+e(title)+'</h2><p class="entradilla">'+e(subtitle)+'</p><dl>'
        for key,value in [('Pregunta',question),('Problema resuelto',challenge),('Trabajo desarrollado',method),('Resultado',output),('Cómo se comprueba',proof)]:
            body += '<dt>'+key+'</dt><dd>'+e(value)+'</dd>'
        application={'seguimiento':'Un cuerpo técnico o un medio puede contrastar la evolución del equipo, preparar preguntas sobre el próximo rival y consultar el origen de cada cifra.','modelo':'Un área de análisis puede explorar la progresión del balón antes del tiro y detectar perfiles para revisar en vídeo; el modelo no constituye por sí solo una recomendación de fichaje.','territorio':'Una entidad deportiva puede justificar dónde estudiar un piloto y definir qué debe comprobarse sobre el terreno antes de ampliar el programa.'}[anchor]
        body += '<dt>Aplicación práctica</dt><dd>'+application+'</dd>'
        body += '</dl><div class="enlaces"><a class="boton lleno" href="'+href+'">Explorar el proyecto</a><a class="boton" href="'+data+'">'+label+'</a></div></article>'
    body += '<section class="seccion" id="english-profile" lang="en"><p class="etiqueta">English profile</p><h2>Football analysis, with the evidence in view</h2><p>Ángel G. Marqueta Alonso is studying for a Master’s in Sports Big Data at Sports Data Campus. His work combines public football data, documented checks and visual explanations.</p><p>His portfolio covers season monitoring for Real Zaragoza, an expected-threat model for the 2023/24 Liga F season, and a regional participation study using Spanish public statistics. Each project distinguishes the findings from the limits of the available data.</p><p>His earlier technical and administrative roles involved incident management, data entry and regular reporting. The portfolio shows how that background is being developed towards sports analytics.</p></section><section class="seccion"><h2>Contacto profesional</h2><p>Ángel Marqueta cursa el Máster en Big Data Deportivo de Sports Data Campus. La selección reúne trabajos de preparación de datos, documentación de decisiones y comunicación de resultados.</p><a class="boton lleno" href="https://www.linkedin.com/in/angel-marqueta-alonso-a8831164" target="_blank" rel="noopener">Contactar por LinkedIn</a> <a class="boton" href="../sobre-mi/index.html">Formación y trayectoria</a></section>'
    (ROOT/'seleccion').mkdir(exist_ok=True)
    (ROOT/'seleccion/index.html').write_text(page('Una selección de trabajos', 'Tres proyectos de Ángel Marqueta: de la pregunta deportiva a los datos comprobables, el informe y su aplicación.',body), encoding='utf-8')


def news_list(entries, prefix):
    out = '<ol class="novedades-lista">'
    for item in entries:
        year, month, day = item['fecha'].split('-')
        out += '<li><span class="tipo-novedad">'+e(item['tipo'])+'</span> <time datetime="'+item['fecha']+'">'+day+'/'+month+'/'+year+'</time><h2><a href="'+prefix+e(item['url'],quote=True)+'">'+e(item['titulo'])+'</a></h2><p>'+e(item['texto'])+'</p></li>'
    return out+'</ol>'


def generate_news(page):
    news = json.loads((ROOT/'datos/novedades.json').read_text(encoding='utf-8'))
    assert all(x['tipo'] in ('Publicación', 'Actualización', 'Corrección') for x in news)
    news.sort(key=lambda x:x['fecha'], reverse=True)
    (ROOT/'novedades').mkdir(exist_ok=True)
    (ROOT/'novedades/index.html').write_text(page('Qué hay de nuevo', 'Publicaciones, actualizaciones de datos y correcciones, con su fecha y el enlace al contenido afectado.',news_list(news,'../')),encoding='utf-8')
