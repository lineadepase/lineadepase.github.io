"""Orientación entre áreas y recorridos de trabajo con proyectos existentes."""
from html import escape

PURPOSES = {
 'datalab': ('EXPERIMENTAR', '¿Qué ocurre si cambio una variable?', 'Manipula un experimento o explora un análisis. Observa el resultado y comprueba sus supuestos.', 'Te llevas una comparación, un resultado o una pregunta mejor formulada.', 'Para ver una explicación, entra en Media. Para preparar una lámina, pasa a Studio.'),
 'studio': ('CREAR UNA PIEZA', '¿Cómo cuento lo que he encontrado?', 'Elige datos existentes, revisa su cobertura y prepara una comparación, un mapa o un borrador.', 'Te llevas un archivo gráfico o un texto para revisar y compartir.', 'Si todavía necesitas comprobar la idea, vuelve a DataLab. La ficha de método está en Pro.'),
 'media': ('VER Y COMPRENDER', '¿Me lo explicas con un ejemplo?', 'Encuentra vídeos y lecturas sobre fútbol y datos. Después puedes probar la idea por ti mismo.', 'Te llevas una explicación y un siguiente paso para profundizar.', 'Los experimentos están en DataLab. Las herramientas para crear piezas están en Studio.'),
 'pro': ('INVESTIGAR Y DOCUMENTAR', '¿Cómo sostengo una conclusión con evidencia?', 'Revisa proyectos reales, contrasta fuentes y deja por escrito tu pregunta, método, validación y límites.', 'Te llevas una ficha de investigación y referencias para continuar el trabajo.', 'Los experimentos didácticos están en DataLab. La preparación de piezas está en Studio.'),
}

def purpose(area):
    if area not in PURPOSES: return ''
    label,question,action,output,boundary = PURPOSES[area]
    return f'<aside class="area-purpose" aria-label="Para qué sirve esta área"><div><p class="eyebrow">{label}</p><h3>{question}</h3><p>{action}</p></div><div><p class="purpose-output">{output}</p><p class="purpose-boundary">{boundary}</p></div></aside>'


def professional_routes():
    cases = [
      ('01 / MODELOS', 'Revisar un modelo de amenaza', 'Liga F · xT', 'Comprueba qué representa el valor de cada zona, con qué datos se ajusta y cómo se comprueba el resultado.', 'Separar el ajuste del modelo de su validación y anotar qué acciones quedan fuera.', 'proyectos/liga-f-xt/'),
      ('02 / PERFILES', 'Interpretar grupos de jugadoras', 'Liga F · perfiles', 'Revisa las variables y la construcción de los perfiles antes de comparar dos jugadoras.', 'Distinguir similitud estadística, contexto del equipo y valoración deportiva.', 'proyectos/liga-f-perfiles/'),
      ('03 / TERRITORIO', 'Plantear un estudio de oportunidad', 'Fútbol femenino · territorio', 'Examina las tasas y fuentes territoriales. Anota qué información local necesitarías antes de tomar una decisión.', 'Diferenciar un indicador territorial de una demanda comprobada con clubes y participantes.', 'proyectos/futbol-femenino/'),
    ]
    cards=''
    for number,title,context,task,learning,path in cases:
        cards+=f'<article class="pro-case"><p class="eyebrow">{number}</p><h4>{title}</h4><p class="case-context">{context}</p><p>{task}</p><p><strong>Qué revisar:</strong> {learning}</p><a href="../{path}">Abrir el proyecto y sus fuentes →</a></article>'
    return '''<article class="pro-workbench" aria-labelledby="pro-rutas-titulo"><p class="eyebrow">MESA DE TRABAJO / PROYECTOS EXISTENTES</p><h3 id="pro-rutas-titulo">Tres maneras de trabajar con evidencia</h3><p>Elige un caso para estudiar su procedimiento. Son accesos a trabajos ya disponibles, no encargos nuevos ni resultados generados para tu pregunta.</p><div class="pro-cases">'''+cards+'''</div><p><a href="#pro-ficha">Preparar mi propia ficha de investigación ↓</a></p></article>
<details class="pro-example"><summary>Ver una ficha de ejemplo: tiros en casa y fuera</summary><p class="eyebrow">EJEMPLO DE PLAN / SIN RESULTADOS CALCULADOS</p><dl><dt>Pregunta</dt><dd>¿Cómo cambia el promedio de tiros del Zaragoza entre los partidos en casa y fuera dentro del mismo corte de datos?</dd><dt>Fuentes</dt><dd>Fichas del seguimiento del Zaragoza y CSV del explorador. Revisar la fecha de corte y la cobertura de cada jornada.</dd><dt>Método</dt><dd>Incluir únicamente jornadas con estadísticas completas. Separar por sede y presentar el número de partidos y el promedio de tiros de cada grupo.</dd><dt>Comprobación</dt><dd>Contrastar los totales exportados con las fichas originales. Documentar las discrepancias y comprobar cuánto cambia el promedio al retirar una jornada.</dd><dt>Límites</dt><dd>Los rivales y el contexto pueden ser distintos. La ausencia de estadísticas puede sesgar la muestra. Una diferencia entre promedios no demuestra que la sede la cause.</dd></dl><p>Esta ficha ilustra cómo preparar un análisis; no afirma que se haya observado una diferencia ni que exista una conclusión validada.</p><p><a href="#titulo-explorador">Abrir los datos del Zaragoza →</a> · <a href="#pro-ficha">Redactar mi ficha →</a></p></details>'''
