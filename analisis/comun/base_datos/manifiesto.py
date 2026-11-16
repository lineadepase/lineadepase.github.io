"""
Manifiesto de la base de datos única de Línea de pase.

Aquí se documenta CADA tabla que entra en la base: de qué proyecto viene,
qué contiene y cuál es su clave. El cargador descubre solos los CSV de
``datos/salida/`` de cada proyecto; si aparece uno que no está descrito aquí,
las pruebas fallan (así ninguna tabla queda sin documentar).

Convenciones
------------
* Un proyecto = un esquema de DuckDB (guiones convertidos en guiones bajos).
* Una tabla = un CSV de salida. Los CSV en subcarpetas se nombran con el
  prefijo de la carpeta (``video/carril.csv`` -> ``video_carril``).
* Solo entran datos de SALIDA (los que ya publica la web). Los de entrada
  (rellenados a mano) siguen viviendo en cada proyecto.
"""
from pathlib import Path

# Carpeta ``analisis/``: dos niveles por encima de este archivo (comun/base_datos).
RAIZ_ANALISIS = Path(__file__).resolve().parents[2]
RUTA_BD = Path(__file__).resolve().parent / "salida" / "linea_de_pase.duckdb"
VERSION_ESQUEMA = "1.0"

# Proyecto (carpeta) -> descripción corta.
PROYECTOS = {
    "real-zaragoza": "Seguimiento del Real Zaragoza 2026/27 en Primera Federación (grupo 2).",
    "grupo2-simulacion": "Simulación Monte Carlo del grupo 2: probabilidades de ascenso, play-off y descenso.",
    "liga-f-xt": "Amenaza esperada (xT) de las jugadoras de la Liga F con StatsBomb Open Data.",
    "espana-eurocopa-redes": "Redes de pases de España en la Eurocopa femenina 2025.",
    "futbol-femenino": "Licencias de fútbol femenino por territorio (CSD) frente a la población (INE).",
}

# (proyecto, tabla) -> descripción y clave (columnas que identifican una fila).
# clave = [] significa que la tabla no tiene identificador natural.
TABLAS = {
    # --- Real Zaragoza -------------------------------------------------
    ("real-zaragoza", "partidos_liga"): dict(
        desc="Un partido de liga del Zaragoza con resultado, puntos, estadísticas del partido y posición del rival.",
        clave=["partido_id"]),
    ("real-zaragoza", "partidos_copa"): dict(
        desc="Partidos de Copa del Rey del Zaragoza (el identificador empieza en 101).",
        clave=["partido_id"]),
    ("real-zaragoza", "proximos"): dict(
        desc="Próximo partido del Zaragoza, con la posición del rival.", clave=["jornada", "competicion"]),
    ("real-zaragoza", "goles"): dict(
        desc="Un gol (a favor o en contra) con minuto, tramo, goleador y datos del partido.", clave=[]),
    ("real-zaragoza", "minutos_partido"): dict(
        desc="Minutos jugados por cada futbolista en cada partido.", clave=["partido_id", "jugador"]),
    ("real-zaragoza", "jugadores"): dict(
        desc="Resumen de temporada por jugador: partidos, minutos, goles y asistencias.", clave=["jugador"]),
    ("real-zaragoza", "participacion_goles"): dict(
        desc="Goles, asistencias y participaciones de cada jugador.", clave=["jugador"]),
    ("real-zaragoza", "clasificacion"): dict(
        desc="Clasificación del grupo 2 tras la última jornada, con ranking de ataque y defensa.",
        clave=["tras_jornada", "equipo"]),
    ("real-zaragoza", "resumen_sede"): dict(
        desc="Puntos, goles y porterías a cero del Zaragoza en casa y fuera.", clave=["sede"]),
    ("real-zaragoza", "grupo2_equipos"): dict(
        desc="Estadísticas avanzadas (xG, tiros, posesión) de los 20 equipos del grupo 2.", clave=["equipo"]),
    ("real-zaragoza", "grupo2_equipos_solo_sofascore"): dict(
        desc="Igual que grupo2_equipos pero solo con partidos de una fuente (control de sensibilidad).",
        clave=["equipo"]),
    ("real-zaragoza", "video_carril"): dict(
        desc="Goles por carril de la jugada (a favor y en contra), de la revisión en vídeo.", clave=["carril"]),
    ("real-zaragoza", "video_inicio"): dict(
        desc="Goles según cómo empezó la jugada (a favor y en contra).", clave=["inicio"]),
    ("real-zaragoza", "video_ultimo_pase"): dict(
        desc="Goles según el tipo del último pase (a favor y en contra).", clave=["ultimo_pase"]),
    ("real-zaragoza", "video_zona_remate"): dict(
        desc="Goles según la zona del remate (a favor y en contra).", clave=["zona_remate"]),
    ("real-zaragoza", "video_sofascore_partidos"): dict(
        desc="Métricas del rival por partido (una columna por métrica) recogidas de Sofascore.",
        clave=["partido_id"]),
    # --- Simulación del grupo 2 ---------------------------------------
    ("grupo2-simulacion", "probabilidades"): dict(
        desc="Probabilidad de ascenso directo, play-off y descenso de cada equipo, con puntos esperados.",
        clave=["equipo"]),
    ("grupo2-simulacion", "distribucion_puestos"): dict(
        desc="Probabilidad de acabar en cada puesto (columnas 1 a 20) para cada equipo.", clave=["equipo"]),
    ("grupo2-simulacion", "fuerzas_equipos"): dict(
        desc="Goles esperados a favor y en contra de cada equipo en el modelo.", clave=["equipo"]),
    ("grupo2-simulacion", "partidos_zaragoza"): dict(
        desc="Probabilidades 1X2 y goles esperados de los partidos pendientes del Zaragoza.",
        clave=["local", "visitante"]),
    ("grupo2-simulacion", "evolucion_zaragoza"): dict(
        desc="Cómo han cambiado las probabilidades del Zaragoza jornada a jornada.", clave=["jornada"]),
    # --- Liga F · xT --------------------------------------------------
    ("liga-f-xt", "jugadoras_xt"): dict(
        desc="xT neto, por 90 minutos y por 100 acciones de cada jugadora, con intervalo al 95 %.",
        clave=["jugadora_id", "equipo"]),
    ("liga-f-xt", "cobertura_validacion"): dict(
        desc="Control de calidad por partido: eventos, duplicados y coordenadas inválidas.",
        clave=["partido_id"]),
    ("liga-f-xt", "resumen_tipos"): dict(
        desc="xT total repartido por tipo de acción (pase o conducción).", clave=["tipo"]),
    ("liga-f-xt", "superficie_xt"): dict(
        desc="Matriz 8x12 de valor de amenaza por zona del campo.", clave=[]),
    # --- España · Eurocopa --------------------------------------------
    ("espana-eurocopa-redes", "partidos"): dict(
        desc="Un partido de España en la Eurocopa con las métricas de su red de pases.", clave=["partido_id"]),
    ("espana-eurocopa-redes", "jugadoras_partido"): dict(
        desc="Métricas de red de cada jugadora en cada partido (intermediación, PageRank, posición media).",
        clave=["partido_id", "jugadora"]),
    ("espana-eurocopa-redes", "jugadoras_torneo"): dict(
        desc="Medias de red de cada jugadora en todo el torneo.", clave=["jugadora"]),
    ("espana-eurocopa-redes", "conexiones"): dict(
        desc="Pases entre cada pareja pasadora-receptora en cada partido.",
        clave=["partido_id", "pasadora", "receptora"]),
    # --- Fútbol femenino ----------------------------------------------
    ("futbol-femenino", "indicadores"): dict(
        desc="Licencias por territorio, por mil mujeres y crecimiento 2023-2025.", clave=["territorio"]),
    ("futbol-femenino", "criterio_seleccion"): dict(
        desc="Territorios que cumplen el criterio de selección del análisis.", clave=["territorio"]),
}

# Vistas que cruzan proyectos (esquema ``comun``). Nombre -> (descripción, SQL).
VISTAS = {
    "v_grupo2_actual": (
        "Clasificación del grupo 2 tras la última jornada unida a la simulación (une real_zaragoza y grupo2_simulacion).",
        """
        SELECT c.posicion, c.equipo, c.pj, c.puntos, c.dg,
               p.ascenso_directo, p.playoff, p.descenso, p.puntos_medios
        FROM real_zaragoza.clasificacion c
        JOIN grupo2_simulacion.probabilidades p USING (equipo)
        WHERE c.tras_jornada = (SELECT max(tras_jornada) FROM real_zaragoza.clasificacion)
        ORDER BY c.posicion
        """),
}

# Relaciones entre tablas: (proyecto, tabla, columna) debe existir en
# (proyecto, tabla, columna). Una lista de destinos significa «en alguno de ellos».
RELACIONES = [
    (("real-zaragoza", "goles", "partido_id"),
     [("real-zaragoza", "partidos_liga", "partido_id"), ("real-zaragoza", "partidos_copa", "partido_id")]),
    (("real-zaragoza", "minutos_partido", "partido_id"),
     [("real-zaragoza", "partidos_liga", "partido_id"), ("real-zaragoza", "partidos_copa", "partido_id")]),
    (("real-zaragoza", "video_sofascore_partidos", "partido_id"),
     [("real-zaragoza", "partidos_liga", "partido_id"), ("real-zaragoza", "partidos_copa", "partido_id")]),
    (("espana-eurocopa-redes", "jugadoras_partido", "partido_id"),
     [("espana-eurocopa-redes", "partidos", "partido_id")]),
    (("espana-eurocopa-redes", "conexiones", "partido_id"),
     [("espana-eurocopa-redes", "partidos", "partido_id")]),
    (("grupo2-simulacion", "fuerzas_equipos", "equipo"),
     [("grupo2-simulacion", "probabilidades", "equipo")]),
    (("grupo2-simulacion", "distribucion_puestos", "equipo"),
     [("grupo2-simulacion", "probabilidades", "equipo")]),
    (("grupo2-simulacion", "probabilidades", "equipo"),
     [("real-zaragoza", "clasificacion", "equipo")]),
    (("real-zaragoza", "grupo2_equipos", "equipo"),
     [("real-zaragoza", "clasificacion", "equipo")]),
]


def esquema_de(proyecto: str) -> str:
    """Nombre del esquema SQL de un proyecto (guiones -> guiones bajos)."""
    return proyecto.replace("-", "_")


def descubrir():
    """Recorre ``analisis/*/datos/salida/**/*.csv`` y devuelve
    ``{(proyecto, tabla): Path}``. Es la fuente de verdad de qué se carga."""
    encontrados = {}
    for proyecto in PROYECTOS:
        base = RAIZ_ANALISIS / proyecto / "datos" / "salida"
        for csv in sorted(base.rglob("*.csv")):
            relativo = csv.relative_to(base).with_suffix("")
            tabla = "_".join(relativo.parts)
            encontrados[(proyecto, tabla)] = csv
    return encontrados
