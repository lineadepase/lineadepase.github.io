"""Experiencias adicionales para el prototipo, sin dependencias externas."""
from html import escape
from datetime import date
from html.parser import HTMLParser
import json


def share_controls(kind):
    return f'<div class="share-view"><button id="{kind}-enlace" type="button" hidden>Preparar enlace de esta vista</button><div id="{kind}-compartir" hidden><label for="{kind}-url">Enlace para copiar</label><input id="{kind}-url" type="url" readonly><p role="status">El enlace conserva los controles de esta vista. No incluye tu nota ni tu pasaporte.</p></div></div>'

def laboratories():
    return '''<article class="lab-wide" aria-labelledby="titulo-distribucion"><p class="eyebrow">EXPERIMENTO 02 · TODOS LOS RESULTADOS</p><h3 id="titulo-distribucion">El promedio no es un destino</h3><p>Usa los controles de disparos y probabilidad del primer experimento. Aquí puedes ver la probabilidad de cada marcador de goles, no solo la de marcar al menos una vez.</p><p id="distribucion-resumen" role="status"></p><div class="table-scroll" role="region" aria-label="Distribución de goles" tabindex="0"><table><caption>Distribución binomial exacta del modelo didáctico</caption><thead><tr><th scope="col">Goles</th><th scope="col">Probabilidad</th><th scope="col">Vista relativa al resultado más probable</th></tr></thead><tbody id="distribucion-cuerpo"></tbody></table></div><noscript><p>Activa JavaScript para calcular la distribución al mover los controles.</p></noscript><details><summary>¿Por qué cambia el resultado?</summary><p>El valor esperado es n × p, pero una serie concreta puede acabar por encima o por debajo. La tabla enumera los resultados de un modelo de n disparos independientes con probabilidad p constante. Las barras se escalan al resultado más probable; los porcentajes muestran las probabilidades absolutas.</p></details></article><article class="experiment" aria-labelledby="titulo-muestra"><div><p class="eyebrow">EXPERIMENTO 03 · TAMAÑO DE MUESTRA</p><h3 id="titulo-muestra">¿Cuánto sabes con pocos remates?</h3><p>Construye una muestra ficticia y observa cuánto cambia la incertidumbre.</p><label for="muestra-tiros">Disparos de la muestra: <output id="muestra-n">20</output></label><input id="muestra-tiros" type="range" min="1" max="500" value="20"><label for="muestra-goles">Goles observados: <output id="muestra-k">4</output></label><input id="muestra-goles" type="range" min="0" max="20" value="4"></div><div><p>Tasa observada e intervalo de Wilson al 95 %</p><p id="muestra-resultado" class="result" aria-live="polite"></p><div class="interval" aria-hidden="true"><span id="muestra-intervalo"></span></div><p id="muestra-lectura"></p><details><summary>Comprende la incertidumbre</summary><p>Este intervalo aproxima la incertidumbre de una proporción bajo un modelo binomial: ensayos independientes con la misma probabilidad. En repeticiones del procedimiento, el nivel nominal de cobertura es el 95 %; no significa que haya un 95 % de probabilidad de que este intervalo concreto contenga el parámetro.</p><p>Los disparos reales tienen distinta dificultad. Esta demostración no estima el talento de un jugador ni sustituye un modelo de xG.</p><a href="https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm">Referencia del método: NIST</a></details><noscript><p>Activa JavaScript para calcular la tasa y su intervalo.</p></noscript></div></article>'''+'<div class="laboratorios-enlaces">'+share_controls('laboratorios')+'</div>'


class ArchiveRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.matches = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'tr' and attrs.get('data-comparison-id'):
            key = (attrs.get('data-jornada'), attrs.get('data-fecha-partido'), attrs.get('data-rival'))
            if key in self.matches and self.matches[key] != attrs['data-comparison-id']:
                raise ValueError('Identificación ambigua de una jornada en el archivo visual')
            self.matches[key] = attrs['data-comparison-id']


def season(data, archive=''):
    parser = ArchiveRows()
    parser.feed(archive)
    cutoff = date.fromisoformat(data['corte'])
    matches = sorted((m for m in data.get('partidos', []) if m.get('goles_favor') is not None and m.get('goles_contra') is not None and date.fromisoformat(m['fecha']) <= cutoff), key=lambda m: (m['fecha'], m['jornada']))
    keys = ['jornada','fecha','rival','sede','goles_favor','goles_contra','completo','tiros_zaragoza','tiros_rival','posesion_pct']
    records = []
    rows = ''
    for match in matches:
        record = {key: match.get(key) for key in keys}
        record['completo'] = match.get('completo') is True
        if not record['completo']:
            for key in ('tiros_zaragoza','tiros_rival','posesion_pct'):
                record[key] = None
        archive_id = parser.matches.get((str(match['jornada']), match['fecha'], match['rival']))
        record['archivo_id'] = archive_id
        records.append(record)
        choose = f'<label class="compare-choice" hidden><input type="checkbox" data-compare-id="{escape(archive_id, quote=True)}" hidden>Elegir J{match["jornada"]}</label>' if archive_id else 'No disponible'
        coverage = 'Completa' if record['completo'] else 'Pendiente'
        rows += f'<tr data-season-row="{match["jornada"]}"><td>{choose}</td><th scope="row"><a href="../proyectos/real-zaragoza/jornada-{match["jornada"]}.html">J{match["jornada"]}</a></th><td>{escape(match["fecha"])}</td><td>{escape(match["rival"])}</td><td>{escape(match["sede"])}</td><td>{match["goles_favor"]}–{match["goles_contra"]}</td><td>{coverage}</td></tr>'
    payload = json.dumps({'corte':data['corte'], 'partidos':records},ensure_ascii=False).replace('<',r'\u003c').replace('>',r'\u003e').replace('&',r'\u0026')
    return f'''<article class="lab-wide" aria-labelledby="titulo-explorador"><p class="eyebrow">EXPLORADOR DE TEMPORADA · CORTE {escape(data['corte'])}</p><h3 id="titulo-explorador">Hazle una pregunta a la temporada</h3><p>¿Qué cambia entre casa y fuera? ¿Cuántas fichas sostienen una media? Explora los resultados de liga disponibles, con su cobertura.</p><div id="temporada-controles" class="filter-grid" hidden><div><label for="temporada-sede">Sede</label><select id="temporada-sede"><option>Todas</option><option>Casa</option><option>Fuera</option></select></div><div><label for="temporada-resultado">Resultado</label><select id="temporada-resultado"><option>Todos</option><option>Victoria</option><option>Empate</option><option>Derrota</option></select></div><div><label for="temporada-cobertura">Cobertura estadística</label><select id="temporada-cobertura"><option>Todas</option><option>Solo completas</option></select></div></div><div class="summary-grid" id="temporada-resumen" role="status"><p>{len(matches)} resultados de liga disponibles.</p></div><p id="temporada-metricas"></p><p id="temporada-vacia" hidden>No hay partidos que cumplan estos filtros. Prueba otra combinación.</p><div class="table-scroll" role="region" aria-label="Resultados del Zaragoza" tabindex="0"><table><caption>Marcadores en orden Zaragoza–rival. Abre cada jornada para consultar sus fuentes.</caption><thead><tr><th scope="col">Studio</th><th scope="col">Jornada</th><th scope="col">Fecha</th><th scope="col">Rival</th><th scope="col">Sede</th><th scope="col">Marcador</th><th scope="col">Ficha estadística</th></tr></thead><tbody>{rows}</tbody></table></div><div id="temporada-comparar" hidden><p id="temporada-seleccion" role="status">Elige dos jornadas de la tabla para compararlas en Studio.</p><a id="temporada-studio" class="cta" href="../archivo-visual/#titulo-comparar" hidden>Abrir las dos jornadas en Studio →</a><button id="temporada-redaccion" type="button" hidden>Preparar publicación con estas jornadas</button></div><div id="temporada-acciones" hidden><button id="temporada-restablecer" type="button">Restablecer filtros</button><button id="temporada-csv" type="button">Descargar selección CSV</button></div><p>Los marcadores incluyen todas las fichas; las medias usan únicamente datos disponibles de fichas completas y muestran su muestra. Filtrar por resultado describe esa selección: no demuestra causalidad ni predice partidos.</p>{share_controls("temporada")}<p><a href="../datos-en-revision/">Consultar discrepancias y datos en revisión</a></p><script type="application/json" id="temporada-datos">{payload}</script></article>'''


def routes():
    return '''<aside class="routes" aria-label="Recorridos sugeridos"><p class="eyebrow">ELIGE POR DÓNDE EMPEZAR</p><div class="grid"><article><h2>Tengo curiosidad</h2><p>Una pregunta, un experimento y una sorpresa.</p><a href="#datalab">Experimentar con el azar →</a></article><article><h2>Sigo al Zaragoza</h2><p>Del resultado de la jornada al contexto de la temporada.</p><a href="#titulo-explorador">Explorar la temporada →</a></article><article><h2>Quiero crear</h2><p>Encuentra una comparación y conviértela en una lámina.</p><a href="#studio">Entrar en Studio →</a></article></div></aside>'''
