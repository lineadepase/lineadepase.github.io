"""Comparador didáctico y ficha de investigación del prototipo."""

def scenario_lab():
    controls=''
    for code,name,n,p in [('a','A',10,10),('b','B',2,50)]:
        controls+=f'''<div class="scenario"><h4>Escenario {name}</h4><label for="escenario-{code}-n">Disparos de {name}: <output id="escenario-{code}-n-valor">{n}</output></label><input id="escenario-{code}-n" type="range" min="1" max="30" value="{n}"><label for="escenario-{code}-p">Probabilidad por disparo de {name}: <output id="escenario-{code}-p-valor">{p} %</output></label><input id="escenario-{code}-p" type="range" min="0" max="100" value="{p}"><dl><dt>Goles esperados</dt><dd id="escenario-{code}-xg">1</dd><dt>Probabilidad de al menos un gol</dt><dd id="escenario-{code}-gol" class="result"></dd></dl></div>'''
    return '<article class="lab-wide" aria-labelledby="titulo-escenarios"><p class="eyebrow">EXPERIMENTO 04 · COMPARA DOS ESCENARIOS</p><h3 id="titulo-escenarios">Mismo xG, distinta historia</h3><p>Diez ocasiones pequeñas o dos grandes: ¿es lo mismo sumar 1 gol esperado?</p><div class="scenario-grid">'+controls+'</div><p id="escenarios-lectura" role="status"></p><button id="escenarios-restablecer" type="button">Volver al ejemplo de 1 xG</button><details><summary>Qué estamos comparando</summary><p>Cada escenario supone remates independientes y una probabilidad constante dentro del escenario. El valor esperado es n × p; la probabilidad de marcar al menos una vez es 1 − (1 − p)ⁿ. Tener el mismo valor esperado no obliga a tener la misma distribución de goles.</p><p>No es una recomendación táctica ni un modelo de partido: no se incluyen rivales, posesiones, tiempo ni dificultad variable entre remates.</p></details><noscript><p>El ejemplo A suma 1 xG con 10 remates al 10 %; el B, con 2 al 50 %. La probabilidad de al menos un gol es aproximadamente 65,1 % en A y 75 % en B.</p></noscript></article>'

RESEARCH_FIELDS=[
 ('pregunta','Pregunta de investigación',300,'¿Qué quieres averiguar?'),
 ('hipotesis','Hipótesis inicial',500,'¿Qué esperas encontrar y qué resultado la pondría en duda?'),
 ('fuentes','Datos y fuentes',1200,'Anota procedencia, fecha de corte, cobertura y condiciones de uso.'),
 ('metodo','Método',1200,'Explica las variables, el procedimiento y una referencia con la que comparar.'),
 ('validacion','Validación',1200,'¿Cómo comprobarás el resultado con datos que no hayas usado para ajustar?'),
 ('limites','Límites del análisis',1000,'¿Qué conclusiones no permiten sacar estos datos?')
]
def research_form():
    fields=''
    for key,label,limit,hint in RESEARCH_FIELDS:
        required=' required' if key=='pregunta' else ''
        fields+=f'<div><label for="pro-{key}">{label}</label><p class="field-hint" id="pro-{key}-ayuda">{hint}</p><textarea id="pro-{key}" maxlength="{limit}" rows="3" aria-describedby="pro-{key}-ayuda"{required}></textarea></div>'
    return '<form id="pro-ficha" class="research-form"><p class="eyebrow">CUADERNO DE INVESTIGACIÓN</p><h3>Deja preparada la pregunta antes de calcular</h3><p>Completa una ficha de trabajo. Es un borrador personal, no un resultado validado. Puedes guardarlo en este navegador o descargarlo; no se envía a ningún servicio.</p><div class="research-fields">'+fields+'</div><p id="pro-estado" role="status"></p><div><button type="submit">Descargar ficha de investigación</button><button id="pro-guardar" type="button">Guardar borrador en este navegador</button><button id="pro-borrar" type="button">Borrar borrador</button></div><noscript><p>Para guardar o descargar la ficha necesitas JavaScript. Puedes copiar tus respuestas a un documento.</p></noscript></form>'
