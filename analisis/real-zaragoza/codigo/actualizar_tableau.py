"""Actualiza un TWBX existente conservando sus hojas y sus esquemas Hyper.

Uso: python actualizar_tableau.py plantilla.twbx salida.twbx
Requiere pandas, openpyxl y tableauhyperapi. Las fuentes son los CSV de
datos/salida. No publica en Tableau Public: produce un libro autónomo.
"""
import argparse
from datetime import datetime
from pathlib import Path
import tempfile
import zipfile
import xml.etree.ElementTree as ET

import pandas as pd
from openpyxl import load_workbook
from tableauhyperapi import Connection, HyperProcess, Inserter, Telemetry, TableName

PROYECTO = Path(__file__).resolve().parents[1]


def actualizar(plantilla, destino):
    with tempfile.TemporaryDirectory() as tmp:
        carpeta = Path(tmp)
        with zipfile.ZipFile(plantilla) as z:
            z.extractall(carpeta)
        twb = next(carpeta.glob('*.twb'))
        arbol = ET.parse(twb)
        libro_excel = next(carpeta.rglob('*.xlsx'))
        excel = load_workbook(libro_excel)
        datos = {}
        # Mantengo los nombres y el orden de columnas del libro original.
        for hoja in excel:
            columnas = [c.value for c in hoja[1]]
            tabla = pd.read_csv(PROYECTO / 'datos/salida' / (hoja.title + '.csv'))
            tabla = tabla[columnas].astype(object).where(pd.notna(tabla[columnas]), None)
            hoja.delete_rows(2, max(hoja.max_row - 1, 0))
            for fila in tabla.itertuples(index=False, name=None):
                hoja.append(fila)
            datos[hoja.title] = tabla
        excel.save(libro_excel)
        ahora = datetime.now().isoformat(sep=' ', timespec='seconds')
        resumen = {}
        # TCP es una opción oficial de Hyper; evita depender de sockets Unix.
        with HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU,
                          parameters={'use_tcp_port': 'auto', 'log_config': ''}) as hyper:
            for fuente in arbol.findall('./datasources/datasource'):
                relacion = fuente.find('./connection/relation')
                nombre = relacion.get('name')
                tabla = datos[nombre]
                extraccion = fuente.find('./extract/connection')
                ruta = carpeta / extraccion.get('dbname')
                with Connection(hyper.endpoint, ruta) as conexion:
                    definicion = conexion.catalog.get_table_definition(TableName('Extract', 'Extract'))
                    columnas = [c.name.unescaped for c in definicion.columns]
                    assert columnas == list(tabla.columns), nombre
                    filas = []
                    for original in tabla.itertuples(index=False, name=None):
                        fila = []
                        for valor, col in zip(original, definicion.columns):
                            tipo = str(col.type)
                            if valor is None:
                                fila.append(None)
                            elif tipo in ('BIG_INT', 'INT', 'SMALL_INT'):
                                # No truncar decimales silenciosamente.
                                assert float(valor).is_integer(), (nombre, col.name, valor)
                                fila.append(int(valor))
                            elif tipo == 'DOUBLE':
                                fila.append(float(valor))
                            elif tipo == 'BOOL':
                                assert isinstance(valor, bool), (nombre, valor)
                                fila.append(valor)
                            else:
                                fila.append(str(valor))
                        filas.append(fila)
                    conexion.execute_command('DELETE FROM "Extract"."Extract"')
                    with Inserter(conexion, definicion) as inserter:
                        inserter.add_rows(filas)
                        inserter.execute()
                    leidas = conexion.execute_list_query('SELECT * FROM "Extract"."Extract"')
                    # Comparación completa de cada extracción contra el CSV.
                    assert sorted(map(repr, leidas)) == sorted(map(repr, filas)), nombre
                    resumen[nombre] = len(leidas)
                extraccion.set('update-time', ahora)
                for evento in extraccion.findall('./refresh/refresh-event'):
                    evento.set('rows-inserted', str(len(tabla)))
                    evento.set('timestamp-start', ahora)
                for conexion_excel in fuente.findall("./connection/named-connections/named-connection/connection"):
                    conexion_excel.set('dbname', libro_excel.relative_to(carpeta).as_posix())
                from openpyxl.utils import get_column_letter
                rango = f'A1:{get_column_letter(len(tabla.columns))}{len(tabla)+1}'
                for nodo in fuente.findall('.//columns[@gridOrigin]'):
                    nodo.set('gridOrigin', f'{rango}:no:{rango}:0')
                for nodo in fuente.findall('.//attribute[@name="gridOrigin"]'):
                    nodo.text = f'"{rango}:no:{rango}:0"'
                for nodo in fuente.findall('.//metadata-record[@class="column"]'):
                    col = nodo.findtext('remote-name')
                    if col in tabla:
                        for contador in nodo.findall('approx-count'):
                            contador.text = str(tabla[col].nunique())
        destino = Path(destino)
        destino.parent.mkdir(parents=True, exist_ok=True)
        # Nombre de archivo interno simple, independiente del sistema operativo.
        nuevo_twb = carpeta / 'Real_Zaragoza.twb'
        arbol.write(nuevo_twb, encoding='utf-8', xml_declaration=True)
        if twb != nuevo_twb:
            twb.unlink()
        with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(carpeta.rglob('*')):
                if p.is_file():
                    z.write(p, p.relative_to(carpeta))
        assert datos['partidos_liga'].jornada.max() == 8
        assert datos['partidos_liga'].iloc[-1].puntos_acumulados == 17
        assert set(datos['clasificacion'].tras_jornada) == {8}
        print(resumen)
        print('J8, 17 puntos y contenido íntegro de las cuatro extracciones verificados.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plantilla', type=Path)
    parser.add_argument('destino', type=Path)
    args = parser.parse_args()
    actualizar(args.plantilla, args.destino)
