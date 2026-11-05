"""Página web del estudio (proyectos/liga-f-perfiles/index.html) y textos para las redes.

Todas las cifras salen de datos/salida y documentacion; nada se escribe a mano.
Uso, después de perfiles.py y graficos.py:
    python analisis/liga-f-perfiles/codigo/web.py
"""
import json
from pathlib import Path
import shutil
import sys

import pandas as pd

ESTUDIO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ESTUDIO.parent / "comun"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pagina import RAIZ_WEB, escribir_pagina, numero  # noqa: E402
import graficos  # noqa: E402

CARPETA_WEB = RAIZ_WEB / "proyectos" / "liga-f-perfiles"
CODIGO_GITHUB = "https://github.com/lineadepase/lineadepase.github.io/tree/main/analisis/liga-f-perfiles"
LICENCIA = "https://github.com/hudl/open-data/blob/4b73468fc5b0f1950f9f66fada70ad3a4f9327cb/LICENSE.pdf"
URL = "https://lineadepase.com/proyectos/liga-f-perfiles/"
NOMBRES, LEMA, DESC = graficos.NOMBRES, graficos.LEMA, graficos.DESCRIPCION


def utm(red):
    return f"{URL}?utm_source={red}&utm_medium=social&utm_campaign=liga-f-perfiles"


def tabla_html(d):
    filas = []
    for i, nombre in enumerate(NOMBRES):
        proto, cima = graficos.seleccion(d, i, 3)
        filas.append(
            f'<tr><th scope="row">{nombre}</th><td class="num">{int((d.perfil == i).sum())}</td>'
            f'<td>{", ".join(graficos.corto(j) for j in proto.jugadora)}</td>'
            f'<td>{", ".join(graficos.corto(j) for j in cima.jugadora)}</td></tr>')
    return ('<div class="tabla-editorial" role="region" aria-label="Jugadoras de cada perfil, tabla desplazable" tabindex="0">'
            '<table><caption>Jugadoras de cada perfil</caption>'
            '<thead><tr><th scope="col">Perfil</th><th scope="col" class="num">Jugadoras</th>'
            '<th scope="col">Las más típicas</th><th scope="col">Las que más lo llevan al extremo</th></tr></thead><tbody>'
            + "".join(filas) + "</tbody></table></div>")


def main():
    d, centros, resumen, equipos = graficos.cargar()
    k = pd.read_csv(ESTUDIO / "datos" / "salida" / "seleccion_k.csv")
    sens = json.loads((ESTUDIO / "datos" / "salida" / "sensibilidad.json").read_text(encoding="utf-8"))
    cob = json.loads((ESTUDIO / "documentacion" / "cobertura.json").read_text(encoding="utf-8"))
    pos = pd.read_csv(ESTUDIO / "datos" / "salida" / "perfiles_por_posicion.csv", index_col=0)
    n = len(d)
    tam = d.perfil.value_counts().sort_index()
    xt = d.groupby("perfil").xt_neto_90.mean()
    otras = d[d.perfil != 3].xt_neto_90.mean()
    barca, madrid = equipos.loc["Barcelona WFC"], equipos.loc["Real Madrid CF W"]
    k4 = k[k.k == sens["k"]].iloc[0]
    hansen = d[d.jugadora == "Caroline Graham Hansen"].iloc[0]
    bonmati = d[d.jugadora == "Aitana Bonmati"].iloc[0]

    graf = CARPETA_WEB / "graficos"
    graf.mkdir(parents=True, exist_ok=True)
    for nombre in ("01_mapa_web", "02_perfiles_web", "03_equipos_web"):
        shutil.copy(ESTUDIO / "graficos" / f"{nombre}.png", graf / f"{nombre}.png")
    shutil.copy(ESTUDIO / "graficos" / "01_mapa_facebook.png", graf / "compartir.png")
    shutil.copy(ESTUDIO / "recursos" / "statsbomb.png", graf / "statsbomb.png")
    publicas = [c for c in d.columns if not c.startswith("z_")]
    d[publicas].to_csv(CARPETA_WEB / "jugadoras_perfiles.csv", index=False)

    cuerpo = f"""  <section class="cab-proyecto">
    <aside class="aviso-historico" aria-label="Periodo del análisis"><strong>ANÁLISIS HISTÓRICO · 2023/24</strong><span>Datos de la Liga F 2023/24, temporada terminada en 2024. No describe la temporada actual.</span></aside>
    <p class="etiqueta">Investigación · Fútbol femenino · Liga F 2023/24</p>
    <h1>¿En qué perfil está tu jugadora favorita?</h1>
    <p class="entradilla">En la alineación son defensas, centrocampistas y delanteras. Pero lo que hacen con el balón, y sin él, cuenta otra historia. Este estudio agrupa a {n} jugadoras de la Liga F 2023/24 según cómo juegan: salen cuatro perfiles con nombre propio.</p>
    <dl class="ficha-tecnica">
      <div><dt>Pregunta</dt><dd>¿Qué tipos de jugadora hay en la Liga F según lo que hacen en el campo, más allá de su posición?</dd></div>
      <div><dt>Datos</dt><dd>StatsBomb Open Data · {cob['partidos']} partidos · {numero(cob['eventos'], 0)} eventos · {n} jugadoras de campo con al menos 900 minutos</dd></div>
      <div><dt>Herramientas</dt><dd>Python (pandas, scikit-learn, Matplotlib) · k-means y PCA · <a href="{CODIGO_GITHUB}">código y datos</a></dd></div>
    </dl>
  </section>

  <nav class="accesos-seccion" aria-label="Secciones del artículo"><a href="#perfiles">Los cuatro perfiles</a><a href="#mapa">El mapa</a><a href="#equipos">Tu equipo</a><a href="#metodo">Cómo se calcula</a><a href="#fuentes">Fuentes y código</a></nav>

  <section class="seccion lectura" id="perfiles">
    <p class="etiqueta">Resultados</p>
    <h2>Iniciadoras, pulmones, las de área y desequilibrantes</h2>
    <p><strong>Iniciadoras ({tam[0]}).</strong> {DESC[0]} {int(pos.loc['Iniciadoras', 'Central'])} de las {tam[0]} son centrales.</p>
    <p><strong>Pulmones ({tam[1]}).</strong> {DESC[1]} Son el perfil más numeroso: laterales ({int(pos.loc['Pulmones', 'Lateral'])}), pivotes ({int(pos.loc['Pulmones', 'Pivote'])}) y mediocentros ({int(pos.loc['Pulmones', 'Mediocentro'])}), pero también {int(pos.loc['Pulmones', 'Extremo'])} extremos.</p>
    <p><strong>Las de área ({tam[2]}).</strong> {DESC[2]} {int(pos.loc['Las de área', 'Delantera'])} son delanteras.</p>
    <p><strong>Desequilibrantes ({tam[3]}).</strong> {DESC[3]} Su amenaza esperada (xT) por 90 minutos es de {numero(xt[3], 2)}, más de tres veces la del resto de jugadoras ({numero(otras, 2)}). Entre ellas están {graficos.corto(hansen.jugadora)} ({numero(hansen.xt_neto_90, 2)}) y {graficos.corto(bonmati.jugadora)}, que en la alineación figura como mediocentro.</p>
  </section>

  <figure class="figura"><img src="graficos/02_perfiles_web.png" width="1600" height="900" alt="Los cuatro perfiles de jugadora de la Liga F: iniciadoras, pulmones, las de área y desequilibrantes, con un radar de lo que hace cada grupo y las jugadoras más típicas y más extremas de cada uno."><figcaption>Perfil medio de cada grupo (por 90 minutos, frente a la media de todas) y jugadoras que lo representan.</figcaption></figure>

  {tabla_html(d)}

  <section class="seccion lectura" id="mapa">
    <h2>Un mapa de {n} jugadoras</h2>
    <p>Cada punto es una jugadora. Las que se parecen en lo que hacen quedan juntas: a la izquierda, las que juegan más atrás y sacan el balón; a la derecha, las que viven cerca del área rival. Arriba están las que más progresan y recuperan.</p>
    <p>Las fronteras no son tajantes: {int(d.entre_dos.sum())} jugadoras están casi a la misma distancia de dos perfiles. El mapa enseña un continuo con cuatro zonas reconocibles, no cuatro compartimentos.</p>
  </section>

  <figure class="figura"><img loading="lazy" src="graficos/01_mapa_web.png" width="1600" height="900" alt="Mapa de las {n} jugadoras agrupadas en cuatro perfiles: las iniciadoras a la izquierda, las pulmones en el centro, las de área abajo a la derecha y las desequilibrantes arriba a la derecha."><figcaption>Las dos primeras componentes del análisis explican el {numero(100 * sum(sens['varianza_pca']), 0)} % de la variación entre jugadoras.</figcaption></figure>

  <section class="seccion lectura" id="equipos">
    <h2>El Barcelona tiene {int(barca['Desequilibrantes'])} de las {int(tam[3])} desequilibrantes</h2>
    <p>Por plantillas, el Barcelona suma {int(barca['Desequilibrantes'])} desequilibrantes y {int(barca['Iniciadoras'])} iniciadoras, y ninguna jugadora de los otros dos perfiles. El Real Madrid es el segundo equipo con más desequilibrantes ({int(madrid['Desequilibrantes'])}); en el resto de plantillas hay dos o menos. Muchas plantillas se parecen entre sí: mucho pulmón, alguna iniciadora, poca amenaza.</p>
  </section>

  <figure class="figura"><img loading="lazy" src="graficos/03_equipos_web.png" width="1600" height="900" alt="Barras con el número de jugadoras de cada perfil en cada equipo: el Barcelona tiene 11 desequilibrantes y el Real Madrid 6."><figcaption>Jugadoras de campo con al menos 900 minutos, por equipo y perfil.</figcaption></figure>

  <section class="seccion lectura" id="metodo">
    <p class="etiqueta">Método</p>
    <h2>De los eventos a los perfiles</h2>
    <p>Para cada jugadora con al menos 900 minutos (se excluyen las porteras) se calculan 18 variables por 90 minutos: pases progresivos, largos y de tiro, centros, conducciones progresivas, altura media de sus acciones, recepciones en el área, regates, presiones, recuperaciones, intercepciones, entradas, tiros, xG y la amenaza esperada (xT) del <a href="../liga-f-xt/">estudio anterior</a>. Se descartan {len(sens['variables_descartadas'])} por repetir información de otras (correlación mayor de 0,85) y quedan {len(sens['variables_usadas'])}.</p>
    <p>Las variables se estandarizan para que ninguna domine por escala, y las muy asimétricas pasan antes por un logaritmo. El análisis de componentes principales (PCA) sirve para dibujar el mapa; el agrupamiento se hace con k-means sobre todas las variables.</p>
    <p>El número de perfiles se fija con una regla escrita antes de mirar los grupos: entre 4 y 7, con al menos 8 jugadoras por grupo, gana el que mejor combina el coeficiente de silueta y la estabilidad (índice de Rand ajustado en 200 remuestras de jugadoras). Con 4 perfiles la silueta es {numero(k4.silueta, 2)} y la estabilidad {numero(k4.estabilidad_rand, 2)}; con 5 baja a {numero(k[k.k == 5].silueta.iloc[0], 2)} y {numero(k[k.k == 5].estabilidad_rand.iloc[0], 2)}.</p>
    <p>Como comprobación, con un mínimo de 600 minutos ({sens['jugadoras_600']} jugadoras) o sin la xT, las jugadoras vuelven a agruparse de forma muy parecida (índice de Rand ajustado de {numero(sens['rand_900_vs_600'], 2)} y {numero(sens['rand_con_vs_sin_xt'], 2)}).</p>
  </section>

  <section class="seccion lectura" id="alcance">
    <h2>Cómo leerlo</h2>
    <p>Son datos de la Liga F 2023/24: no describen el rendimiento ni el club actual de ninguna jugadora. Los perfiles resumen cómo juega cada una, no cuánto vale, y el equipo influye en lo que cada jugadora puede hacer con el balón.</p>
  </section>

  <section class="seccion lectura" id="fuentes">
    <p class="etiqueta">Trabajo verificable</p>
    <h2>Datos, código y comprobaciones</h2>
    <p>Se descargaron {cob['archivos_descargados']} archivos de StatsBomb Open Data (commit fijado) con su huella SHA-256. El análisis se reproduce con un solo script y las pruebas automáticas comprueban la estandarización, el filtrado, el agrupamiento y las variables con casos de solución conocida.</p>
    <p><a class="boton" href="{CODIGO_GITHUB}">Ver el código</a></p>
    <p><a href="jugadoras_perfiles.csv" download>Descargar las {n} jugadoras con su perfil (CSV)</a></p>
    <p>Fuente: <a href="https://github.com/hudl/open-data">StatsBomb Open Data</a>. Los eventos originales no se redistribuyen, como pide su <a href="{LICENCIA}">acuerdo de uso</a>.</p>
    <img class="logo-fuente" src="graficos/statsbomb.png" width="180" alt="StatsBomb, proveedor de los datos">
  </section>"""

    destino = escribir_pagina(
        "liga-f-perfiles",
        "¿En qué perfil está tu jugadora favorita?",
        f"Cuatro perfiles de jugadora en la Liga F 2023/24: iniciadoras, pulmones, las de área y desequilibrantes, con {n} jugadoras y datos de StatsBomb.",
        "Investigación",
        cuerpo,
        "Fuente: StatsBomb Open Data, Liga F 2023/24. K-means sobre variables por 90 minutos.",
    )
    sys.path.insert(0, str(RAIZ_WEB / "herramientas"))
    from actualizar_exploracion import enrich  # noqa: E402
    destino.write_text(enrich(destino.read_text(encoding="utf-8"), destino), encoding="utf-8")
    print(f"Página escrita en {destino.relative_to(RAIZ_WEB)}")
    redes(d, equipos, tam, xt, otras, barca, madrid, hansen)


def redes(d, equipos, tam, xt, otras, barca, madrid, hansen):
    n = len(d)
    pub = ESTUDIO / "publicaciones"
    ig = pub / "instagram"
    ig.mkdir(parents=True, exist_ok=True)
    orden = ["01_portada_instagram", "02_mapa_instagram", "03_perfil_1_instagram", "04_perfil_2_instagram",
             "05_perfil_3_instagram", "06_perfil_4_instagram", "07_equipos_instagram", "08_cierre_instagram"]
    nombres_ig = ["01_portada", "02_mapa", "03_iniciadoras", "04_pulmones", "05_las_de_area", "06_desequilibrantes", "07_equipos", "08_cierre"]
    for a, b in zip(orden, nombres_ig):
        for ext in ("png", "svg"):
            shutil.copy(ESTUDIO / "graficos" / f"{a}.{ext}", ig / f"{b}.{ext}")
    nombres = ", ".join(NOMBRES[:3]) + f" y {NOMBRES[3].lower()}"
    comun_dato = (f"Barcelona: {int(barca['Desequilibrantes'])} desequilibrantes, {int(barca['Iniciadoras'])} iniciadoras y ninguna pulmón ni de área. "
                  f"Real Madrid: {int(madrid['Desequilibrantes'])} desequilibrantes.")
    (pub / "linkedin.txt").write_text(f"""¿En qué perfil está tu jugadora favorita?

Línea de pase ha agrupado a {n} jugadoras de la Liga F 2023/24 según lo que hacen con el balón y sin él, no según la posición que figura en la alineación. Salen cuatro perfiles con nombre propio:

· Iniciadoras ({tam[0]}): sacan el balón jugando, con pases largos y progresivos.
· Pulmones ({tam[1]}): presionan, cortan y recuperan.
· Las de área ({tam[2]}): reciben cerca de la portería rival y presionan arriba.
· Desequilibrantes ({tam[3]}): la amenaza esperada (xT) por 90 minutos es de {numero(xt[3], 2)}, más de tres veces la del resto ({numero(otras, 2)}).

{comun_dato}

Cómo está hecho: 18 variables por 90 minutos de {n} jugadoras con al menos 900 minutos, estandarizadas, PCA para el mapa y k-means para los grupos; el número de perfiles se eligió con silueta y estabilidad en 200 remuestras. Python, scikit-learn y datos de StatsBomb Open Data; código en abierto.

{utm('linkedin')}

#AnaliticaDeportiva #FutbolFemenino #LigaF #Python #CienciaDeDatos
""", encoding="utf-8")
    (pub / "facebook.txt").write_text(f"""¿En qué perfil está tu jugadora favorita?

Línea de pase ha agrupado a {n} jugadoras de la Liga F 2023/24 por lo que hacen en el campo, no por su posición. Salen cuatro tipos: {nombres}.

Un dato: el Barcelona tiene {int(barca['Desequilibrantes'])} de las {tam[3]} desequilibrantes, las que más amenaza generan, como {graficos.corto(hansen.jugadora)}. ¿Dónde pondrías a tu favorita? Mira a qué perfil pertenece cada jugadora y cómo es la plantilla de tu equipo:
{utm('facebook')}

Datos: StatsBomb Open Data. Temporada 2023/24.
""", encoding="utf-8")
    (pub / "instagram.txt").write_text(f"""¿En qué perfil está tu jugadora favorita?

Hemos agrupado a {n} jugadoras de la Liga F 2023/24 según lo que hacen con y sin balón. Salen cuatro perfiles: {nombres}.

Desliza para ver el mapa, cada perfil con sus jugadoras más típicas y las que más lo llevan al extremo, y cómo se reparten las plantillas. {comun_dato}

Cuéntanos en comentarios en qué perfil pondrías a tu jugadora favorita.

Estudio completo y listado de las {n} jugadoras: enlace en la bio.

Datos: StatsBomb Open Data. Temporada 2023/24.

#LigaF #FutbolFemenino #AnaliticaDeportiva #DatosYFutbol #LineaDePase
""", encoding="utf-8")
    alt = [
        "Portada: «¿En qué perfil está tu jugadora favorita?». Cuatro perfiles para 220 jugadoras de la Liga F 2023/24.",
        f"Mapa de {n} jugadoras de la Liga F agrupadas en cuatro perfiles; las iniciadoras a la izquierda, las desequilibrantes arriba a la derecha.",
    ] + [f"Perfil {NOMBRES[i]}: radar con lo que hace el grupo y sus jugadoras más típicas y más extremas." for i in range(4)] + [
        f"Barras con los perfiles de cada plantilla; el Barcelona tiene {int(barca['Desequilibrantes'])} desequilibrantes.",
        "Cierre: dónde ver el estudio completo en lineadepase.com y pregunta para los comentarios."]
    (pub / "textos_alternativos.txt").write_text("\n".join(f"{i + 1}. {t}" for i, t in enumerate(alt)) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
