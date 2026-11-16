"""
Comprobaciones de integridad de la base de datos.

Uso:  python analisis/comun/base_datos/comprobar.py
Devuelve código de salida 1 si alguna comprobación de nivel «error» falla.

Cada comprobación es una consulta SQL que devuelve las filas QUE FALLAN:
si no devuelve ninguna, pasa.
"""
import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import RELACIONES, RUTA_BD, TABLAS, descubrir, esquema_de  # noqa: E402


def comprobaciones(con):
    """Genera tuplas (nivel, nombre, sql_de_filas_que_fallan)."""
    # 1. Cada CSV descubierto está documentado y viceversa.
    encontrados = set(descubrir())
    for clave in sorted(encontrados - set(TABLAS)):
        yield "error", f"tabla sin documentar: {clave}", "SELECT 1"
    for clave in sorted(set(TABLAS) - encontrados):
        yield "error", f"documentada pero sin CSV: {clave}", "SELECT 1"

    # 2. Ninguna tabla vacía y la clave natural es única y sin nulos.
    for (proyecto, tabla), info in TABLAS.items():
        t = f'"{esquema_de(proyecto)}"."{tabla}"'
        yield "error", f"{proyecto}.{tabla}: tabla vacía", f"SELECT 1 WHERE (SELECT count(*) FROM {t}) = 0"
        clave = info["clave"]
        if clave:
            cols = ", ".join(f'"{c}"' for c in clave)
            nulos = " OR ".join(f'"{c}" IS NULL' for c in clave)
            yield "error", f"{proyecto}.{tabla}: clave con nulos ({cols})", f"SELECT * FROM {t} WHERE {nulos}"
            yield "error", f"{proyecto}.{tabla}: clave duplicada ({cols})", \
                f"SELECT {cols}, count(*) n FROM {t} GROUP BY {cols} HAVING n > 1"

    # 3. Integridad referencial entre tablas (e incluso entre proyectos).
    for (p, t, c), destinos in RELACIONES:
        origen = f'"{esquema_de(p)}"."{t}"'
        union = " UNION ".join(f'SELECT "{dc}" AS v FROM "{esquema_de(dp)}"."{dt}"' for dp, dt, dc in destinos)
        yield "error", f"{p}.{t}.{c} sin correspondencia", \
            f'SELECT DISTINCT "{c}" FROM {origen} WHERE "{c}" IS NOT NULL AND "{c}" NOT IN ({union})'

    # 4. Cuadres numéricos que detectan CSV desfasados entre sí.
    # Mismos equipos en la simulación y en la clasificación (en ambos sentidos).
    yield "error", "simulación y clasificación no tienen los mismos equipos", """
        SELECT equipo FROM (
          (SELECT equipo FROM grupo2_simulacion.probabilidades
             EXCEPT SELECT equipo FROM real_zaragoza.clasificacion)
          UNION ALL
          (SELECT equipo FROM real_zaragoza.clasificacion
             WHERE tras_jornada = (SELECT max(tras_jornada) FROM real_zaragoza.clasificacion)
             EXCEPT SELECT equipo FROM grupo2_simulacion.probabilidades))"""
    # Cada fila de distribucion_puestos es una distribución: suma ~1.
    yield "error", "distribucion_puestos: una fila no suma 1", """
        SELECT equipo FROM grupo2_simulacion.distribucion_puestos
        WHERE abs(list_sum([ "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20" ]) - 1) > 0.01"""
    # Ascenso directo + play-off + descenso no puede pasar de 1.
    yield "error", "probabilidades: ascenso + play-off + descenso > 1", """
        SELECT equipo FROM grupo2_simulacion.probabilidades
        WHERE ascenso_directo + playoff + descenso > 1.0001"""
    # Los goles listados deben coincidir con el marcador de cada partido de liga.
    yield "aviso", "goles listados distintos del marcador (partido_id)", """
        SELECT p.partido_id, p.goles_favor, p.goles_contra,
               count(*) FILTER (WHERE g.sentido='Favor') gf_lista,
               count(*) FILTER (WHERE g.sentido='Contra') gc_lista
        FROM real_zaragoza.partidos_liga p LEFT JOIN real_zaragoza.goles g USING (partido_id)
        GROUP BY ALL
        HAVING gf_lista <> p.goles_favor OR gc_lista <> p.goles_contra"""
    # Los pases de la red por partido cuadran con la suma de sus conexiones.
    yield "aviso", "espana: pases_red distinto de la suma de conexiones", """
        SELECT p.partido_id, p.pases_red, sum(c.pases) suma
        FROM espana_eurocopa_redes.partidos p JOIN espana_eurocopa_redes.conexiones c USING (partido_id)
        GROUP BY ALL HAVING p.pases_red <> sum(c.pases)"""


def ejecutar(ruta_bd=RUTA_BD):
    """Corre todas las comprobaciones. Devuelve lista de (nivel, nombre, n_filas_que_fallan)."""
    con = duckdb.connect(str(ruta_bd), read_only=True)
    resultados = []
    for nivel, nombre, sql in comprobaciones(con):
        fallos = len(con.execute(sql).fetchall())
        resultados.append((nivel, nombre, fallos))
    con.close()
    return resultados


if __name__ == "__main__":
    res = ejecutar()
    errores = [r for r in res if r[0] == "error" and r[2]]
    avisos = [r for r in res if r[0] == "aviso" and r[2]]
    for nivel, nombre, n in errores + avisos:
        print(f"[{nivel.upper()}] {nombre}: {n} fila(s)")
    print(f"{len(res)} comprobaciones, {len(errores)} errores, {len(avisos)} avisos")
    sys.exit(1 if errores else 0)
