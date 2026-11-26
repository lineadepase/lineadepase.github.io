"""Tabla base: una fila por jugadora con sus minutos, posición y variables por 90 minutos."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

import caracteristicas
import datos
import modelo

ESTUDIO = Path(__file__).resolve().parents[1]
SALIDA = ESTUDIO / 'datos' / 'salida'

SUMAS = ['pases', 'pases_ok', 'pases_prog', 'pases_largos', 'centros', 'pases_clave', 'cond_prog', 'tiros', 'xg',
         'tiros_area', 'regates_int', 'regates', 'recepciones_area', 'presiones', 'presiones_rival',
         'recuperaciones', 'intercepciones', 'entradas', 'x_suma', 'x_n']


def construir(cache):
    partidos, archivos, manifiesto = datos.obtener_temporada(cache)
    acciones, minutos, auditoria = datos.preparar(partidos, archivos)
    cont, posiciones = caracteristicas.extraer(partidos, archivos)
    cont = cont.merge(minutos[['partido_id', 'jugadora_id']], on=['partido_id', 'jugadora_id'], how='inner')
    puntos, _ = modelo.validacion_cruzada(acciones)
    xt, _ = modelo.resumir(puntos, minutos, bootstrap=2)
    tabla = minutos.groupby('jugadora_id').agg(jugadora=('jugadora', 'first'), equipo=('equipo', 'first'),
                                               partidos=('partido_id', 'nunique'), minutos=('minutos', 'sum')).reset_index()
    # Quien cambia de equipo a mitad de temporada se asigna al equipo donde más minutos jugó.
    principal = (minutos.groupby(['jugadora_id', 'equipo']).minutos.sum().reset_index()
                 .sort_values('minutos').drop_duplicates('jugadora_id', keep='last')[['jugadora_id', 'equipo']])
    tabla = tabla.drop(columns='equipo').merge(principal, on='jugadora_id')
    suma = cont.groupby('jugadora_id')[SUMAS].sum().reset_index()
    tabla = tabla.merge(suma, on='jugadora_id', how='left').fillna(0)
    tabla = tabla.merge(xt[['jugadora_id', 'xt_neto']], on='jugadora_id', how='left')
    tabla['posicion'] = tabla.jugadora_id.map(lambda j: caracteristicas.posicion_principal(posiciones[j]) if posiciones[j] else 'Otra')
    por90 = 90 / tabla.minutos
    out = tabla[['jugadora_id', 'jugadora', 'equipo', 'posicion', 'partidos', 'minutos']].copy()
    out['minutos'] = out.minutos.round(1)
    out['pases_90'] = tabla.pases * por90
    out['pct_pases'] = 100 * tabla.pases_ok / tabla.pases.clip(lower=1)
    out['pases_prog_90'] = tabla.pases_prog * por90
    out['pases_largos_90'] = tabla.pases_largos * por90
    out['centros_90'] = tabla.centros * por90
    out['pases_clave_90'] = tabla.pases_clave * por90
    out['cond_prog_90'] = tabla.cond_prog * por90
    out['xt_neto_90'] = tabla.xt_neto * por90
    out['altura_media'] = tabla.x_suma / tabla.x_n.clip(lower=1)
    out['presiones_90'] = tabla.presiones * por90
    out['pct_presion_rival'] = 100 * tabla.presiones_rival / tabla.presiones.clip(lower=1)
    out['recuperaciones_90'] = tabla.recuperaciones * por90
    out['intercepciones_90'] = tabla.intercepciones * por90
    out['entradas_90'] = tabla.entradas * por90
    out['regates_90'] = tabla.regates * por90
    out['tiros_90'] = tabla.tiros * por90
    out['xg_90'] = tabla.xg * por90
    out['recepciones_area_90'] = tabla.recepciones_area * por90
    SALIDA.mkdir(parents=True, exist_ok=True)
    out.round(4).to_csv(SALIDA / 'jugadoras_base.csv', index=False)
    resumen = {'partidos': len(partidos), 'eventos': int(auditoria.eventos.sum()), 'acciones_xt': len(acciones),
               'jugadoras': len(out), 'archivos_descargados': len(manifiesto), 'commit_statsbomb': datos.COMMIT}
    (ESTUDIO / 'documentacion').mkdir(exist_ok=True)
    (ESTUDIO / 'documentacion' / 'manifiesto_descargas.json').write_text(json.dumps(manifiesto, indent=1), encoding='utf-8')
    (ESTUDIO / 'documentacion' / 'cobertura.json').write_text(json.dumps(resumen, indent=1), encoding='utf-8')
    return out
