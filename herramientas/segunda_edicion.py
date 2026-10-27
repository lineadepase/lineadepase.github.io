"""Portada editorial y mapa del grupo, con las fuentes del seguimiento existente."""
from pathlib import Path
from html import escape as e
import json
import re

ROOT=Path(__file__).resolve().parents[1]


def generate_map(page):
    data=json.loads((ROOT/'datos/comparador-grupo2.json').read_text(encoding='utf-8'))
    from cortes import nota_corte_grupo
    seguimiento=json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    corte=nota_corte_grupo(data['jornada'],data['fecha'],seguimiento['jornada'],seguimiento['corte'])
    teams=sorted({r['equipo'] for r in data['partidos']})
    metrics=[('xg','xG a favor por partido'),('xgc','xG en contra por partido'),('puntos','Puntos por partido'),('gf','Goles a favor por partido'),('gc','Goles en contra por partido'),('tiros','Tiros por partido'),('claras','Ocasiones claras por partido'),('posesion','Posesión media (%)')]
    body='<p class="nota corte-datos">Primera Federación · Temporada 2026/27. '+e(corte)+' Cada punto representa un equipo; las líneas discontinuas señalan las medias con los filtros elegidos. <a href="../proyectos/real-zaragoza/grupo-2.html#metodo-grupo">Cobertura y método</a>.</p><div class="archivo-controles" id="controles-mapa" hidden>'
    for key,label,values,selected in [('equipo','Equipo destacado',[(x,x) for x in teams],'Real Zaragoza'),('x','Eje horizontal',metrics,'xg'),('y','Eje vertical',metrics,'xgc'),('sede','Sede',[('','Casa y fuera'),('Casa','Casa'),('Fuera','Fuera')],''),('periodo','Periodo',[('toda','Toda la temporada'),('ultimas5','Últimas cinco jornadas')],'toda'),('fuente','Fuente de xG',[('sofascore','Solo Sofascore'),('todas','Todas las fuentes documentadas')],'sofascore')]:
        body+='<label for="mapa-'+key+'">'+label+'<select id="mapa-'+key+'">'+''.join('<option value="'+e(value,quote=True)+'"'+(' selected' if value==selected else '')+'>'+e(text)+'</option>' for value,text in values)+'</select></label>'
    body+='</div><p id="mapa-detalle" role="status" aria-live="polite">Cargando los datos del grupo…</p><div class="tarjeta tarjeta-mapa"><h3>El grupo, en perspectiva</h3><p class="nota" id="mapa-nota"></p><div class="grafico" id="mapa-plot"></div></div><p class="nota">En la vista inicial, avanzar a la derecha significa generar más xG; bajar significa conceder menos. La posición describe la muestra seleccionada. La posesión y el volumen de tiros requieren contexto y no se interpretan como notas de rendimiento.</p><p><a class="boton lleno" id="mapa-comparar" href="../comparador/index.html">Comparar el equipo con el Zaragoza</a></p><details class="desplegable"><summary>Consultar todos los equipos en tabla</summary><div class="tabla-comparador"><table><thead><tr><th>Equipo</th><th id="mapa-th-x">Eje horizontal</th><th id="mapa-th-y">Eje vertical</th></tr></thead><tbody id="mapa-tabla"></tbody></table></div></details><p>n indica los partidos con dato en cada eje. <a href="../proyectos/real-zaragoza/grupo-2.html#metodo-grupo">Fuentes, cobertura y límites</a>.</p><noscript><p>La <a href="../proyectos/real-zaragoza/grupo-2.html">tabla del grupo</a> está disponible sin JavaScript.</p></noscript><script src="../assets/metricas-grupo.js?v=20261021d" defer></script><script src="../assets/mapa-grupo.js?v=20261021d" defer></script>'
    (ROOT/'mapa-grupo').mkdir(exist_ok=True)
    (ROOT/'mapa-grupo/index.html').write_text(page('El mapa del Grupo 2','Una vista conjunta para explorar cómo se relacionan los resultados, el ataque y el peligro concedido.',body),encoding='utf-8')


def generate_home():
    from entregas import latest_delivery
    file=ROOT/'index.html'
    raw=file.read_text(encoding='utf-8')
    data=json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    latest=max(data['partidos'],key=lambda r:r['jornada'])
    j=latest['jornada']; rival=latest['rival']; home=latest['sede']=='Casa'
    title=('Real Zaragoza – '+rival) if home else (rival+' – Real Zaragoza')
    score=(str(latest['goles_favor'])+'–'+str(latest['goles_contra'])) if home else (str(latest['goles_contra'])+'–'+str(latest['goles_favor']))
    clues=json.loads((ROOT/'datos/claves-editoriales.json').read_text(encoding='utf-8'))
    lead=clues.get(str(j),{}).get('conclusion','Resultado, estadísticas y contexto del último encuentro de liga.')
    photo=json.loads((ROOT/'analisis/liga-f-xt/recursos/foto.json').read_text(encoding='utf-8'))
    territory_photo=json.loads((ROOT/'analisis/futbol-femenino/recursos/foto.json').read_text(encoding='utf-8'))
    delivery=latest_delivery()
    question=('<h3 class="pregunta-portada">'+e(delivery[2]['pregunta'])+'</h3>') if delivery else ''
    brief=('<a class="boton lleno" href="tras-la-jornada/index.html">Leer las claves del partido →</a>') if delivery else ''
    date=data['corte'][8:10]+'/'+data['corte'][5:7]+'/'+data['corte'][:4]
    detail_visual=''
    if latest.get('posesion_pct') is not None:
        possession=max(0,min(100,round(float(latest['posesion_pct']))))
        moments=json.loads((ROOT/'datos/momentos-partido.json').read_text(encoding='utf-8')).get(str(j),{})
        decisive=next((item for item in moments.get('momentos',[]) if str(item.get('marcador','')).split('–')[-1] != '0'),None)
        if str(j)=='9' and decisive:
            context='El único gol llegó en el minuto '+str(decisive['minuto'])+' tras un córner. La posesión describe el reparto del balón, no el momento en que se decidió el partido.'
        else:
            context='La posesión describe el reparto del balón, no la calidad de las ocasiones. Por eso se lee junto al marcador y al resto de la ficha.'
        detail_visual=('<section class="detalle-que-cambia" aria-labelledby="titulo-detalle-visual"><div class="detalle-que-cambia-texto"><p class="etiqueta">Un dato, con contexto · Jornada '+e(str(j))+'</p><h2 id="titulo-detalle-visual">El balón no cuenta todo el partido</h2><p>'+e(context)+'</p><a class="enlace-editorial" href="proyectos/real-zaragoza/jornada-'+e(str(j))+'.html#titulo-claves">Ver el análisis completo →</a></div><figure class="detalle-visual-dato" aria-label="Dato destacado del partido"><p class="detalle-visual-cifra">'+str(possession)+'<span>%</span></p><figcaption>Posesión del Real Zaragoza</figcaption><div class="detalle-visual-barra" role="img" aria-label="El Real Zaragoza tuvo el balón el '+str(possession)+' por ciento del tiempo"><span style="width:'+str(possession)+'%"></span></div><p class="detalle-visual-pareja">'+e(title)+'</p></figure></section>')
    html=f"""<main>
<section class="apertura-editorial apertura-visual"><div class="envoltorio apertura-visual-rejilla">
  <div class="apertura-texto"><p class="etiqueta">Línea de pase · Fútbol y datos</p><h1>El juego, más allá del marcador.</h1><p class="entradilla">Partidos, protagonistas y contexto para entender el fútbol con datos.</p><p class="firma-editorial">Por Ángel G. Marqueta Alonso</p><div class="rutas-portada"><a class="boton lleno" href="proyectos/real-zaragoza/jornada-{j}.html#titulo-claves">Leer el último análisis</a><a class="boton" href="proyectos/index.html">Descubrir los proyectos</a></div></div>
  <figure class="foto foto-portada portada-ilustrada"><a class="entrada-fotografica" href="proyectos/real-zaragoza/plantilla.html"><img src="assets/ilustraciones/juego-en-perspectiva.svg" width="720" height="540" fetchpriority="high" alt="Ilustración original de un campo y una trayectoria gráfica, sin representar un partido concreto"><span>Leer los datos de la plantilla →</span></a><figcaption>Ilustración vectorial original · Sin posiciones de un partido real.</figcaption></figure>
</div></section>
<div class="envoltorio">
<section class="actualidad-editorial actualidad-compacta"><article class="analisis-principal"><p class="etiqueta">Último partido de liga · Jornada {j}</p><div class="titulo-resultado"><h2><a href="proyectos/real-zaragoza/jornada-{j}.html">{e(title)}</a></h2><p class="marcador-editorial">{score}</p></div>{question}<p class="entradilla">{e(lead)}</p><p class="fecha-datos">{date} · Temporada 2026/27</p><div class="enlaces">{brief}<a class="enlace-editorial" href="proyectos/real-zaragoza/jornada-{j}.html#titulo-claves">El análisis completo →</a></div></article><aside class="mesa-de-datos"><p class="etiqueta">Para explorar</p><h2>Haz tu propia comparación</h2><a class="imagen-menu-comparador" href="comparador/index.html" aria-label="Abrir el comparador de equipos"><img src="assets/ilustraciones/comparador-grupo2.webp" width="1672" height="941" loading="lazy" alt="Ilustración editorial de dos equipos comparados sobre un campo de fútbol"><span class="solo-lectores">Abrir el comparador de equipos</span></a><a href="comparador/index.html"><strong>Dos equipos, frente a frente →</strong><span>Resultados, ocasiones y contexto.</span></a><a href="mapa-grupo/index.html"><strong>El mapa del Grupo 2 →</strong><span>Veinte equipos en una misma vista.</span></a><a href="archivo/index.html"><strong>Buscar un análisis →</strong><span>Por rival, temporada o tema.</span></a><a href="marcador-a-ciegas/index.html"><strong>El marcador a ciegas →</strong><span>¿Qué cuentan los tiros y la posesión?</span></a><a href="preguntas-del-partido/index.html"><strong>Preguntas del partido →</strong><span>Lo que se planteó antes y se comprobó después.</span></a></aside></section>
{detail_visual}
<section class="investigacion-editorial investigacion-con-foto"><figure class="foto foto-lectura"><a href="proyectos/liga-f-xt/index.html"><img src="proyectos/liga-f-xt/graficos/foto.jpg" width="1080" height="1000" loading="lazy" alt="Caroline Graham Hansen con el FC Barcelona en 2024"></a><figcaption>Foto: {e(photo['autor'])} · <a href="{e(photo['licencia_url'],quote=True)}">{e(photo['licencia'])}</a> · <a href="{e(photo['pagina'],quote=True)}">Wikimedia Commons</a> ({e(photo['cambios'])}).</figcaption></figure><div><p class="etiqueta">Investigación · Liga F 2023/24</p><h2><a href="proyectos/liga-f-xt/index.html">¿Quién acerca el balón a las zonas de gol?</a></h2><p>Graham Hansen encabeza el estudio de amenaza esperada. El análisis explica qué mide el xT y qué queda fuera del número.</p><a class="enlace-editorial" href="proyectos/liga-f-xt/index.html">Leer «El peligro empieza antes del último pase» →</a></div></section>
<section class="otras-lecturas lecturas-visuales"><article class="lectura-territorio"><figure class="foto foto-lectura"><a href="proyectos/futbol-femenino/index.html"><img src="assets/fotos/seleccion-espanola-riazor-2024.jpg" width="1280" height="859" alt="Selección española femenina en Riazor en 2024" loading="lazy"></a><figcaption>Selección española · 2024. Foto: {e(territory_photo['autor'])} · <a href="{e(territory_photo['licencia_url'],quote=True)}">{e(territory_photo['licencia'])}</a> · <a href="{e(territory_photo['pagina'],quote=True)}">Wikimedia Commons</a> (recortada).</figcaption></figure><div><p class="etiqueta">Fútbol femenino · Territorio</p><h2><a href="proyectos/futbol-femenino/index.html">Más jugadoras, una base más amplia</a></h2><p>¿Dónde empezar un programa de iniciación? Un análisis de licencias y población, con mapa y criterios para elegir.</p><a class="enlace-editorial" href="proyectos/futbol-femenino/index.html">Ver la propuesta →</a></div></article><article class="lectura-video"><a class="miniatura-video" href="videos/index.html#fvs" aria-label="Ver la explicación del FVS de Primera Federación"><img src="assets/fvs-portada.jpg" width="1920" height="1080" loading="lazy" alt="Portada del vídeo sobre el FVS de Primera Federación"><span aria-hidden="true">▶</span></a><div><p class="etiqueta">En vídeo · Reglamento</p><h2><a href="videos/index.html#fvs">El FVS, explicado</a></h2><p>Cuándo se puede pedir una revisión y qué jugadas entran.</p></div></article></section>
<section class="bloque-profesional"><div class="firma-con-retrato"><img src="assets/angel-marqueta.webp" width="640" height="640" loading="lazy" alt="Ángel Marqueta Alonso"><div><p class="etiqueta">Quién está detrás</p><h2>Del dato al informe</h2><p>Tres proyectos de Ángel Marqueta: las preguntas, el método y lo que se puede concluir.</p></div></div><div class="enlaces"><a class="boton lleno" href="seleccion/index.html">Conocer su trabajo</a><a class="boton" href="assets/documentos/dossier-linea-de-pase.pdf">Dossier (PDF)</a></div></section>
"""
    explore_links='<a href="reloj-del-marcador/index.html"><strong>El reloj del marcador →</strong><span>Minutos de ventaja, empate o desventaja.</span></a><a href="pizarron-de-una-jugada/index.html"><strong>El pizarrón de una jugada →</strong><span>La secuencia del gol ante el Europa.</span></a><a href="balance-de-preguntas/index.html"><strong>Balance de preguntas →</strong><span>Qué se pudo comprobar después.</span></a><a href="partidos-espejo/index.html"><strong>Partidos espejo →</strong><span>Perfiles parecidos, marcadores distintos.</span></a><a href="datos-en-revision/index.html"><strong>Cuando las cifras no coinciden →</strong><span>Qué se publica y cómo se trata la diferencia.</span></a>'
    html=html.replace('<a href="preguntas-del-partido/index.html">', explore_links+'<a href="preguntas-del-partido/index.html">', 1)
    news=json.loads((ROOT/'datos/novedades.json').read_text(encoding='utf-8'))
    html+='<section class="actualizaciones-breves"><h2>Últimas actualizaciones</h2><ul>'+''.join('<li><time datetime="'+n['fecha']+'">'+n['fecha'][8:10]+'/'+n['fecha'][5:7]+'</time><span>'+e(n['tipo'])+'</span><a href="'+e(n['url'],quote=True)+'">'+e(n['titulo'])+'</a></li>' for n in news[:3])+'</ul><a href="novedades/index.html">Ver el registro completo →</a></section>'
    html+='<details class="goles-portada"><summary>Los goles del Zaragoza, minuto a minuto</summary><figure class="minutos" id="minutos" aria-labelledby="t-minutos"><h2 id="t-minutos">Real Zaragoza 2026/27, minuto a minuto</h2><p id="minutos-texto">Goles de los partidos de liga del Zaragoza según el minuto en que llegaron.</p><svg id="minutos-svg" viewBox="0 0 1000 136" preserveAspectRatio="xMinYMid meet" role="img" aria-label="Goles a favor y en contra del Zaragoza por minuto"></svg><div class="leyenda-min"><span><i class="zgz-mitad"></i>A favor</span><span><i style="background:var(--senal)"></i>En contra</span></div></figure></details></div></main>'
    raw=re.sub(r'<main[\s\S]*?</main>',lambda _:html,raw,count=1)
    if 'assets/fotografia-editorial.css' not in raw:
        raw=raw.replace('</head>', '<link rel="stylesheet" href="assets/fotografia-editorial.css?v=20261027visual02">\n</head>',1)
    else:
        raw=re.sub(r'(assets/fotografia-editorial\.css\?v=)[^"\s]+',r'\g<1>20261027visual02',raw)
    original=file.read_bytes()
    if b'\r\n' in original and b'\n' not in original.replace(b'\r\n',b''):
        raw=raw.replace('\r\n','\n').replace('\n','\r\n')
    file.write_bytes(raw.encode('utf-8'))
    from previas import portada
    portada(ROOT)
