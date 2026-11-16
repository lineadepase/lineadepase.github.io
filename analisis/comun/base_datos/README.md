# Base de datos única (DuckDB)

Reúne en un solo archivo los datos de **salida** de todos los proyectos de `analisis/`.
Es reproducible: se reconstruye entera desde los CSV y no se sube al repositorio.

## Uso

```bash
pip install -r analisis/comun/base_datos/requirements.txt
python analisis/comun/base_datos/cargar.py --documentar   # crea salida/linea_de_pase.duckdb y ESQUEMA.md
python analisis/comun/base_datos/comprobar.py             # integridad (código 1 si hay errores)
python -m pytest analisis/comun/base_datos/pruebas        # pruebas
```

## Diseño

- **Un proyecto = un esquema** (`real_zaragoza`, `grupo2_simulacion`, `liga_f_xt`, `espana_eurocopa_redes`, `futbol_femenino`).
- **Un CSV de `datos/salida/` = una tabla.** Los CSV en subcarpetas llevan su prefijo (`video/carril.csv` → `video_carril`).
- **`meta`**: catálogo (`proyectos`, `tablas`, `columnas`, `version`). Guarda filas, columnas, tipos y SHA-256 de cada CSV; no guarda fechas, así que dos cargas dan el mismo resultado.
- **`comun`**: vistas que cruzan proyectos (hoy `v_grupo2_actual`).
- Los tipos los deduce DuckDB leyendo todas las filas (`sample_size=-1`).

## Archivos

| Archivo | Qué hace |
|---|---|
| `manifiesto.py` | Documenta cada tabla (descripción y clave), las vistas y las relaciones entre tablas. |
| `cargar.py` | Descubre los CSV, crea la base y genera `ESQUEMA.md`. |
| `comprobar.py` | Claves únicas y sin nulos, relaciones entre tablas y cuadres numéricos. |
| `pruebas/` | Pruebas, incluidas las que inyectan errores para ver que se detectan. |
| `ESQUEMA.md` | Esquema completo (generado, no se edita a mano). |

## Añadir datos nuevos

1. El proyecto escribe su CSV en `datos/salida/`.
2. Se describe la tabla en `manifiesto.py` (`TABLAS`); si no, las pruebas fallan a propósito.
3. Se vuelve a ejecutar `cargar.py --documentar`.
