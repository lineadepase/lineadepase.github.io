"""Portada editorial y mapa del grupo, con las fuentes del seguimiento existente."""
from pathlib import Path
from html import escape as e
import json
import re

ROOT=Path(__file__).resolve().parents[1]


def generate_anual_visual():
    data=json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    played=[row for row in data['partidos'] if int(row['jornada'])<=int(data['jornada'])]
    goals_for=sum(int(row['goles_favor']) for row in played)
    goals_against=sum(int(row['goles_contra']) for row in played)
    xt_page=(ROOT/'proyectos/liga-f-xt/index.html').read_text(encoding='utf-8')
    territory=(ROOT/'proyectos/futbol-femenino/index.html').read_text(encoding='utf-8')
    xt=re.search(r'(0,\d+) xT neto por 90 minutos',xt_page)
    share=re.search(r'(28,6) %.{0,150}?(23,4) %',territory,re.S)
    if not xt or not share:
        raise ValueError('No se encuentran las cifras publicadas para la lámina anual.')
    teams=json.loads((ROOT/'datos/comparador-grupo2.json').read_text(encoding='utf-8'))
    team_count=len({row['equipo'] for row in teams['partidos']})
    sim_page=(ROOT/'proyectos/real-zaragoza/simulacion.html').read_text(encoding='utf-8')
    simulations=re.search(r'(\d[\d.]+) simulaciones',sim_page)
    if not simulations:
        raise ValueError('No se encuentra el número publicado de simulaciones.')
    issue=f"J{int(data['jornada']):02d}"
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1740" role="img" aria-labelledby="titulo descripcion">
<title id="titulo">Línea de pase · Cuaderno visual 2026</title><desc id="descripcion">Cuatro proyectos publicados: seguimiento del Real Zaragoza tras {int(data['jornada'])} jornadas, {simulations[1]} simulaciones de una competición de {team_count} equipos, {xt[1]} xT neto por 90 minutos en la Liga F 2023/24 y comparación territorial de población y licencias de fútbol femenino.</desc>
<rect width="1200" height="1740" fill="#f3f5ef"/><path d="M0 0h1200v320H0z" fill="#103b24"/><path d="M900 0h300v320H900z" fill="#174a30"/><path d="M930 0v320m90-320v320m90-320v320M900 106h300m-300 106h300" stroke="#b9d4c2" stroke-opacity=".15" stroke-width="2"/>
<text x="70" y="82" fill="#bed8c4" font-family="Arial,sans-serif" font-size="24" font-weight="700" letter-spacing="5">LÍNEA DE PASE · CUADERNO VISUAL</text><text x="66" y="188" fill="#f7f8f4" font-family="Arial,sans-serif" font-size="84" font-weight="800">2026</text><text x="70" y="252" fill="#e0e9e2" font-family="Arial,sans-serif" font-size="34">Cuatro proyectos. Cuatro formas de mirar el juego.</text>
<path d="M70 340h1060" stroke="#ff7a2f" stroke-width="7"/><circle cx="70" cy="340" r="11" fill="#ff7a2f"/>
<g font-family="Arial,sans-serif"><rect x="64" y="392" width="1072" height="270" rx="18" fill="#fff" stroke="#d4ded6" stroke-width="2"/><rect x="64" y="392" width="12" height="270" rx="6" fill="#245b9b"/><text x="110" y="448" fill="#536257" font-size="24" font-weight="700" letter-spacing="3">01 · SEGUIMIENTO DE TEMPORADA</text><text x="110" y="552" fill="#163e28" font-size="92" font-weight="800">{issue}</text><text x="110" y="605" fill="#293c30" font-size="30">{len(played)} partidos · {goals_for} goles a favor · {goals_against} en contra</text><path d="M870 456h180m-180 34h130m-130 34h160m-160 34h100" stroke="#245b9b" stroke-width="6" stroke-linecap="round" opacity=".65"/><circle cx="1080" cy="558" r="18" fill="#ff7a2f"/>
<rect x="64" y="688" width="1072" height="270" rx="18" fill="#fff" stroke="#d4ded6" stroke-width="2"/><rect x="64" y="688" width="12" height="270" rx="6" fill="#597c2d"/><text x="110" y="744" fill="#536257" font-size="24" font-weight="700" letter-spacing="3">02 · SIMULACIÓN DEL GRUPO</text><text x="110" y="848" fill="#365722" font-size="84" font-weight="800">{simulations[1]}</text><text x="110" y="901" fill="#293c30" font-size="30">temporadas simuladas · {team_count} equipos</text><path d="M870 895c55-115 105-12 155-100s95 5 122-67" fill="none" stroke="#597c2d" stroke-width="8" stroke-linecap="round"/><circle cx="870" cy="895" r="10" fill="#597c2d"/><circle cx="1147" cy="728" r="12" fill="#ff7a2f"/>
<rect x="64" y="984" width="1072" height="270" rx="18" fill="#fff" stroke="#d4ded6" stroke-width="2"/><rect x="64" y="984" width="12" height="270" rx="6" fill="#387b79"/><text x="110" y="1040" fill="#536257" font-size="24" font-weight="700" letter-spacing="3">03 · AMENAZA ESPERADA · LIGA F 2023/24</text><text x="110" y="1144" fill="#276c68" font-size="84" font-weight="800">{xt[1]}</text><text x="110" y="1197" fill="#293c30" font-size="30">xT neto por 90 minutos</text><path d="M855 1190h235m-180-72 55-50 54 30 73-100" fill="none" stroke="#387b79" stroke-width="7" stroke-linecap="round" stroke-dasharray="2 13"/><circle cx="1087" cy="998" r="14" fill="#ff7a2f"/>
<rect x="64" y="1280" width="1072" height="270" rx="18" fill="#fff" stroke="#d4ded6" stroke-width="2"/><rect x="64" y="1280" width="12" height="270" rx="6" fill="#8a5a82"/><text x="110" y="1336" fill="#536257" font-size="24" font-weight="700" letter-spacing="3">04 · FÚTBOL FEMENINO · TERRITORIO</text><text x="110" y="1440" fill="#744c70" font-size="68" font-weight="800">{share[1]}% <tspan fill="#aeb8b0" font-size="40">/</tspan> {share[2]}%</text><text x="110" y="1493" fill="#293c30" font-size="26">población femenina / licencias en dos comunidades</text><circle cx="955" cy="1415" r="62" fill="none" stroke="#8a5a82" stroke-width="3"/><circle cx="1050" cy="1415" r="62" fill="none" stroke="#c7a6c4" stroke-width="3"/><path d="M985 1415h35" stroke="#ff7a2f" stroke-width="7" stroke-linecap="round"/>
</g><text x="70" y="1625" fill="#405448" font-family="Arial,sans-serif" font-size="25" font-weight="700">Cifras tomadas de los proyectos publicados en Línea de pase.</text><text x="70" y="1670" fill="#64766b" font-family="Arial,sans-serif" font-size="21">Cada estudio conserva su temporada, corte, fuentes y método en la página correspondiente.</text><text x="70" y="1710" fill="#64766b" font-family="Arial,sans-serif" font-size="20">lineadepase.com · Edición 2026</text></svg>'''
    folder=ROOT/'assets/ilustraciones'
    folder.mkdir(exist_ok=True)
    (folder/'anuario-visual-2026.svg').write_text(svg,encoding='utf-8')
    cards=[
        ('01 · SEGUIMIENTO DE TEMPORADA',issue,f'{len(played)} partidos · {goals_for} goles a favor · {goals_against} en contra','#245b9b',72),
        ('02 · SIMULACIÓN DEL GRUPO',simulations[1],f'temporadas simuladas · {team_count} equipos','#597c2d',72),
        ('03 · AMENAZA ESPERADA · LIGA F 2023/24',xt[1],'xT neto por 90 minutos','#387b79',72),
        ('04 · FÚTBOL FEMENINO · TERRITORIO',f'{share[1]}%  /  {share[2]}%','población femenina / licencias en dos comunidades','#8a5a82',56),
    ]
    def tile(x,y,width,height,index,label,value,detail,color,value_size):
        label_y=y+(43 if height<300 else 55)
        value_y=y+(116 if height<300 else 177)
        detail_y=y+(158 if height<300 else 229)
        motif=(f'<path d="M{x+width-126} {y+height-60}h62m-62 16h43m-43 16h55" stroke="{color}" stroke-width="4" stroke-linecap="round" opacity=".65"/><circle cx="{x+width-37}" cy="{y+height-38}" r="10" fill="#ff7a2f"/>') if width>700 else ''
        return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="18" fill="#fff" stroke="#d4ded6" stroke-width="2"/><rect x="{x}" y="{y}" width="10" height="{height}" rx="5" fill="{color}"/>'
                f'<text x="{x+30}" y="{label_y}" fill="#536257" font-size="18" font-weight="700" letter-spacing="2">{label}</text>'
                f'<text x="{x+30}" y="{value_y}" fill="{color}" font-size="{value_size}" font-weight="800">{value}</text>'
                f'<text x="{x+30}" y="{detail_y}" fill="#293c30" font-size="19">{detail}</text>'
                +motif)
    def make_social(name,width,height,vertical=False,landscape=False):
        if vertical:
            header_h=190; card_h=216; gap=22; margin=48; y0=218
            placements=[(margin,y0+i*(card_h+gap),width-2*margin,card_h,i,*card) for i,card in enumerate(cards)]
            title_y=72; year_y=130; subtitle_y=167; foot_y=1285
            subtitle_size=22
        elif landscape:
            header_h=126; margin=36; gap=18; card_w=(width-2*margin-gap)//2; card_h=214
            positions=[(margin,145),(margin+card_w+gap,145),(margin,378),(margin+card_w+gap,378)]
            placements=[(*positions[i],card_w,card_h,i,*card) for i,card in enumerate(cards)]
            title_y=34; year_y=76; subtitle_y=111; foot_y=624; subtitle_size=17
        else:
            header_h=190; margin=48; gap=24; card_w=(width-2*margin-gap)//2; card_h=356
            positions=[(margin,220),(margin+card_w+gap,220),(margin,600),(margin+card_w+gap,600)]
            placements=[(*positions[i],card_w,card_h,i,*card) for i,card in enumerate(cards)]
            title_y=64; year_y=119; subtitle_y=164; foot_y=1032; subtitle_size=20
        tile_markup=''.join(tile(x,y,w,h,i+1,label,value,detail,color,value_size if w>700 else min(value_size,56)) for x,y,w,h,i,label,value,detail,color,value_size in placements)
        source=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="titulo descripcion"><title id="titulo">Línea de pase · Cuaderno visual 2026</title><desc id="descripcion">Resumen gráfico de cuatro proyectos publicados con sus temporadas y cifras.</desc><rect width="{width}" height="{height}" fill="#f3f5ef"/><path d="M0 0h{width}v{header_h}H0z" fill="#103b24"/><path d="M0 {header_h-4}h{width}" stroke="#ff7a2f" stroke-width="7"/><text x="{margin}" y="{title_y}" fill="#bed8c4" font-family="Arial,sans-serif" font-size="17" font-weight="700" letter-spacing="3">LÍNEA DE PASE · CUADERNO VISUAL</text><text x="{margin}" y="{year_y}" fill="#f7f8f4" font-family="Arial,sans-serif" font-size="48" font-weight="800">2026</text><text x="{margin}" y="{subtitle_y}" fill="#e0e9e2" font-family="Arial,sans-serif" font-size="{subtitle_size}">Cuatro proyectos. Cuatro formas de mirar el juego.</text><g font-family="Arial,sans-serif">{tile_markup}</g><text x="{margin}" y="{foot_y}" fill="#405448" font-family="Arial,sans-serif" font-size="17" font-weight="700">Cifras de los proyectos publicados · cortes y métodos en cada estudio.</text><text x="{margin}" y="{foot_y+30}" fill="#64766b" font-family="Arial,sans-serif" font-size="16">lineadepase.com · Edición 2026</text></svg>'''
        (folder/name).write_text(source,encoding='utf-8')
    make_social('anuario-visual-2026-cuadrado.svg',1080,1080)
    make_social('anuario-visual-2026-vertical.svg',1080,1350,True)
    make_social('anuario-visual-2026-apaisado.svg',1200,675,landscape=True)


def generate_matchday_visual():
    """Crea una pieza de marcador basada en el partido más reciente del registro."""
    data=json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    match=max(data['partidos'],key=lambda row:int(row['jornada']))
    date_parts=match['fecha'].split('-')
    months=['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC']
    date_label=f'{date_parts[2]} {months[int(date_parts[1])-1]} {date_parts[0]}'
    home=match['rival'] if match['sede']=='Fuera' else 'Real Zaragoza'
    away='Real Zaragoza' if match['sede']=='Fuera' else match['rival']
    home_goals=match['goles_contra'] if match['sede']=='Fuera' else match['goles_favor']
    away_goals=match['goles_favor'] if match['sede']=='Fuera' else match['goles_contra']
    winner=match['resultado'].upper()
    place='FUERA' if match['sede']=='Fuera' else 'EN CASA'

    def svg(width,height,square=False):
        header_h=245 if square else 155
        panel_y=285 if square else 184
        panel_h=475 if square else 300
        left_margin=55 if square else 48
        panel_w=width-2*left_margin
        label_y=panel_y+(140 if square else 91)
        score_y=panel_y+(302 if square else 202)
        team_size=38 if square else 30
        score_size=138 if square else 112
        note_y=panel_y+panel_h+81
        line_y=panel_y+(390 if square else 250)
        stamp_y=height-40
        description=f'{home} {home_goals}–{away_goals} {away}. Jornada {int(match["jornada"])} de Primera Federación 2026/27, {date_label}. Resultado registrado en el seguimiento del Real Zaragoza.'
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="titulo descripcion">
<title id="titulo">Jornada {int(match['jornada'])} · {home_goals}–{away_goals}</title><desc id="descripcion">{e(description)}</desc>
<rect width="{width}" height="{height}" fill="#f3f5ef"/><path d="M0 0h{width}v{header_h}H0z" fill="#103b24"/><path d="M{width-190} 0h190v{header_h}H{width-190}z" fill="#174a30"/><g fill="none" stroke="#bed8c4" stroke-opacity=".16" stroke-width="2"><path d="M{width-170} 0v{header_h}M{width-112} 0v{header_h}M{width-54} 0v{header_h}M{width-190} {header_h//3}h190M{width-190} {2*header_h//3}h190"/></g>
<text x="{left_margin+10}" y="{46 if square else 35}" fill="#bed8c4" font-family="Arial,sans-serif" font-size="20" font-weight="700" letter-spacing="3">LÍNEA DE PASE · PRIMERA FEDERACIÓN</text>
<text x="{left_margin+8}" y="{117 if square else 91}" fill="#f7f8f4" font-family="Arial,sans-serif" font-size="{48 if square else 40}" font-weight="800">Jornada {int(match['jornada']):02d}</text>
<text x="{left_margin+10}" y="{166 if square else 128}" fill="#e0e9e2" font-family="Arial,sans-serif" font-size="{24 if square else 21}">Grupo 2 · Temporada 2026/27</text>
<rect x="{left_margin}" y="{panel_y}" width="{panel_w}" height="{panel_h}" rx="24" fill="#fff" stroke="#d4ded6" stroke-width="2"/><path d="M{left_margin} {panel_y+panel_h-13}h{panel_w}" stroke="#ff7a2f" stroke-width="8"/>
<text x="{width*.25:.1f}" y="{label_y}" text-anchor="middle" fill="#536257" font-family="Arial,sans-serif" font-size="{team_size}" font-weight="700">{e(home)}</text>
<text x="{width*.75:.1f}" y="{label_y}" text-anchor="middle" fill="#163e28" font-family="Arial,sans-serif" font-size="{team_size}" font-weight="700">{e(away)}</text>
<text x="{width*.42:.1f}" y="{score_y}" text-anchor="middle" fill="#536257" font-family="Arial,sans-serif" font-size="{score_size}" font-weight="800">{home_goals}</text><text x="{width*.50:.1f}" y="{score_y-8}" text-anchor="middle" fill="#ff7a2f" font-family="Arial,sans-serif" font-size="{score_size*.64:.0f}" font-weight="700">–</text><text x="{width*.58:.1f}" y="{score_y}" text-anchor="middle" fill="#163e28" font-family="Arial,sans-serif" font-size="{score_size}" font-weight="800">{away_goals}</text>
<path d="{width*.25:.1f} {line_y}h{width*.5:.1f}" stroke="#d4ded6" stroke-width="2"/><text x="{width/2:.0f}" y="{note_y}" text-anchor="middle" fill="#245b9b" font-family="Arial,sans-serif" font-size="22" font-weight="700" letter-spacing="2">{winner} · {place}</text>
<text x="{left_margin+8}" y="{stamp_y}" fill="#405448" font-family="Arial,sans-serif" font-size="19" font-weight="700">{date_label} · RESULTADO REGISTRADO</text><text x="{width-left_margin-8}" y="{stamp_y}" text-anchor="end" fill="#64766b" font-family="Arial,sans-serif" font-size="18">lineadepase.com</text></svg>'''

    folder=ROOT/'assets/ilustraciones'
    folder.mkdir(exist_ok=True)
    for name,width,height,square in [('resultado-real-zaragoza-ultima-jornada.svg',1200,630,False),('resultado-real-zaragoza-ultima-jornada-cuadrado.svg',1080,1080,True)]:
        (folder/name).write_text(svg(width,height,square),encoding='utf-8')


def generate_map(page):
    data=json.loads((ROOT/'datos/comparador-grupo2.json').read_text(encoding='utf-8'))
    from cortes import nota_corte_grupo
    seguimiento=json.loads((ROOT/'datos/zaragoza.json').read_text(encoding='utf-8'))
    corte=nota_corte_grupo(data['jornada'],data['fecha'],seguimiento['jornada'],seguimiento['corte'])
    teams=sorted({r['equipo'] for r in data['partidos']})
    metrics=[('xg','xG a favor por partido'),('xgc','xG en contra por partido'),('puntos','Puntos por partido'),('gf','Goles a favor por partido'),('gc','Goles en contra por partido'),('tiros','Tiros por partido'),('claras','Ocasiones claras por partido'),('posesion','Posesión media (%)')]
    body='<p class="nota corte-datos">Primera Federación · Temporada 2026/27. '+e(corte)+' Cada punto representa un equipo; las líneas discontinuas señalan las medias con los filtros elegidos. <a href="../proyectos/real-zaragoza/grupo-2.html#metodo-grupo">Cobertura y método</a>.</p><div class="leyenda-visual-global" aria-label="Leyenda del mapa"><span><i class="marca-visual"></i>Equipo del grupo</span><span><i class="marca-visual destacado"></i>Equipo destacado</span><span><i class="marca-visual media"></i>Media del grupo</span></div><div class="archivo-controles" id="controles-mapa" hidden>'
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
    match_visual=('<figure class="resultado-portada-visual" data-jornada="'+e(str(j))+'" data-fecha-partido="'+e(str(latest['fecha']))+'"><a href="proyectos/real-zaragoza/ultimo-partido.html" aria-label="Abrir el análisis de '+e(title)+'"><img src="assets/ilustraciones/resultado-real-zaragoza-ultima-jornada.png" width="1200" height="630" loading="lazy" alt="Marcador final de '+e(title)+' · Jornada '+e(str(j))+'"></a><figcaption>Marcador · Jornada '+e(str(j))+'</figcaption></figure>')
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
        detail_visual=('<section class="detalle-que-cambia" aria-labelledby="titulo-detalle-visual"><div class="detalle-que-cambia-texto"><p class="etiqueta">Un dato, con contexto · Jornada '+e(str(j))+'</p><h2 id="titulo-detalle-visual">El balón no cuenta todo el partido</h2><details class="detalle-visual-contexto"><summary>Añadir el contexto del partido</summary><p>'+e(context)+'</p></details><a class="enlace-editorial" href="proyectos/real-zaragoza/jornada-'+e(str(j))+'.html#titulo-claves">Ver el análisis completo →</a></div><figure class="detalle-visual-dato" aria-label="Dato destacado del partido"><p class="detalle-visual-cifra">'+str(possession)+'<span>%</span></p><figcaption>Posesión del Real Zaragoza</figcaption><div class="detalle-visual-barra" role="img" aria-label="El Real Zaragoza tuvo el balón el '+str(possession)+' por ciento del tiempo"><span style="width:'+str(possession)+'%"></span></div><p class="detalle-visual-pareja">'+e(title)+'</p></figure></section>')
    html=f"""<main>
<section class="apertura-editorial apertura-visual"><div class="envoltorio apertura-visual-rejilla">
  <div class="apertura-texto"><p class="etiqueta">Línea de pase · Fútbol y datos</p><h1>El juego, más allá del marcador.</h1><p class="entradilla">Partidos, protagonistas y contexto para entender el fútbol con datos.</p><p class="firma-editorial">Por Ángel G. Marqueta Alonso</p><div class="rutas-portada"><a class="boton lleno" href="proyectos/real-zaragoza/jornada-{j}.html#titulo-claves">Leer el último análisis</a><a class="boton" href="proyectos/index.html">Descubrir los proyectos</a></div></div>
  <figure class="foto foto-portada portada-ilustrada"><a class="entrada-fotografica" href="proyectos/real-zaragoza/plantilla.html"><img src="assets/ilustraciones/juego-en-perspectiva.svg" width="720" height="540" fetchpriority="high" alt="Ilustración original de un campo y una trayectoria gráfica, sin representar un partido concreto"><span>Leer los datos de la plantilla →</span></a><figcaption>Ilustración vectorial original · Sin posiciones de un partido real.</figcaption></figure>
</div></section>
<div class="envoltorio">
<section class="actualidad-editorial actualidad-compacta"><article class="analisis-principal"><p class="etiqueta">Último partido de liga · Jornada {j}</p><div class="titulo-resultado"><h2><a href="proyectos/real-zaragoza/jornada-{j}.html">{e(title)}</a></h2><p class="marcador-editorial">{score}</p></div>{match_visual}{question}<p class="entradilla">{e(lead)}</p><p class="fecha-datos">{date} · Temporada 2026/27</p><div class="enlaces">{brief}<a class="enlace-editorial" href="proyectos/real-zaragoza/jornada-{j}.html#titulo-claves">El análisis completo →</a></div></article><aside class="mesa-de-datos"><p class="etiqueta">Para explorar</p><h2>Haz tu propia comparación</h2><a class="imagen-menu-comparador" href="comparador/index.html" aria-label="Abrir el comparador de equipos"><img src="assets/ilustraciones/comparador-grupo2.webp" width="1672" height="941" loading="lazy" alt="Ilustración editorial de dos equipos comparados sobre un campo de fútbol"><span class="solo-lectores">Abrir el comparador de equipos</span></a><a href="comparador/index.html"><strong>Dos equipos, frente a frente →</strong><span>Resultados, ocasiones y contexto.</span></a><a href="mapa-grupo/index.html"><strong>El mapa del Grupo 2 →</strong><span>Veinte equipos en una misma vista.</span></a><a href="archivo/index.html"><strong>Buscar un análisis →</strong><span>Por rival, temporada o tema.</span></a><a href="marcador-a-ciegas/index.html"><strong>El marcador a ciegas →</strong><span>¿Qué cuentan los tiros y la posesión?</span></a><a href="preguntas-del-partido/index.html"><strong>Preguntas del partido →</strong><span>Lo que se planteó antes y se comprobó después.</span></a></aside></section>
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
