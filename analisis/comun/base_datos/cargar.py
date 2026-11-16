"""
Construye la base de datos única (DuckDB) a partir de los CSV de salida.

Uso (desde cualquier carpeta):
    python analisis/comun/base_datos/cargar.py              # reconstruye la base
    python analisis/comun/base_datos/cargar.py --documentar # además escribe ESQUEMA.md

La base se REGENERA entera cada vez: no se edita a mano y no se sube al
repositorio. Con los mismos CSV sale siempre el mismo contenido (no se guarda
ninguna fecha), de modo que cualquiera puede reproducirla.
"""
import argparse
import hashlib
import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import (PROYECTOS, RAIZ_ANALISIS, RUTA_BD, TABLAS, VERSION_ESQUEMA,  # noqa: E402
                        VISTAS, descubrir, esquema_de)


def sha256(ruta: Path) -> str:
    """Huella del archivo: permite saber si un CSV cambió desde la última carga."""
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def cargar_tabla(con, esquema: str, tabla: str, csv: Path) -> None:
    """Crea ``esquema.tabla`` leyendo el CSV completo.

    * ``sample_size=-1`` hace que DuckDB mire TODAS las filas antes de decidir
      el tipo de cada columna (evita tipos mal deducidos).
    * El BOM inicial que dejan Excel y algunos scripts lo ignora DuckDB.
    """
    ruta = str(csv).replace("'", "''")
    con.execute(
        f'CREATE TABLE "{esquema}"."{tabla}" AS '
        f"SELECT * FROM read_csv('{ruta}', header=true, sample_size=-1)"
    )


def construir(ruta_bd: Path = RUTA_BD, solo=None) -> Path:
    """Crea la base desde cero y devuelve su ruta.

    ``solo``: lista opcional de proyectos (carpetas) a cargar; útil en pruebas.
    """
    ruta_bd = Path(ruta_bd)
    ruta_bd.parent.mkdir(parents=True, exist_ok=True)
    if ruta_bd.exists():
        ruta_bd.unlink()  # partir siempre de cero garantiza reproducibilidad

    con = duckdb.connect(str(ruta_bd))
    con.execute("CREATE SCHEMA meta")
    con.execute("CREATE SCHEMA comun")
    con.execute("""CREATE TABLE meta.proyectos (
        esquema VARCHAR PRIMARY KEY, carpeta VARCHAR, descripcion VARCHAR)""")
    con.execute("""CREATE TABLE meta.tablas (
        esquema VARCHAR, tabla VARCHAR, descripcion VARCHAR, clave VARCHAR,
        archivo VARCHAR, filas BIGINT, columnas INTEGER, sha256 VARCHAR,
        PRIMARY KEY (esquema, tabla))""")
    con.execute("""CREATE TABLE meta.columnas (
        esquema VARCHAR, tabla VARCHAR, posicion INTEGER, columna VARCHAR,
        tipo VARCHAR, PRIMARY KEY (esquema, tabla, columna))""")
    con.execute("CREATE TABLE meta.version (version_esquema VARCHAR)")
    con.execute("INSERT INTO meta.version VALUES (?)", [VERSION_ESQUEMA])

    for (proyecto, tabla), csv in descubrir().items():
        if solo and proyecto not in solo:
            continue
        esquema = esquema_de(proyecto)
        con.execute(f'CREATE SCHEMA IF NOT EXISTS "{esquema}"')
        con.execute("INSERT OR IGNORE INTO meta.proyectos VALUES (?,?,?)",
                    [esquema, proyecto, PROYECTOS[proyecto]])
        cargar_tabla(con, esquema, tabla, csv)

        info = TABLAS.get((proyecto, tabla), {})  # sin descripción -> lo avisan las pruebas
        filas = con.execute(f'SELECT count(*) FROM "{esquema}"."{tabla}"').fetchone()[0]
        cols = con.execute(
            "SELECT column_name, data_type FROM information_schema.columns "
            "WHERE table_schema=? AND table_name=? ORDER BY ordinal_position",
            [esquema, tabla]).fetchall()
        con.execute("INSERT INTO meta.tablas VALUES (?,?,?,?,?,?,?,?)", [
            esquema, tabla, info.get("desc", ""), ", ".join(info.get("clave", [])),
            csv.relative_to(RAIZ_ANALISIS).as_posix(), filas, len(cols), sha256(csv)])
        for pos, (nombre, tipo) in enumerate(cols, start=1):
            con.execute("INSERT INTO meta.columnas VALUES (?,?,?,?,?)", [esquema, tabla, pos, nombre, tipo])

    # Vistas que cruzan proyectos; solo se crean si están todos los esquemas.
    if not solo:
        for nombre, (_, sql) in VISTAS.items():
            con.execute(f"CREATE VIEW comun.{nombre} AS {sql}")
    con.close()
    return ruta_bd


def documentar(ruta_bd: Path = RUTA_BD, destino: Path = None) -> Path:
    """Escribe ``ESQUEMA.md`` con todas las tablas y columnas (se genera, no se edita)."""
    destino = destino or Path(__file__).resolve().parent / "ESQUEMA.md"
    con = duckdb.connect(str(ruta_bd), read_only=True)
    lineas = ["# Esquema de la base de datos",
              "",
              "Documento generado por `cargar.py --documentar`. No se edita a mano: "
              "cambia `manifiesto.py` y vuelve a generarlo.",
              ""]
    for esquema, carpeta, desc in con.execute(
            "SELECT esquema, carpeta, descripcion FROM meta.proyectos ORDER BY esquema").fetchall():
        lineas += [f"## `{esquema}`", "", desc, f"Origen: `analisis/{carpeta}/datos/salida/`.", ""]
        for tabla, d, clave, filas, archivo in con.execute(
                "SELECT tabla, descripcion, clave, filas, archivo FROM meta.tablas "
                "WHERE esquema=? ORDER BY tabla", [esquema]).fetchall():
            lineas += [f"### `{esquema}.{tabla}`", "",
                       f"{d} Filas: {filas}. Clave: {clave or 'sin clave natural'}. Archivo: `{archivo}`.", "",
                       "| Columna | Tipo |", "|---|---|"]
            for col, tipo in con.execute(
                    "SELECT columna, tipo FROM meta.columnas WHERE esquema=? AND tabla=? ORDER BY posicion",
                    [esquema, tabla]).fetchall():
                lineas.append(f"| `{col}` | {tipo} |")
            lineas.append("")
    lineas += ["## `comun` (vistas entre proyectos)", ""]
    for nombre, (d, _) in VISTAS.items():
        lineas.append(f"- `comun.{nombre}`: {d}")
    lineas.append("")
    con.close()
    destino.write_text("\n".join(lineas), encoding="utf-8")
    return destino


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--documentar", action="store_true", help="escribe también ESQUEMA.md")
    ap.add_argument("--bd", type=Path, default=RUTA_BD, help="ruta de la base de salida")
    args = ap.parse_args()
    ruta = construir(args.bd)
    print(f"Base creada: {ruta}")
    if args.documentar:
        print(f"Esquema: {documentar(ruta)}")
