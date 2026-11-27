from pathlib import Path
from html import escape
import json
import re
from datetime import date
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1]
D=R/'datalab-prototipo'
sections={
'datalab':('DataLab','La curiosidad también se entrena.','Experimenta, comprende e investiga. Cambia una variable antes de sacar conclusiones.', [('xG, sin líos','Qué significa una probabilidad de gol y qué no puede decirnos.','proyectos/xg/'),('El peligro empieza antes del último pase','Modelo xT de Liga F, metodología y validación.','proyectos/liga-f-xt/'),('Los puntos engañan','Explora el seguimiento disponible. La investigación de fortaleza todavía requiere validación.','proyectos/real-zaragoza/')]),
'museo':('Museo','Cada gráfico guarda una historia.','Un recorrido por redes de pases, territorio y memoria de una temporada.', [('La selección conectada','Redes de pases y estructura de la selección española.','proyectos/espana-eurocopa-redes/'),('Una temporada en imágenes','Explora jornadas, compara marcadores y descarga sus láminas.','archivo-visual/'),('El fútbol femenino en el mapa','Datos, población y oportunidades para ampliar la base.','proyectos/futbol-femenino/')]),
'play':('Play','Primero intuye. Después comprueba.','Retos breves para mirar el partido con otras preguntas.', [('Marcador a ciegas','¿Qué te cuentan los datos antes de conocer el resultado?','marcador-a-ciegas/'),('Partidos espejo','Compara partidos que parecen iguales.','partidos-espejo/'),('El reloj del marcador','Descubre cómo cambia la lectura con el paso del tiempo.','reloj-del-marcador/'),('Balance de preguntas','Pon a prueba tu interpretación del encuentro.','balance-de-preguntas/')]),
'zaragoza':('Zaragoza','Un equipo. Muchas preguntas.','Seguimiento de temporada con fecha de corte, fuentes y cobertura explícitas.', [('El panel de temporada','Resultados, evolución y participación.','proyectos/real-zaragoza/'),('El contexto del grupo','Compara equipos con los filtros existentes.','comparador/'),('Los futuros posibles','Consulta el modelo de simulación y sus límites.','proyectos/real-zaragoza/simulacion.html'),('Tras la jornada','La última entrega editorial disponible.','tras-la-jornada/')]),
'pro':('Pro','Del gráfico a la decisión.','Métodos reproducibles, fuentes y herramientas para trabajar con criterio.', [('Selección profesional','Proyectos, perfil y dossier del autor.','seleccion/'),('Caja de herramientas','Comparador y mapa del grupo.','herramientas/'),('Conceptos para interpretar','Una guía para leer las métricas.','conceptos/'),('Código y metodología','Reproduce los análisis y consulta las pruebas.','https://github.com/lineadepase/lineadepase.github.io')]),
'studio':('Studio','Dale forma a lo que has descubierto.','Crea piezas con los generadores existentes. Revisa el corte y las fuentes antes de compartir.', [('Taller de láminas','SVG, PNG, WebP, carruseles y formatos sociales con datos de jornada.','archivo-visual/'),('La entrega de jornada','Prepara imagen y texto por canal.','tras-la-jornada/'),('Pizarrón de una jugada','Descompón y explica una secuencia.','pizarron-de-una-jugada/'),('Galería visual','Encuentra una pieza y consulta su contexto.','galeria-visual/')]),
'media':('Media','El fútbol también se explica mirando.','Vídeos y lecturas para seguir una pregunta más allá del laboratorio.', [('Vídeos','Explicaciones audiovisuales de Línea de Pase.','videos/'),('Archivo de análisis','Busca por tema, proyecto o jornada.','archivo/'),('Novedades','Consulta las incorporaciones a la web.','novedades/')]),
'pasaporte':('Pasaporte','Tu recorrido, a tu ritmo.','Guarda las áreas que has explorado y una nota de aprendizaje. Solo en este navegador.', [])}
def cards(items):
 return ''.join(f'<article class="card"><span class="number">{i:02}</span><h3>{escape(t)}</h3><p>{escape(d)}</p><a href="{u if u.startswith("https:") else "../"+u}">Abrir experiencia <span aria-hidden="true">↗</span></a></article>' for i,(t,d,u) in enumerate(items,1))
def snapshot(data):
 """Resumen de liga: solo marcadores completos y anteriores al corte."""
 cutoff = date.fromisoformat(data['corte'])
 played = []
 for match in data.get('partidos', []):
  if type(match.get('jornada')) is not int or match['jornada']<1:
   raise ValueError('Jornada inválida en los datos del Zaragoza')
  if any(match.get(key) is None for key in ('goles_favor', 'goles_contra')):
   continue
  if any(type(match[key]) is not int or match[key] < 0 for key in ('goles_favor', 'goles_contra')):
   raise ValueError('Marcador inválido en los datos del Zaragoza')
  match_date = date.fromisoformat(match['fecha'])
  if match_date <= cutoff:
   played.append(match)
 if not played:
  return '<div class="snapshot"><p>No hay resultados de liga disponibles para este corte.</p></div>'
 p = max(played, key=lambda match: (match['fecha'], match['jornada']))
 return f'<div class="snapshot"><p class="eyebrow">DATOS EXISTENTES · CORTE {escape(data["corte"])}</p><h3>Jornada {p["jornada"]} · {escape(p["rival"])}</h3><p class="result">{p["goles_favor"]} – {p["goles_contra"]}</p><p>Marcador de liga en orden Zaragoza–rival · {escape(p["sede"])} · {escape(p["fecha"])}.</p><p>La cobertura estadística varía entre partidos. Consulta las fuentes y las fichas completas en el panel.</p><a href="../proyectos/real-zaragoza/">Consultar el panel y sus fuentes</a></div>'

def museum():
 return '''<div class="gallery"><article class="exhibit"><p class="eyebrow">SALA 01 · CONEXIONES</p><h3>¿Quién conecta al equipo?</h3><figure><a href="../analisis/espana-eurocopa-redes/graficos/01_red_final_instagram.svg"><img src="../analisis/espana-eurocopa-redes/graficos/01_red_final_instagram.png" alt="Red de pases de España en la final de la Eurocopa femenina 2025. Laia Aleixandri está destacada por su intermediación." width="1080" height="1350" loading="lazy"></a><figcaption>Eurocopa femenina 2025 · StatsBomb Open Data · Elaboración de Línea de Pase. Abre la imagen para ampliarla.</figcaption></figure><p>Antes de leer: ¿la futbolista que más conecta tiene que ser quien más pases da?</p><details><summary>Descubre cómo leer la red</summary><p>Los círculos representan posición media y volumen de pases; las líneas unen parejas con al menos cuatro pases. El naranja identifica la mayor intermediación: por esa jugadora pasan más caminos cortos entre compañeras. En esta muestra es Laia Aleixandri.</p><p>La red incluye pases completados en juego hasta el primer cambio de España, en el minuto 70. No representa todas las acciones ni demuestra por sí sola la calidad de una jugadora.</p><a href="../proyectos/espana-eurocopa-redes/">Investiga la metodología y el contexto</a></details></article><article class="exhibit"><p class="eyebrow">SALA 02 · TERRITORIO</p><h3>¿Vale lo mismo un pase en cualquier zona?</h3><figure><a href="../proyectos/liga-f-xt/graficos/02_superficie_xt_instagram.png"><img src="../proyectos/liga-f-xt/graficos/02_superficie_xt_instagram.png" alt="Superficie de amenaza esperada de Liga F 2023/24: el valor de zona aumenta cerca de la portería hacia la derecha." width="1080" height="1350" loading="lazy"></a><figcaption>Liga F 2023/24 · StatsBomb Open Data · Modelo propio de Línea de Pase.</figcaption></figure><p>Observa el destino del balón. ¿Qué cambia si el pase acaba más cerca de la portería?</p><details><summary>Descubre el valor del territorio</summary><p>El modelo asigna un valor a cada zona. El xT de una acción completada es el valor del destino menos el del origen. En este mapa la dirección de ataque va hacia la derecha.</p><p>La superficie está ajustada con toda la temporada para explicar el método. No mide los movimientos sin balón ni demuestra que una decisión haya sido la mejor posible.</p><a href="../proyectos/liga-f-xt/">Investiga la validación del modelo</a></details></article></div>'''

class ArchiveOptions(HTMLParser):
 def __init__(self,select_id='comparar-jornada-a'):
  super().__init__()
  self.target=select_id
  self.active=False
  self.current=None
  self.options=[]
 def handle_starttag(self, tag, attrs):
  attrs=dict(attrs)
  if tag=='select': self.active=attrs.get('id')==self.target
  if tag=='option' and self.active: self.current=[attrs['value'], '']
 def handle_data(self, text):
  if self.current is not None: self.current[1]+=text
 def handle_endtag(self, tag):
  if tag=='option' and self.current is not None:
   self.options.append(tuple(self.current))
   self.current=None
  if tag=='select': self.active=False

def studio(archive):
 parser=ArchiveOptions()
 parser.feed(archive)
 options=parser.options
 if len(options)<2:
  return '<p>La comparación necesita dos jornadas disponibles. <a href="../archivo-visual/">Consulta el archivo visual</a>.</p>'
 def select(name, label, selected):
  choices=''.join(f'<option value="{escape(value, quote=True)}"'+(' selected' if i==selected else '')+f'>{escape(text)}</option>' for i,(value,text) in enumerate(options))
  return f'<label for="studio-{name}">{label}</label><select id="studio-{name}" name="{name}">{choices}</select>'
 poster_parser=ArchiveOptions('temporada-mapa')
 poster_parser.feed(archive)
 poster=''
 poster_options=poster_parser.options
 if not poster_options:
  seasons=sorted({value.split('|',1)[0] for value,_ in options if re.fullmatch(r'\d{4}/\d{2}\|[1-9]\d*',value)},reverse=True)
  poster_options=[(season,season) for season in seasons]
 if poster_options:
  choices=''.join(f'<option value="{escape(value,quote=True)}">{escape(text)}</option>' for value,text in poster_options)
  poster='<form class="studio-map" action="../archivo-visual/#titulo-mapa-temporada" method="get"><h3>Un mapa de la temporada</h3><p>Abre el generador con la temporada y el formato que necesitas.</p><label for="studio-mapa-temporada">Temporada</label><select id="studio-mapa-temporada" name="mapa-temporada">'+choices+'</select><label for="studio-mapa-formato">Formato del mapa</label><select id="studio-mapa-formato" name="mapa-formato"><option value="cuadrado">Cuadrado</option><option value="vertical">Vertical</option><option value="historias">Historias</option></select><input type="hidden" name="mapa-archivo" value="webp"><button type="submit">Preparar mapa en el taller →</button></form>'
 return '<div class="experiment"><form id="studio-form" action="../archivo-visual/#titulo-comparar" method="get"><h3>De dos jornadas a una lámina</h3><p>Elige dos jornadas distintas y abre el taller con esa pareja preparada.</p>'+select('jornada_a','Primera jornada',0)+select('jornada_b','Segunda jornada',1)+'<p id="studio-estado" role="status"></p><button type="submit">Abrir la comparación en Studio ↗</button></form><div><h3>Tu proceso de creación</h3><ol><li>Compara los marcadores y revisa la cobertura.</li><li>En el taller, elige formato: cuadrado, vertical, historias o carrusel.</li><li>Revisa la fuente y el texto alternativo antes de descargar.</li></ol><p>Las métricas se muestran solo cuando ambas fichas están completas. El taller permite exportar SVG, PNG o WebP.</p><a href="../archivo-visual/#titulo-mapa-temporada">Crear un mapa de temporada</a></div></div>'+poster

def media():
 return '''<article class="media-feature"><div><p class="eyebrow">MIRA · EXPERIMENTA · COMPRENDE</p><h3>xG, sin líos</h3><p>¿Puedes crear más peligro y aun así perder? Una explicación de 1 minuto y 14 segundos, con subtítulos integrados.</p><video controls playsinline preload="none" poster="../assets/xg-portada.jpg" width="1920" height="1080" aria-label="xG, sin líos: explicación de los goles esperados"><source src="../assets/xg-sin-lios.mp4?v=20261014b" type="video/mp4">Tu navegador no puede reproducir el vídeo. <a href="../assets/xg-sin-lios.mp4?v=20261014b">Descargar el vídeo</a>.</video><p>Fuentes indicadas en el vídeo: Opta / FotMob y Hudl StatsBomb. Incluye ejemplos didácticos e imágenes recreadas con IA.</p></div><div><h3>Del vídeo al laboratorio</h3><p>Antes de verlo, piensa: si sumas 1 xG, ¿has garantizado un gol?</p><details><summary>Leer la idea principal</summary><p>El xG estima la probabilidad de gol de cada remate y suma esas probabilidades. Un tiro de 0,20 xG representa una probabilidad estimada del 20 %. Acumular 1 xG no garantiza un gol.</p><p>La estimación depende del modelo y de la información disponible. Describe la calidad de los tiros, pero no decide el marcador.</p></details><a class="cta" href="#datalab">Compruébalo con el simulador</a><p><a href="../videos/#t-xg">Ver explicación completa y fuentes</a></p></div></article><details class="brand-intro"><summary>La firma de Línea de Pase · Del campo al dato</summary><p>Un recorrido de pases se convierte en el logotipo de la marca. Intro original facilitada por el autor.</p><video controls playsinline preload="none" poster="../assets/marca/intro-poster.webp" width="1280" height="720" aria-label="Intro de Línea de Pase: del campo al dato"><source src="../assets/marca/intro-corta-horizontal.mp4" type="video/mp4">Tu navegador no puede reproducir la intro. <a href="../assets/marca/intro-corta-horizontal.mp4">Abrir vídeo horizontal</a>.</video><p><a href="../assets/marca/intro-corta-vertical.mp4" download>Descargar versión vertical</a> · <a href="../assets/marca/intro-corta-horizontal.mp4" download>Descargar versión horizontal</a></p></details>'''

def build():
 nav=''.join(f'<a href="#{k}">{v[0]}</a>' for k,v in sections.items())
 body=''
 for section_number,(k,(name,title,desc,items)) in enumerate(sections.items(),1):
  extra=''
  acciones=''
  if k=='datalab':
   extra='''<div class="experiment"><div><p class="eyebrow">EXPERIMENTO 01 · PROBABILIDAD</p><h3>¿Cuántas ocasiones necesitas?</h3><p>Predice el resultado y mueve los controles.</p><label for="tiros">Disparos: <output id="n">5</output></label><input id="tiros" type="range" min="1" max="30" value="5"><label for="prob">Probabilidad por disparo: <output id="p">15 %</output></label><input id="prob" type="range" min="0" max="100" value="15"></div><div><p>Probabilidad de al menos un gol</p><p id="resultado" class="result" aria-live="polite">55,6 %</p><div class="bar"><span id="barra"></span></div><p id="esperados">Goles esperados: 0,8</p><details><summary>Comprende el experimento</summary><p>1 − (1 − p)ⁿ. Disparos independientes con idéntica probabilidad. Es un modelo didáctico, no un xG entrenado ni una predicción real.</p><p><a href="../proyectos/xg/">Profundiza en xG, sin líos</a></p></details><button id="simular" type="button">Simular una serie</button><p id="simulacion" aria-live="polite"></p></div></div>'''
   from linea2_experiencias import laboratories
   extra+=laboratories()
   from linea2_cuaderno import scenario_lab, varied_lab
   extra+=scenario_lab()+varied_lab()
  if k=='museo':
   extra=museum()
   from linea2_cuaderno import museum_notebook
   extra+=museum_notebook()
  if k=='studio':
   extra=studio((R/'archivo-visual/index.html').read_text(encoding='utf-8'))
   from linea2_cuaderno import editorial_form
   extra+=editorial_form()
  if k=='media':
   extra=media()
  if k=='pro':
   extra='''<div class="method"><h3>De una pregunta a una conclusión verificable</h3><ol><li><strong>Formula:</strong> define qué quieres saber y qué evidencia cambiaría tu opinión.</li><li><strong>Audita:</strong> comprueba origen, licencia, fecha y cobertura de los datos.</li><li><strong>Contrasta:</strong> compara con una referencia y valida fuera de la muestra usada para ajustar.</li><li><strong>Comunica:</strong> muestra la incertidumbre, las limitaciones y el código reproducible.</li></ol><p><a href="../seleccion/">Explora los proyectos y sus métodos</a></p></div>'''
   from linea2_cuaderno import research_form
   extra+=research_form()
  if k=='play':
   extra='''<div class="experiment"><div><h3>El trivial del dato</h3><p>Tres rondas temáticas de tres preguntas. Cada respuesta incluye una explicación. Cambiar de tema inicia una partida nueva; no se guarda la puntuación.</p><label for="reto-tema">Elige tu ronda</label><select id="reto-tema"><option value="intuicion">Intuición y goles esperados</option><option value="lectura">Leer el partido</option><option value="metodo">Investigar con criterio</option></select><p id="reto-progreso" role="status" tabindex="-1"></p><p id="reto-pregunta" tabindex="-1">Con dos disparos independientes al 50 %, ¿cuál es la probabilidad de marcar al menos una vez?</p><div class="answers"><button data-answer="50">50 %</button><button data-answer="75">75 %</button><button data-answer="100">100 %</button></div><p id="respuesta" aria-live="polite"></p><ol id="reto-historial" aria-label="Resultados de tus respuestas"></ol><div id="reto-resumen" hidden></div><button id="reto-siguiente" type="button" disabled>Siguiente pregunta</button><button id="reto-reiniciar" type="button">Volver a empezar</button><noscript><p>Activa JavaScript para responder. Solución del primer reto: 75 %. La probabilidad de fallar ambos es 25 %.</p></noscript></div></div>'''
  if k=='zaragoza':
   data=json.loads((R/'datos/zaragoza.json').read_text(encoding='utf-8'))
   from linea2_experiencias import season
   extra=snapshot(data)+season(data,(R/'archivo-visual/index.html').read_text(encoding='utf-8'))
  if k=='pasaporte':
   extra='''<div class="experiment"><div><noscript><p>El pasaporte necesita JavaScript para guardar tu recorrido. Puedes seguir explorando todas las áreas y sus enlaces.</p></noscript><p id="progreso" aria-live="polite"></p><progress id="pasaporte-barra" max="7" value="0" aria-label="Áreas exploradas"></progress><p><a id="pasaporte-retomar" href="#datalab">Continuar por DataLab →</a></p><div id="sellos"></div><label for="nota">¿Qué has aprendido?</label><textarea id="nota" maxlength="2000" rows="4"></textarea><p id="guardado" role="status"></p><button id="exportar">Descargar pasaporte</button><button id="borrar">Borrar mi recorrido</button><details class="passport-transfer"><summary>Llevar mi pasaporte a otro navegador</summary><p>Descarga una copia JSON y elígela en el otro dispositivo. La importación sustituye el recorrido solo cuando lo confirmas. El archivo puede contener tu nota personal; se lee en este navegador.</p><button id="pasaporte-json" type="button">Descargar copia JSON</button><label for="pasaporte-archivo">Elegir una copia de pasaporte</label><input id="pasaporte-archivo" type="file" accept=".json,application/json"><p id="pasaporte-importacion" role="status"></p><button id="pasaporte-aplicar" type="button" disabled>Sustituir mi recorrido por esta copia</button></details></div><div><h3>Un recuerdo de tu visita</h3><p>Marca cada área después de explorarla. Puedes descargar una copia y borrar tus datos cuando quieras. No se crea una cuenta ni se envían tus notas.</p></div></div>'''
  if k!='pasaporte':
   siguiente=list(sections)[list(sections).index(k)+1]
   acciones=f'<div class="visit-actions"><button id="sello-{k}" type="button" aria-pressed="false" hidden>Guardar {name} en mi pasaporte</button><a href="#pasaporte">Anotar un descubrimiento</a><a href="#indice-experiencias">Ver todas las herramientas ↑</a><a href="#{siguiente}">Seguir hacia {sections[siguiente][0]} →</a></div>'
  bands={
   'datalab':'<strong>DataLab / Ciencia del fútbol</strong><span>Experimenta · Comprende · Investiga</span>',
   'zaragoza':'<strong class="club"><img src="../assets/real-zaragoza-escudo-96.png" width="34" height="40" alt="" role="presentation">Real Zaragoza</strong><span>La temporada, en datos</span>',
   'play':'<strong>LDP / PLAY</strong><span>Lee el juego. Toma una decisión.</span>',
   'studio':'<strong>Studio / Mesa de edición</strong><span>Selecciona · Compón · Exporta</span>',
   'pro':'<strong>Línea de Pase / Pro</strong><span>Fuentes · Método · Validación</span>'
  }
  band=f'<div class="area-band">{bands[k]}</div>' if k in bands else ''
  body+=f'<section id="{k}" aria-labelledby="titulo-{k}">{band}<div class="section-head"><p class="eyebrow">{section_number:02} / {name.upper()}</p><h2 id="titulo-{k}">{title}</h2><p>{desc}</p></div>{extra}<div class="grid">{cards(items)}</div>{acciones}</section>'
 from linea2_experiencias import routes, experience_index
 recorridos=routes()+experience_index()
 html=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><link rel="canonical" href="https://lineadepase.com/datalab-prototipo/"><meta name="description" content="Línea de Pase 2.0: experimenta con la ciencia del fútbol, explora su historia y crea con datos."><title>Línea de Pase 2.0 · Prototipo</title><link rel="icon" href="../assets/icono.svg"><link rel="stylesheet" href="../assets/linea2.css"><link rel="stylesheet" href="../assets/linea2-areas.css"></head><body><a class="skip" href="#contenido">Saltar al contenido</a><header><a class="brand" href="../"><img class="brand-original" src="../assets/marca/logo-intro.webp" width="804" height="258" alt="Línea de Pase"></a><span class="edition">Del campo al dato.</span><a href="#pasaporte">Mi pasaporte ↗</a></header><nav aria-label="Áreas de Línea de Pase">{nav}</nav><main id="contenido"><section class="hero"><div class="hero-copy"><p class="eyebrow">FÚTBOL / DATOS / PREGUNTAS</p><h1>No solo mires el fútbol.<br><em>Experiméntalo.</em></h1><p>Un museo vivo para explorar su historia, comprender su presente y jugar con sus posibilidades.</p><a class="cta" href="#datalab">Entra en el laboratorio ↗</a><p class="prototype">Prototipo de desarrollo · sin publicar</p></div><aside class="hero-note" aria-label="Pregunta para empezar"><div class="note-top"><span>Cuaderno de campo</span><span>N.º 01</span></div><p class="question">¿Jugar mejor<br>es ganar?</p><div class="pencil-line" aria-hidden="true"></div><p class="note-foot">El marcador es un comienzo.<br>La pregunta viene después.</p><a href="#titulo-explorador">Buscar una respuesta en los datos →</a></aside></section>{recorridos}{body}</main><footer><a class="brand" href="../">Línea de Pase</a><p>Ángel Marqueta Alonso · Ciencia de datos aplicada al fútbol</p><a href="../sobre-mi/">Sobre el proyecto</a> · <a href="../privacidad/">Privacidad</a><p>Los contenidos conservan sus direcciones originales. Este espacio es una versión en desarrollo.</p></footer><script src="../assets/linea2-core.js" defer></script><script src="../assets/linea2.js" defer></script><script src="../assets/linea2-experiencias.js" defer></script><script src="../assets/linea2-cuaderno.js" defer></script><script src="../assets/linea2-editorial.js" defer></script><script src="../assets/linea2-museo.js" defer></script><script src="../assets/linea2-secuencia.js" defer></script></body></html>'''
 (D/'index.html').write_text(html,encoding='utf-8')
if __name__=='__main__': build()

