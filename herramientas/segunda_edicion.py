"""Portada editorial y mapa del grupo, con las fuentes del seguimiento existente."""
from pathlib import Path
from html import escape as e
import json
import re

ROOT=Path(__file__).resolve().parents[1]


def generate_map(page):
    data=json.loads((ROOT/'datos/comparador-grupo2.json').read_text(encoding='utf-8'))
    teams=sorted({r['equipo'] for r in data['partidos']})
    metrics=[('xg','xG a favor por partido'),('xgc','xG en contra por partido'),('puntos','Puntos por partido'),('gf','Goles a favor por partido'),('gc','Goles en contra por partido'),('tiros','Tiros por partido'),('claras','Ocasiones claras por partido'),('posesion','Posesión media (%)')]
    body='<p class="nota">Primera Federación · Grupo 2 · 2026/27. Cada punto representa un equipo. Las dos líneas discontinuas señalan las medias del grupo para los filtros elegidos.</p><div class="archivo-controles" id="controles-mapa" hidden>'
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
    j=latest['jornada'];rival=latest['rival'];home=latest['sede']=='Casa'
    title=('Real Zaragoza – '+rival) if home else (rival+' – Real Zaragoza')
    score=(str(latest['goles_favor'])+'–'+str(latest['goles_contra'])) if home else (str(latest['goles_contra'])+'–'+str(latest['goles_favor']))
    clues=json.loads((ROOT/'datos/claves-editoriales.json').read_text(encoding='utf-8'))
    lead=clues.get(str(j),{}).get('conclusion','La ficha reúne el resultado, las estadísticas y el contexto del último encuentro de liga.')
    html='<main><section class="apertura-editorial"><div class="envoltorio"><p class="etiqueta">Fútbol · Datos abiertos · Análisis</p><h1>El juego, más allá del marcador.</h1><p class="entradilla">Línea de pase conecta resultados, ocasiones y contexto para explicar el fútbol con datos comprobables.</p><p class="firma-editorial">Por Ángel G. Marqueta Alonso</p><div class="rutas-portada"><a class="boton lleno" href="proyectos/real-zaragoza/jornada-'+str(j)+'.html#titulo-claves">Leer el último análisis</a><a class="boton" href="comparador/index.html">Explorar los datos</a><a class="boton" href="seleccion/index.html">Conocer su trabajo</a></div></div></section>'
    html+='<div class="envoltorio"><section class="actualidad-editorial"><article class="analisis-principal"><p class="etiqueta">Último análisis · Jornada '+str(j)+'</p><h2><a href="proyectos/real-zaragoza/jornada-'+str(j)+'.html">'+e(title)+'</a></h2><p class="marcador-editorial">'+score+'</p><p class="entradilla">'+e(lead)+'</p><p class="fecha-datos">'+data['corte']+' · Temporada 2026/27</p><a class="enlace-editorial" href="proyectos/real-zaragoza/jornada-'+str(j)+'.html#titulo-claves">Las claves y el análisis completo →</a></article><aside class="mesa-de-datos"><p class="etiqueta">Mesa de datos</p><h2>Una pregunta, una herramienta</h2><a href="comparador/index.html"><strong>Dos equipos, frente a frente</strong><span>Por partido, totales y media del grupo.</span></a><a href="mapa-grupo/index.html"><strong>El grupo, en perspectiva</strong><span>Un mapa interactivo de los veinte equipos.</span></a><a href="archivo/index.html"><strong>Volver a un análisis</strong><span>Buscar por temporada, rival o tema.</span></a></aside></section>'
    delivery=latest_delivery()
    if delivery:
        html=html.replace('Último análisis · Jornada','Tras la jornada · Jornada',1)
        target='<p class="entradilla">'+e(lead)+'</p>'
        html=html.replace(target,'<h3 class="pregunta-portada">'+e(delivery[2]['pregunta'])+'</h3>'+target+'<p><a class="enlace-editorial" href="tras-la-jornada/index.html">Leer la entrega breve y ver el gráfico →</a></p>',1)
    html+='<section class="investigacion-editorial"><a class="imagen-investigacion" href="proyectos/liga-f-xt/index.html"><img src="proyectos/liga-f-xt/graficos/04_creadoras_xt_web.png" width="1600" height="900" loading="lazy" alt="Comparación de jugadoras por amenaza esperada neta por 90 minutos en la Liga F 2023/24"></a><div><p class="etiqueta">Investigación · Liga F 2023/24</p><h2><a href="proyectos/liga-f-xt/index.html">El peligro empieza antes del último pase</a></h2><p>Un modelo propio de xT estudia qué jugadoras acercan el balón a las zonas de gol y expone los límites de comparar contextos distintos.</p><a class="enlace-editorial" href="proyectos/liga-f-xt/index.html">Leer la investigación →</a></div></section>'
    html+='<section class="otras-lecturas"><article><p class="etiqueta">Fútbol femenino · Territorio</p><h2><a href="proyectos/futbol-femenino/index.html">Dónde empezar a ampliar la base</a></h2><p>Licencias del CSD y población del INE para orientar un programa piloto, con sus límites a la vista.</p></article><article><p class="etiqueta">Vídeo · Reglamento</p><h2><a href="videos/index.html#fvs">El FVS de Primera Federación</a></h2><p>Una explicación del sistema de revisión, sus solicitudes y las jugadas que pueden revisarse.</p><a href="videos/index.html">Todos los vídeos →</a></article></section>'
    html+='<section class="bloque-profesional"><div><p class="etiqueta">Para clubes, medios y proyectos deportivos</p><h2>Del dato al informe</h2><p>Una selección de tres trabajos muestra cómo Ángel Marqueta prepara datos, documenta decisiones y comunica sus conclusiones.</p></div><div class="enlaces"><a class="boton lleno" href="seleccion/index.html">Ver los casos de trabajo</a><a class="boton" href="assets/documentos/dossier-linea-de-pase.pdf">Dossier (PDF)</a><a class="boton" href="assets/documentos/cv-angel-marqueta.pdf">CV (PDF)</a></div></section>'
    news=json.loads((ROOT/'datos/novedades.json').read_text(encoding='utf-8'))
    html+='<section class="actualizaciones-breves"><h2>Últimas actualizaciones</h2><ul>'+''.join('<li><time datetime="'+n['fecha']+'">'+n['fecha'][8:10]+'/'+n['fecha'][5:7]+'</time><span>'+e(n['tipo'])+'</span><a href="'+e(n['url'],quote=True)+'">'+e(n['titulo'])+'</a></li>' for n in news[:3])+'</ul><a href="novedades/index.html">Ver el registro completo →</a></section>'
    html+='<details class="goles-portada"><summary>Los goles del Zaragoza, minuto a minuto</summary><figure class="minutos" id="minutos" aria-labelledby="t-minutos"><h2 id="t-minutos">Real Zaragoza 2026/27, minuto a minuto</h2><p id="minutos-texto">Goles de los partidos de liga del Zaragoza según el minuto en que llegaron.</p><svg id="minutos-svg" viewBox="0 0 1000 136" preserveAspectRatio="xMinYMid meet" role="img" aria-label="Goles a favor y en contra del Zaragoza por minuto"></svg><div class="leyenda-min"><span><i class="zgz-mitad"></i>A favor</span><span><i style="background:var(--senal)"></i>En contra</span></div></figure></details></div></main>'
    raw=re.sub(r'<main[\s\S]*?</main>',lambda _:html,raw,count=1)
    file.write_text(raw,encoding='utf-8')
