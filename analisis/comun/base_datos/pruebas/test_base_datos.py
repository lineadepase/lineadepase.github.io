"""
Pruebas de la base de datos única.

Ejecutar:  python -m pytest analisis/comun/base_datos/pruebas
"""
import csv
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cargar  # noqa: E402
import comprobar  # noqa: E402
from manifiesto import TABLAS, descubrir, esquema_de  # noqa: E402


@pytest.fixture(scope="module")
def bd(tmp_path_factory):
    """Base real construida en una carpeta temporal (no toca la de trabajo)."""
    ruta = tmp_path_factory.mktemp("bd") / "prueba.duckdb"
    cargar.construir(ruta)
    return ruta


def filas_csv(ruta: Path) -> int:
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        return sum(1 for _ in csv.reader(f)) - 1  # sin la cabecera


def test_todas_las_tablas_estan_documentadas():
    assert set(descubrir()) == set(TABLAS)


def test_cada_csv_tiene_su_tabla_con_las_mismas_filas(bd):
    con = duckdb.connect(str(bd), read_only=True)
    for (proyecto, tabla), ruta in descubrir().items():
        n = con.execute(f'SELECT count(*) FROM "{esquema_de(proyecto)}"."{tabla}"').fetchone()[0]
        assert n == filas_csv(ruta), f"{proyecto}.{tabla}"


def test_el_catalogo_coincide_con_las_tablas(bd):
    con = duckdb.connect(str(bd), read_only=True)
    assert con.execute("SELECT count(*) FROM meta.tablas").fetchone()[0] == len(TABLAS)
    sin_desc = con.execute("SELECT count(*) FROM meta.tablas WHERE descripcion = ''").fetchone()[0]
    assert sin_desc == 0


def test_la_vista_entre_proyectos_devuelve_20_equipos(bd):
    con = duckdb.connect(str(bd), read_only=True)
    assert con.execute("SELECT count(*) FROM comun.v_grupo2_actual").fetchone()[0] == 20


def test_las_comprobaciones_pasan_con_los_datos_actuales(bd):
    errores = [r for r in comprobar.ejecutar(bd) if r[0] == "error" and r[2]]
    assert errores == []


def test_la_carga_es_reproducible(tmp_path):
    """Dos cargas seguidas dan exactamente el mismo contenido (mismas huellas)."""
    a, b = tmp_path / "a.duckdb", tmp_path / "b.duckdb"
    cargar.construir(a)
    cargar.construir(b)
    consulta = "SELECT esquema, tabla, filas, columnas, sha256 FROM meta.tablas ORDER BY 1, 2"
    ra = duckdb.connect(str(a), read_only=True).execute(consulta).fetchall()
    rb = duckdb.connect(str(b), read_only=True).execute(consulta).fetchall()
    assert ra == rb and len(ra) == len(TABLAS)


def test_detecta_clave_duplicada(tmp_path):
    ruta = tmp_path / "x.duckdb"
    cargar.construir(ruta)
    con = duckdb.connect(str(ruta))
    con.execute("INSERT INTO real_zaragoza.partidos_liga SELECT * FROM real_zaragoza.partidos_liga LIMIT 1")
    con.close()
    malos = [r for r in comprobar.ejecutar(ruta) if r[0] == "error" and r[2]]
    assert any("partidos_liga" in nombre and "duplicada" in nombre for _, nombre, _ in malos)


def test_detecta_partido_huerfano(tmp_path):
    ruta = tmp_path / "x.duckdb"
    cargar.construir(ruta)
    con = duckdb.connect(str(ruta))
    con.execute("UPDATE real_zaragoza.goles SET partido_id = 9999 WHERE rowid IN (SELECT rowid FROM real_zaragoza.goles LIMIT 1)")
    con.close()
    malos = [r for r in comprobar.ejecutar(ruta) if r[0] == "error" and r[2]]
    assert any("goles.partido_id" in nombre for _, nombre, _ in malos)


def test_detecta_distribucion_que_no_suma_uno(tmp_path):
    ruta = tmp_path / "x.duckdb"
    cargar.construir(ruta)
    con = duckdb.connect(str(ruta))
    con.execute('UPDATE grupo2_simulacion.distribucion_puestos SET "1" = "1" + 0.5 WHERE equipo = (SELECT min(equipo) FROM grupo2_simulacion.distribucion_puestos)')
    con.close()
    malos = [r for r in comprobar.ejecutar(ruta) if r[0] == "error" and r[2]]
    assert any("distribucion_puestos" in nombre for _, nombre, _ in malos)
