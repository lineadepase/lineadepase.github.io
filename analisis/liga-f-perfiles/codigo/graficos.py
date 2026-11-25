"""Gráficos de la investigación con la identidad de Línea de pase (analisis/comun/estilo.py).

Formatos: web y LinkedIn 1600 × 900, Facebook 1200 × 630, Instagram 1080 × 1350 (carrusel de 8).
Las jugadoras se identifican con una chapa de iniciales y el color de su perfil. Si existe
recursos/fotos/<identificador>.jpg (una foto con licencia propia), la chapa la muestra en su lugar.
"""
from pathlib import Path
import sys
import unicodedata

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from PIL import Image

ESTUDIO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ESTUDIO.parent / 'comun'))
from estilo import FORMATOS, PX, TEXTO, TITULAR, cierre, colores, estilo_ejes, guardar, lienzo, preparar  # noqa: E402

SALIDA = ESTUDIO / 'datos' / 'salida'
GRAFICOS = ESTUDIO / 'graficos'
LOGO = ESTUDIO / 'recursos' / 'statsbomb.png'
FOTOS = ESTUDIO / 'recursos' / 'fotos'
ETIQUETA = 'Investigación 02 · Liga F'
PIE = ('Liga F 2023/24 · Fuente: StatsBomb Open Data\n'
       '{n} jugadoras de campo con al menos 900 minutos · Variables por 90 minutos · Agrupación con k-means')
COLORES = ['#2f6db5', '#1f6b3e', '#7b4fa3', '#ff6a2b']
MARCAS = ['o', 's', '^', 'D']
NOMBRES = ['Iniciadoras', 'Pulmones', 'Las de área', 'Desequilibrantes']
LEMA = ['Sacan el balón jugando', 'Presionan, cortan y recuperan', 'Viven cerca del área rival', 'Rompen el partido con el balón']
DESCRIPCION = [
    'Centrales y laterales que inician la jugada: más pases largos y progresivos que nadie y muy poco juego cerca del área.',
    'El motor del equipo: presionan, recuperan e intersectan más que el resto, con un papel discreto en ataque.',
    'Delanteras y extremos que reciben en el área y presionan arriba, casi sin progresar con el balón.',
    'Las que más amenaza generan: pases de tiro, centros, regates y xT muy por encima de las demás.',
]
RADAR = [('xt_neto_90', 'Amenaza\n(xT)'), ('pases_prog_90', 'Pases\nprogresivos'), ('cond_prog_90', 'Conducción'),
         ('pases_largos_90', 'Pases\nlargos'), ('pases_clave_90', 'Pases\nde tiro'), ('recepciones_area_90', 'Recibe\nen el área'),
         ('presiones_90', 'Presión'), ('recuperaciones_90', 'Recupera')]
VISIBLE = {'Aitana Bonmati': 'Aitana Bonmatí', 'Manuela Vanegas Cataño': 'Manuela Vanegas', 'Leicy Maria Santos Herrera': 'Leicy Santos',
           'Camila Alejandra Saez Oyaneder': 'Camila Sáez', 'Andreia de Jesus Jacinto': 'Andreia Jacinto',
           'Jessica Dahiana Martínez Villagra': 'Jessica Martínez', 'Sanni Maija Franssi': 'Sanni Franssi'}


def cargar():
    d = pd.read_csv(SALIDA / 'jugadoras_perfiles.csv')
    centros = pd.read_csv(SALIDA / 'perfiles_centros_z.csv', index_col='perfil')
    resumen = pd.read_csv(SALIDA / 'perfiles_resumen.csv')
    equipos = pd.read_csv(SALIDA / 'perfiles_por_equipo.csv', index_col='equipo')[NOMBRES]
    return d, centros, resumen, equipos


def corto(nombre):
    nombre = VISIBLE.get(nombre, nombre)
    partes = nombre.split()
    if len(nombre) <= 22:
        return nombre
    return f'{partes[0]} {partes[-1]}'


def dos_lineas(nombre):
    p = nombre.split()
    return nombre if len(p) < 2 else p[0] + '\n' + ' '.join(p[1:])


def identificador(nombre):
    t = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode().lower()
    return '-'.join(t.replace('.', '').split())


def iniciales(nombre):
    p = VISIBLE.get(nombre, nombre).split()
    return (p[0][0] + p[-1][0]).upper()


def equipo_corto(e):
    return {'Barcelona WFC': 'Barcelona', 'Atletico Madrid W': 'Atlético', 'Real Madrid CF W': 'Real Madrid',
            'Athletic Club Bilbao': 'Athletic', 'Real Sociedad de Fútbol': 'Real Sociedad', 'Real Betis Balompié': 'Betis',
            'CD Sporting de Huelva': 'Sporting Huelva', 'Costa Adeje Tenerife': 'Tenerife', 'FC Levante Badalona': 'Levante Badalona',
            'Levante UD Femenino': 'Levante', 'Granada W': 'Granada', 'Madrid CFF': 'Madrid CFF', 'SD Eibar': 'Eibar',
            'Sevilla FC': 'Sevilla', 'Valencia CF': 'Valencia', 'Villarreal': 'Villarreal'}.get(e, e)


# --------------------------------------------------------------------------- piezas
class Px:
    """Capa transparente con coordenadas en píxeles (origen arriba a la izquierda)."""
    def __init__(self, fig, z=10):
        self.W, self.H = fig.get_figwidth() * 100, fig.get_figheight() * 100
        self.fig = fig
        self.ax = fig.add_axes([0, 0, 1, 1], zorder=z)
        self.ax.set_xlim(0, self.W); self.ax.set_ylim(self.H, 0); self.ax.axis('off'); self.ax.patch.set_alpha(0)

    def marco(self, x, y, w, h):
        return [x / self.W, 1 - (y + h) / self.H, w / self.W, h / self.H]

    def chapa(self, x, y, r, perfil, nombre, c):
        ruta = FOTOS / f'{identificador(nombre)}.jpg'
        self.ax.add_patch(Circle((x, y), r + 3, color=c['papel'], zorder=3))
        if ruta.exists():
            img = Image.open(ruta).convert('RGB').resize((int(2 * r), int(2 * r)))
            ejes = self.fig.add_axes(self.marco(x - r, y - r, 2 * r, 2 * r), zorder=12)
            ejes.imshow(img); ejes.axis('off')
            recorte = Circle((r, r), r, transform=ejes.transData)
            ejes.images[0].set_clip_path(recorte)
        else:
            self.ax.add_patch(Circle((x, y), r, color=COLORES[perfil], zorder=4))
            self.ax.text(x, y + r * 0.04, iniciales(nombre), ha='center', va='center', color='white', fontsize=r * 0.62 / PX * 1.0,
                         fontfamily=TITULAR, fontweight=800, zorder=5)


RADAR_CORTO = ['xT', 'Progresión', 'Conducción', 'Largos', 'Pase de tiro', 'Área', 'Presión', 'Recupera']


def radar(fig, marco, valores, color, c, tam=11, etiquetas=True, relleno=0.28, cortas=False):
    """Radar de puntuaciones z (de -2 a +2); el aro discontinuo es la media de todas las jugadoras."""
    ax = fig.add_axes(marco, polar=True, zorder=20)
    n = len(valores)
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = np.clip((np.array(valores) + 2) / 4, 0.03, 1)
    ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
    ax.set_ylim(0, 1); ax.set_yticks([]); ax.grid(color=c['linea'], linewidth=0.8)
    ax.set_xticks(ang)
    ax.set_xticklabels((RADAR_CORTO if cortas else [e for _, e in RADAR]) if etiquetas else [], fontsize=tam, color=c['tinta_suave'], linespacing=1.0)
    ax.tick_params(axis='x', pad=tam * 0.9)
    ax.spines['polar'].set_visible(False)
    ax.set_facecolor('none')
    ax.plot(np.linspace(0, 2 * np.pi, 100), [0.5] * 100, color=c['tinta_suave'], linewidth=1, linestyle=(0, (3, 3)), alpha=0.8)
    ax.fill(np.r_[ang, ang[0]], np.r_[r, r[0]], color=color, alpha=relleno)
    ax.plot(np.r_[ang, ang[0]], np.r_[r, r[0]], color=color, linewidth=2.6)
    ax.scatter(ang, r, s=26, color=color, zorder=5)
    return ax


def valores_radar(centros, perfil):
    return [centros.loc[perfil, v] for v, _ in RADAR]


def seleccion(d, perfil, n=3):
    g = d[d.perfil == perfil]
    return g.nsmallest(n, 'prototipo'), g.nsmallest(n, 'cima')


def leyenda(px, x, y, c, tam=15, separacion=22):
    ren = px.ax.figure.canvas.get_renderer()
    for i, nombre in enumerate(NOMBRES):
        px.ax.scatter([x], [y], s=tam * 11, marker=MARCAS[i], color=COLORES[i], zorder=6, linewidths=0)
        t = px.ax.text(x + 18, y, nombre, va='center', fontsize=tam, color=c['tinta'], fontweight=600, zorder=6)
        fin = px.ax.transData.inverted().transform((t.get_window_extent(ren).x1, 0))[0]
        x = fin + 14 + separacion


# --------------------------------------------------------------------------- mapa
def se_cruzan(a, b):
    """Indica si dos segmentos ((x, y), (x, y)) se cortan."""
    def lado(p, q, r):
        return np.sign((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]))
    return lado(a[0], a[1], b[0]) * lado(a[0], a[1], b[1]) < 0 and lado(b[0], b[1], a[0]) * lado(b[0], b[1], a[1]) < 0


def pisa(segmento, bb):
    """Indica si un segmento atraviesa la caja de una etiqueta."""
    a, b = np.asarray(segmento[0]), np.asarray(segmento[1])
    return any(bb.x0 <= x <= bb.x1 and bb.y0 <= y <= bb.y1 for x, y in (a + (b - a) * k for k in np.linspace(0, 1, 40)))


def etiquetar(ax, puntos, c, tam):
    """Etiqueta jugadoras sin confundirlas: aro en su punto, línea hasta el nombre y,
    entre los huecos probados, el que no pisa otra etiqueta y tapa menos puntos."""
    fig = ax.figure
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    nube = np.vstack([col.get_offsets() for col in ax.collections])
    nube = ax.transData.transform(nube)
    marcados = ax.transData.transform([(x, y) for x, y, *_ in puntos])
    ax.scatter([p[0] for p in puntos], [p[1] for p in puntos], s=230, facecolors='none',
               edgecolors=c['tinta'], linewidths=1.5, zorder=6, clip_on=False)
    caja = ax.get_window_extent(ren)
    ocupadas, lineas = [], []
    desplazamientos = [(r * np.cos(np.radians(a)), r * np.sin(np.radians(a)))
                       for r in (22, 34, 48, 64, 84, 108) for a in (35, 145, -35, -145, 90, -90, 0, 180, 60, 120, -60, -120)]
    for (x, y, texto, color), origen in zip(puntos, marcados):
        mejor = None
        for orden, (dx, dy) in enumerate(desplazamientos):
            ha = 'left' if dx > 1 else 'right' if dx < -1 else 'center'
            va = 'bottom' if dy > 1 else 'top' if dy < -1 else 'center'
            t = ax.annotate(texto, (x, y), xytext=(dx, dy), textcoords='offset points', ha=ha, va=va, fontsize=tam,
                            color=c['tinta'], fontweight=700, zorder=8)
            bb = t.get_window_extent(ren).expanded(1.04, 1.25)
            t.remove()
            if not (caja.x0 <= bb.x0 and bb.x1 <= caja.x1 and caja.y0 <= bb.y0 and bb.y1 <= caja.y1):
                continue
            if any(bb.overlaps(o) for o in ocupadas):
                continue
            tapados = sum(bb.x0 - 4 <= px <= bb.x1 + 4 and bb.y0 - 4 <= py <= bb.y1 + 4 for px, py in nube)
            aros = sum(bb.x0 - 8 <= px <= bb.x1 + 8 and bb.y0 - 8 <= py <= bb.y1 + 8 for px, py in marcados)
            linea = (origen, origen + np.array([dx, dy]) * fig.dpi / 72)
            cruces = sum(se_cruzan(linea, otra) for otra in lineas)
            cruces += sum(pisa(linea, o) for o in ocupadas) + sum(pisa(otra, bb) for otra in lineas)
            coste = 10 * tapados + 100 * aros + 300 * cruces + orden * 0.15
            if mejor is None or coste < mejor[0]:
                mejor = (coste, dx, dy, ha, va, bb, linea)
        if mejor is None:
            raise ValueError(f'No hay hueco para la etiqueta de {texto}')
        _, dx, dy, ha, va, bb, linea = mejor
        ax.annotate(texto, (x, y), xytext=(dx, dy), textcoords='offset points', ha=ha, va=va, fontsize=tam,
                    color=c['tinta'], fontweight=700, zorder=8,
                    bbox=dict(boxstyle='round,pad=0.12', fc=c['papel'], ec='none', alpha=0.9),
                    arrowprops=dict(arrowstyle='-', color=c['tinta'], linewidth=1, shrinkA=0, shrinkB=9))
        ocupadas.append(bb)
        lineas.append(linea)


def dibujar_mapa(ax, d, c, etiquetadas, tam_pt=60, tam_texto=11):
    estilo_ejes(ax, rejilla=None)
    ax.spines['left'].set_visible(False); ax.spines['bottom'].set_visible(False)
    ax.axhline(0, color=c['linea'], linewidth=1, zorder=1); ax.axvline(0, color=c['linea'], linewidth=1, zorder=1)
    for i in range(4):
        g = d[d.perfil == i]
        ax.scatter(g.pc1, g.pc2, s=tam_pt, marker=MARCAS[i], color=COLORES[i], alpha=0.82, edgecolor=c['papel'], linewidth=0.8, zorder=3)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(d.pc1.min() - 0.5, d.pc1.max() + 0.5); ax.set_ylim(d.pc2.min() - 0.5, d.pc2.max() + 0.5)
    pts = [(r.pc1, r.pc2, corto(r.jugadora), COLORES[r.perfil]) for r in etiquetadas.itertuples()]
    etiquetar(ax, pts, c, tam_texto)


def jugadoras_mapa(d, por_perfil=2):
    """Las más extremas de cada perfil (cima) y las más típicas (prototipo), para anclar la lectura."""
    partes = [d[d.perfil == i].nsmallest(por_perfil, 'cima') for i in range(4)]
    partes += [d[d.perfil == i].nsmallest(1, 'prototipo') for i in range(4)]
    return pd.concat(partes).drop_duplicates('jugadora_id')


def mapa(formato, d, nombre):
    c = preparar()
    vertical = formato == 'instagram'
    if formato == 'facebook':
        titulo, sub = 'Cuatro perfiles en la Liga F', 'Cada punto es una jugadora; las que se parecen quedan juntas.'
    else:
        titulo = 'Cada punto, una jugadora:\ncuatro perfiles en la Liga F'
        sub = ('Las jugadoras que se parecen en lo que hacen con y sin balón quedan juntas.\n'
               'Arriba, más progresión y recuperación; a la derecha, más cerca del área rival.')
    fig, area = lienzo(formato, titulo, sub,
                       pie=PIE.format(n=len(d)), etiqueta=ETIQUETA, logo_fuente=LOGO)
    px = Px(fig)
    area[3] -= 34 / px.H; area[1] += 34 / px.H
    if formato == 'facebook':
        area[1] -= 8 / px.H; area[3] += 8 / px.H
    ax = fig.add_axes(area)
    dibujar_mapa(ax, d, c, jugadoras_mapa(d, 2 if not vertical else 2), tam_pt=70 if not vertical else 80,
                 tam_texto=12 if formato != 'facebook' else 10)
    leyenda(px, 60 + 8, px.H - (area[1] * px.H) + 12 - 0, c) if False else None
    y_leyenda = px.H - area[1] * px.H + 26
    leyenda(px, 70, y_leyenda, c, tam=13 if formato == 'facebook' else 15)
    guardar(fig, GRAFICOS, nombre)


# --------------------------------------------------------------------------- perfiles
def tarjeta_perfil(px, fig, d, centros, resumen, i, x, y, w, h, c, tam=1.0, compacta=False):
    px.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=10', fc=c['panel'], ec=c['linea'], lw=1.2, zorder=1))
    px.ax.add_patch(Rectangle((x, y), w, 7, color=COLORES[i], zorder=2))
    n = int((d.perfil == i).sum())
    px.ax.text(x + 18, y + 20, NOMBRES[i], fontfamily=TITULAR, fontweight=800, fontsize=27 * tam, color=COLORES[i] if i != 3 else c['acento_texto'], va='top', zorder=5)
    px.ax.text(x + 18, y + 20 + 42, LEMA[i], fontsize=12.5, color=c['tinta'], va='top', zorder=5)
    px.ax.text(x + 18, y + 20 + 62, f'{n} jugadoras', fontsize=11, color=c['tinta_suave'], va='top', zorder=5)
    bloque = 96
    rad = min(w - 120, h - 90 - 2 * bloque - 74)
    radar(fig, px.marco(x + (w - rad) / 2, y + 90 + 30, rad, rad), valores_radar(centros, i), COLORES[i], c, tam=8.5, cortas=True)
    proto, cima = seleccion(d, i, 3)
    y0 = y + 90 + 30 + rad + 40
    px.ax.text(x + 18, y0, 'LAS MÁS TÍPICAS', fontsize=10 * tam, color=c['tinta_suave'], fontweight=700, va='center', zorder=5)
    for k, r in enumerate(proto.itertuples()):
        cx = x + (k + 0.5) * w / 3
        px.chapa(cx, y0 + 28, 17, i, r.jugadora, c)
        px.ax.text(cx, y0 + 50, dos_lineas(corto(r.jugadora)), ha='center', va='top', fontsize=10, color=c['tinta'], fontweight=600, linespacing=1.1, zorder=5)
    y1 = y0 + bloque
    px.ax.text(x + 18, y1, 'LAS QUE MÁS LO LLEVAN AL EXTREMO', fontsize=10 * tam, color=c['tinta_suave'], fontweight=700, va='center', zorder=5)
    for k, r in enumerate(cima.itertuples()):
        cx = x + (k + 0.5) * w / 3
        px.chapa(cx, y1 + 28, 17, i, r.jugadora, c)
        px.ax.text(cx, y1 + 50, dos_lineas(corto(r.jugadora)), ha='center', va='top', fontsize=10, color=c['tinta'], fontweight=600, linespacing=1.1, zorder=5)


def perfiles(formato, d, centros, resumen, nombre):
    c = preparar()
    fig, area = lienzo(formato, 'Los cuatro perfiles de la Liga F',
                       'Resumen de lo que hace cada grupo de jugadoras por 90 minutos frente a la media de todas (aro discontinuo).',
                       pie=PIE.format(n=len(d)), etiqueta=ETIQUETA, logo_fuente=LOGO)
    px = Px(fig)
    top = px.H - (area[1] + area[3]) * px.H - 10
    base = px.H - 74 - 14
    w = (px.W - 120 - 3 * 18) / 4
    h = base - top
    for i in range(4):
        tarjeta_perfil(px, fig, d, centros, resumen, i, 60 + i * (w + 18), top, w, h, c, tam=0.92)
    guardar(fig, GRAFICOS, nombre)


def diapositiva_perfil(i, d, centros, resumen, nombre):
    c = preparar()
    rs = resumen.set_index('perfil').loc[i]
    fig, area = lienzo('instagram', f'{NOMBRES[i]}', LEMA[i], pie=PIE.format(n=len(d)), etiqueta=ETIQUETA, logo_fuente=LOGO)
    px = Px(fig)
    top = px.H - (area[1] + area[3]) * px.H
    px.ax.add_patch(Rectangle((60, top - 12), 200, 8, color=COLORES[i], zorder=3))
    rad = 470
    radar(fig, px.marco((px.W - rad) / 2, top + 50, rad, rad), valores_radar(centros, i), COLORES[i], c, tam=12.5)
    y = top + 50 + rad + 70
    px.ax.text(60, y, DESCRIPCION[i], fontsize=17, color=c['tinta'], va='top', linespacing=1.45, wrap=True, zorder=5) if False else None
    import textwrap
    px.ax.text(60, y, '\n'.join(textwrap.wrap(DESCRIPCION[i], 62)), fontsize=17, color=c['tinta'], va='top', linespacing=1.4, zorder=5)
    y += 108
    proto, cima = seleccion(d, i, 3)
    for titulo, grupo, yy in (('LAS MÁS TÍPICAS', proto, y), ('LAS QUE MÁS LO LLEVAN AL EXTREMO', cima, y + 112)):
        px.ax.text(60, yy, titulo, fontsize=12, color=c['tinta_suave'], fontweight=700, va='center', zorder=5)
        for k, r in enumerate(grupo.itertuples()):
            cx = 60 + 38 + k * 330
            px.chapa(cx, yy + 48, 30, i, r.jugadora, c)
            px.ax.text(cx + 42, yy + 48, f'{corto(r.jugadora)}\n{equipo_corto(r.equipo)}', fontsize=12.5, va='center', color=c['tinta'], fontweight=600, linespacing=1.3, zorder=5)
    guardar(fig, GRAFICOS, nombre)


# --------------------------------------------------------------------------- equipos
def equipos(formato, d, tabla, nombre):
    c = preparar()
    vertical = formato == 'instagram'
    barca = int(tabla.loc['Barcelona WFC', 'Desequilibrantes'])
    total = int(tabla['Desequilibrantes'].sum())
    sub = ('Jugadoras de campo con al menos 900 minutos, por perfil.' + ('\n' if vertical else ' ')
           + f'El Barcelona suma {barca} de las {total} desequilibrantes.')
    fig, area = lienzo(formato, '¿Cómo es tu equipo?\nPerfiles por plantilla', sub,
                       pie=PIE.format(n=len(d)), etiqueta=ETIQUETA, logo_fuente=LOGO)
    px = Px(fig)
    ax = fig.add_axes([area[0] + 0.11 if vertical else area[0] + 0.09, area[1] - 0.02, area[2] - (0.14 if vertical else 0.11), area[3] + 0.02])
    t = tabla.copy()
    t['tot'] = t.sum(axis=1)
    t = t.sort_values(['Desequilibrantes', 'tot'], ascending=True)
    y = np.arange(len(t)); izq = np.zeros(len(t))
    for i, n in enumerate(NOMBRES):
        ax.barh(y, t[n], left=izq, color=COLORES[i], height=0.74, edgecolor=c['papel'], linewidth=1.2, label=n, zorder=3)
        for yy, l, v in zip(y, izq, t[n]):
            if v >= 2:
                ax.text(l + v / 2, yy, int(v), ha='center', va='center', color='white', fontsize=10.5 if not vertical else 12, fontweight=700, zorder=5)
        izq += t[n].to_numpy()
    ax.set_yticks(y, [equipo_corto(e) for e in t.index], fontsize=11 if not vertical else 13)
    estilo_ejes(ax, rejilla=None); ax.spines['left'].set_visible(False); ax.spines['bottom'].set_visible(False)
    ax.set_xticks([]); ax.tick_params(axis='y', pad=6)
    leyenda(px, 70, px.H - (area[1] - 0.02) * px.H + 34, c, tam=14)
    guardar(fig, GRAFICOS, nombre)


# --------------------------------------------------------------------------- carrusel de Instagram
def portada_ig(d, nombre):
    """Portada de redes: ilustración de los cuatro perfiles (recursos/portada.jpg) con la pregunta encima."""
    c = preparar()
    ancho, alto = 1080, 1350
    fig = plt.figure(figsize=(ancho / 100, alto / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    fondo = np.asarray(Image.open(ESTUDIO / 'recursos' / 'portada.jpg').convert('RGB'))
    ax.imshow(fondo, extent=(0, ancho, alto, 0), interpolation='lanczos')
    # Sombra suave en la esquina inferior derecha para que el texto se lea bien.
    xx, yy = np.meshgrid(np.linspace(0, ancho, 270), np.linspace(0, alto, 338))
    sombra = np.zeros(xx.shape + (4,))
    sombra[..., 3] = 0.72 * np.clip((xx - 560) / 300, 0, 1) * np.clip((yy - 820) / 220, 0, 1)
    ax.imshow(sombra, extent=(0, ancho, alto, 0), interpolation='bilinear')
    ax.set_xlim(0, ancho); ax.set_ylim(alto, 0); ax.axis('off')
    for k, linea in enumerate(('¿En qué', 'perfil está', 'tu jugadora', 'favorita?')):
        ax.text(1040, 975 + k * 76, linea, ha='right', va='center', fontfamily=TITULAR, fontweight=800,
                fontsize=80 / PX, color=c['cal'])
    pie = ax.text(1040, 1306, f'Línea de pase · Liga F 2023/24', ha='right', va='center',
                  fontsize=22 / PX, fontweight=700, color=c['cal'])
    fig.canvas.draw()
    x0 = ax.transData.inverted().transform((pie.get_window_extent().x0, 0))[0]
    ax.scatter([x0 - 20], [1306], s=110, color=c['acento'], zorder=5)
    # Solo JPG: al ser una ilustración, un SVG pesaría megas sin aportar nada.
    fig.savefig(GRAFICOS / f'{nombre}.jpg', dpi=100, pil_kwargs={'quality': 92, 'optimize': True})
    plt.close(fig)


def cierre_ig(d, tabla, nombre):
    barca, madrid = tabla.loc['Barcelona WFC'], tabla.loc['Real Madrid CF W']
    fig = cierre('¿Y tu equipo?\nBúscalo en la web',
                 [f'Barcelona: {int(barca["Desequilibrantes"])} desequilibrantes, {int(barca["Iniciadoras"])} iniciadoras,\nninguna pulmón ni de área.',
                  f'Real Madrid: {int(madrid["Desequilibrantes"])} desequilibrantes,\nla segunda plantilla con más.',
                  f'En la web, las {len(d)} jugadoras con su perfil,\npara descargar.',
                  'En comentarios: ¿en qué perfil\npondrías a tu jugadora favorita?'])
    guardar(fig, GRAFICOS, nombre)


def crear_todo():
    GRAFICOS.mkdir(exist_ok=True)
    plt.rcParams['text.hinting'] = 'none'  # sin ajuste a píxel: interletrado regular en cualquier equipo
    d, centros, resumen, tabla = cargar()
    for f, n in (('web', '01_mapa_web'), ('linkedin', '01_mapa_linkedin'), ('facebook', '01_mapa_facebook'), ('instagram', '02_mapa_instagram')):
        mapa(f, d, n)
    perfiles('web', d, centros, resumen, '02_perfiles_web')
    perfiles('linkedin', d, centros, resumen, '02_perfiles_linkedin')
    equipos('web', d, tabla, '03_equipos_web')
    equipos('instagram', d, tabla, '07_equipos_instagram')
    portada_ig(d, '01_portada_instagram')
    for i in range(4):
        diapositiva_perfil(i, d, centros, resumen, f'0{3 + i}_perfil_{i + 1}_instagram')
    cierre_ig(d, tabla, '08_cierre_instagram')


if __name__ == '__main__':
    crear_todo()
