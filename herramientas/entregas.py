"""Herramientas y entrega editorial de la última jornada, sin enviar publicaciones."""
from pathlib import Path
from html import escape as e
import json
import textwrap
from urllib.parse import urlsplit
from datetime import date

ROOT = Path(__file__).resolve().parents[1]


def latest_delivery():
    data=json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    latest=max(data['partidos'],key=lambda row:row['jornada'])
    number=str(latest['jornada'])
    editorial=json.loads((ROOT/'datos/entregas-zaragoza.json').read_text(encoding='utf-8'))
    clues=json.loads((ROOT/'datos/claves-editoriales.json').read_text(encoding='utf-8'))
    # Una entrega exige lectura y pregunta revisadas para esa jornada.
    if number not in editorial or number not in clues:
        return None
    return data,latest,editorial[number],clues[number]


def generate_tools(page):
    body='<div class="herramientas-rejilla"><article class="herramienta"><p class="etiqueta">Dos equipos</p><h2>Comparador del Grupo 2</h2><p>Resultados, goles, xG y ocasiones, por partido o en totales. La media del grupo y la cobertura acompañan a cada indicador.</p><a class="boton lleno" href="../comparador/index.html">Abrir el comparador</a><ul class="preguntas-herramienta"><li><a href="../comparador/index.html?a=Real+Zaragoza&amp;b=Villarreal+B&amp;sede=Casa&amp;modo=promedio&amp;periodo=toda&amp;fuente=sofascore">Zaragoza y Villarreal B: rendimiento en casa</a></li><li><a href="../comparador/index.html?a=Real+Zaragoza&amp;b=Real+Murcia&amp;sede=&amp;modo=promedio&amp;periodo=ultimas5&amp;fuente=sofascore">Zaragoza y Murcia: las últimas cinco jornadas</a></li></ul></article><article class="herramienta"><p class="etiqueta">Veinte equipos</p><h2>Mapa del Grupo 2</h2><p>Una vista conjunta para situar a cada equipo según dos indicadores, con filtros de sede, periodo y fuente de xG.</p><a class="boton lleno" href="../mapa-grupo/index.html">Abrir el mapa</a><ul class="preguntas-herramienta"><li><a href="../mapa-grupo/index.html?equipo=Real+Zaragoza&amp;x=xg&amp;y=xgc&amp;sede=&amp;periodo=toda&amp;fuente=sofascore">Peligro generado y concedido en el grupo</a></li><li><a href="../mapa-grupo/index.html?equipo=Real+Zaragoza&amp;x=puntos&amp;y=xg&amp;sede=&amp;periodo=ultimas5&amp;fuente=sofascore">Puntos y xG en las últimas cinco jornadas</a></li></ul></article></div><p class="nota">Primera Federación · Grupo 2 · 2026/27. El corte de datos aparece en cada herramienta. La cobertura puede variar entre equipos y métricas.</p><div class="enlaces"><a class="boton" href="../conceptos/index.html">Entender los indicadores</a><a class="boton" href="../proyectos/real-zaragoza/grupo-2.html#metodo-grupo">Fuentes y método</a></div>'
    (ROOT/'herramientas').mkdir(exist_ok=True)
    (ROOT/'herramientas/index.html').write_text(page('Herramientas para explorar el Grupo 2','Una pregunta futbolística como punto de partida: comparar dos equipos o situarlos dentro de la competición.',body),encoding='utf-8')


def generate_delivery(page):
    info=latest_delivery()
    if info is None:
        # La web no conserva como actual una entrega anterior sin revisión.
        body='<p>La próxima entrega breve está pendiente de revisión editorial.</p><a class="boton" href="../proyectos/real-zaragoza/jornadas.html">Consultar los partidos publicados</a>'
    else:
        data,match,editorial,clues=info
        j=match['jornada']
        home=match['sede']=='Casa'
        rival=match['rival']
        title='Real Zaragoza – '+rival if home else rival+' – Real Zaragoza'
        score=f"{match['goles_favor']}–{match['goles_contra']}" if home else f"{match['goles_contra']}–{match['goles_favor']}"
        match_date=date.fromisoformat(match['fecha']).strftime('%d/%m/%Y')
        detail=f'proyectos/real-zaragoza/jornada-{j}.html'
        group=json.loads((ROOT/'datos/comparador-grupo2.json').read_text(encoding='utf-8'))
        row=next(r for r in group['partidos'] if r['equipo']=='Real Zaragoza' and r['jornada']==j)
        host=urlsplit(row.get('fuente_xg','')).hostname or ''
        if host!='sofascore.com' and not host.endswith('.sofascore.com'):
            raise ValueError('La fuente de xG de la entrega requiere revisión editorial.')
        chart_path=f'assets/entregas/zaragoza-j{j}.png'
        draw_chart(match,row,editorial,clues,ROOT/chart_path)
        canonical='https://lineadepase.com/'+detail
        social=f"Tras la jornada · J{j}\n{title} {score}\n\n{editorial['pregunta']}\n{clues['conclusion']}\n\n{clues['dato']}\n\nAnálisis, fuentes y contexto:"
        body=f'<p class="etiqueta">Real Zaragoza · 2026/27 · Jornada {j}</p><h2 class="pregunta-entrega">{e(editorial["pregunta"])}</h2><p class="entradilla">{e(clues["conclusion"])}</p><p class="nota">{e(title)} · {score} · Partido del <time datetime="{match["fecha"]}">{match_date}</time>.</p>'
        body+=f'<figure class="grafico-entrega"><a href="../{chart_path}" aria-label="Ampliar el gráfico de la jornada {j}"><img src="../{chart_path}" width="1200" height="900" alt="{e(title,quote=True)}: {score}. {e(clues["dato"],quote=True)}"></a><figcaption>{e(clues["dato"])} Fuente del gráfico: Sofascore; xG del encuentro, sin mezclar proveedores.</figcaption></figure>'
        body+='<div class="lectura-entrega"><h2>La lectura</h2><p>'+e(clues['lectura'])+'</p></div>'
        body+=f'<div class="enlaces"><a class="boton lleno" href="../{detail}#titulo-claves">Leer el análisis completo</a><a class="boton" href="../{chart_path}" download="linea-de-pase-zaragoza-j{j}.png">Descargar imagen (PNG)</a><a class="boton" href="../proyectos/real-zaragoza/evolucion.html">Situar el partido en la temporada</a></div>'
        body+='<details class="compartir-entrega"><summary>Preparar esta entrega para redes</summary><p>El texto y la imagen se pueden copiar y descargar. El selector identifica el origen del enlace; la publicación se realiza desde la red elegida.</p><label for="canal-entrega">Canal<select id="canal-entrega"><option value="redes">Enlace general para redes</option><option value="linkedin">LinkedIn</option><option value="instagram">Instagram</option><option value="facebook">Facebook</option></select></label>'
        body+=f'<label for="texto-entrega">Texto de la entrega<textarea id="texto-entrega" rows="10" readonly data-enlace="{canonical}">{e(social)}\n{canonical}?utm_source=redes&amp;utm_medium=social&amp;utm_campaign=zaragoza-2026-27-j{j}</textarea></label><button class="boton" id="copiar-entrega" type="button">Copiar texto y enlace</button><p id="estado-entrega" role="status"></p></details><script src="../assets/entrega.js?v=20261021f" defer></script>'
    body+='<p class="nota">La serie parte de una pregunta, un gráfico propio y una lectura breve de cada partido. Las entregas se actualizan después de revisar los datos y el análisis.</p><a class="boton" href="../proyectos/real-zaragoza/jornadas.html">Volver a las jornadas</a>'
    (ROOT/'tras-la-jornada').mkdir(exist_ok=True)
    (ROOT/'tras-la-jornada/index.html').write_text(page('Tras la jornada','El último partido del Zaragoza, en una pregunta, un gráfico y una lectura breve.',body),encoding='utf-8')


def draw_chart(match,row,editorial,clues,path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter, MaxNLocator
    j=match['jornada']
    fig=plt.figure(figsize=(12,9),dpi=100,facecolor='#f7f9f5')
    fig.text(.07,.94,f'TRAS LA JORNADA · REAL ZARAGOZA · J{j}',color='#1f6b3e',weight='bold',size=15)
    fig.text(.07,.855,'\n'.join(textwrap.wrap(editorial['pregunta'],48)),size=25,weight='bold',color='#0f2418',va='top')
    fig.text(.07,.69,f"Partido del {date.fromisoformat(match['fecha']).strftime('%d/%m/%Y')} · Temporada 2026/27",size=12,color='#4d6356')
    ax=fig.add_axes([.24,.37,.65,.23],facecolor='#f7f9f5')
    values=[row['xg'],row['xg_rival']]
    labels=['Real Zaragoza',match['rival']]
    if any(value is None for value in values):
        plt.close(fig)
        raise ValueError('La entrega necesita los dos xG documentados.')
    bars=ax.barh(labels,values,color=['#1f6b3e','#82998a'],height=.5)
    ax.invert_yaxis()
    ax.set_xlim(0,max(1,max(values)*1.28))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,_:f'{x:g}'.replace('.',',')))
    ax.tick_params(axis='both',labelsize=13,length=0,pad=12,colors='#0f2418')
    ax.set_axisbelow(True)
    ax.grid(axis='x',color='#dbe3dc')
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.set_xlabel('Goles esperados (xG) del partido',fontsize=13,labelpad=15,color='#4d6356')
    for bar,value in zip(bars,values):
        ax.text(bar.get_width()+ax.get_xlim()[1]*.025,bar.get_y()+bar.get_height()/2,f'{value:.2f}'.replace('.',','),va='center',weight='bold',size=16,color='#0f2418')
    score=f"{match['goles_favor']}–{match['goles_contra']}"
    fig.text(.07,.23,f'Marcador desde el Zaragoza: {score}',size=16,weight='bold',color='#0f2418')
    fig.text(.07,.18,'El xG describe la calidad de los tiros; no determina quién mereció ganar.',size=12,color='#4d6356')
    fig.text(.07,.105,'Fuente: Sofascore · Elaboración propia con los datos documentados del encuentro.',size=11,color='#4d6356')
    fig.text(.07,.055,'Línea de pase · lineadepase.com',size=15,weight='bold',color='#1f6b3e')
    path.parent.mkdir(exist_ok=True)
    fig.savefig(path,dpi=100,metadata={'Title':f'Tras la jornada · J{j}','Author':'Ángel G. Marqueta Alonso'})
    plt.close(fig)
