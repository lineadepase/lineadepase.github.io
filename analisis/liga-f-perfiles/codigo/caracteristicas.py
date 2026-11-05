"""Variables por jugadora y partido a partir de los eventos de StatsBomb.

Cada contador sale de un tipo de evento concreto y se suma por partido; la
conversión a «por 90 minutos» se hace en perfiles.py con los minutos
reconstruidos en datos.py.
"""
from collections import Counter, defaultdict
import math

import pandas as pd

PORTERIA = (120.0, 40.0)
EXITO_INTERCEPCION = {'Won', 'Success', 'Success In Play', 'Success Out'}
EXITO_DUELO = {'Won', 'Success', 'Success In Play', 'Success Out'}
SAQUES = {'Kick Off', 'Throw-in', 'Goal Kick', 'Corner', 'Free Kick'}
GRUPOS_POSICION = {
    'Goalkeeper': 'Portera',
    'Center Back': 'Central', 'Left Center Back': 'Central', 'Right Center Back': 'Central',
    'Left Back': 'Lateral', 'Right Back': 'Lateral', 'Left Wing Back': 'Lateral', 'Right Wing Back': 'Lateral',
    'Center Defensive Midfield': 'Pivote', 'Left Defensive Midfield': 'Pivote', 'Right Defensive Midfield': 'Pivote',
    'Center Midfield': 'Mediocentro', 'Left Center Midfield': 'Mediocentro', 'Right Center Midfield': 'Mediocentro',
    'Center Attacking Midfield': 'Mediapunta', 'Left Attacking Midfield': 'Mediapunta',
    'Right Attacking Midfield': 'Mediapunta', 'Secondary Striker': 'Delantera',
    'Left Midfield': 'Extremo', 'Right Midfield': 'Extremo', 'Left Wing': 'Extremo', 'Right Wing': 'Extremo',
    'Center Forward': 'Delantera', 'Left Center Forward': 'Delantera', 'Right Center Forward': 'Delantera',
}


def distancia(p):
    return math.hypot(PORTERIA[0] - p[0], PORTERIA[1] - p[1])


def en_area_rival(p):
    return p[0] >= 102 and 18 <= p[1] <= 62


def extraer(partidos, archivos):
    """Devuelve (contadores por jugadora y partido, posiciones por jugadora)."""
    filas, posiciones = [], defaultdict(Counter)
    for partido in partidos:
        mid = partido['match_id']
        cont = defaultdict(Counter)
        for e in archivos[f'data/events/{mid}.json']:
            if e['period'] not in (1, 2) or 'player' not in e:
                continue
            pid, tipo, c = e['player']['id'], e['type']['name'], None
            c = cont[pid]
            if 'position' in e:
                posiciones[pid][e['position']['name']] += 1
            loc = e.get('location')
            sobre_balon = False
            if tipo == 'Pass':
                p = e['pass']
                if p.get('type', {}).get('name') in SAQUES:
                    continue
                sobre_balon = True
                c['pases'] += 1
                ok = 'outcome' not in p
                c['pases_ok'] += ok
                fin = p['end_location']
                if ok and distancia(loc) - distancia(fin) >= 10 and fin[0] >= 40:
                    c['pases_prog'] += 1
                if p.get('length', 0) >= 30:
                    c['pases_largos'] += 1
                if p.get('cross'):
                    c['centros'] += 1
                if p.get('shot_assist') or p.get('goal_assist'):
                    c['pases_clave'] += 1
            elif tipo == 'Carry':
                sobre_balon = True
                if distancia(loc) - distancia(e['carry']['end_location']) >= 5:
                    c['cond_prog'] += 1
            elif tipo == 'Shot':
                sobre_balon = True
                if e['shot'].get('type', {}).get('name') != 'Penalty':
                    c['tiros'] += 1
                    c['xg'] += e['shot'].get('statsbomb_xg', 0.0)
                    c['tiros_area'] += en_area_rival(loc)
            elif tipo == 'Dribble':
                sobre_balon = True
                c['regates_int'] += 1
                c['regates'] += e['dribble']['outcome']['name'] == 'Complete'
            elif tipo == 'Ball Receipt*':
                if 'ball_receipt' not in e:
                    sobre_balon = True
                    c['recepciones_area'] += en_area_rival(loc)
            elif tipo == 'Pressure':
                c['presiones'] += 1
                c['presiones_rival'] += loc[0] >= 60
            elif tipo == 'Ball Recovery':
                if not e.get('ball_recovery', {}).get('recovery_failure'):
                    c['recuperaciones'] += 1
            elif tipo == 'Interception':
                c['intercepciones'] += e['interception']['outcome']['name'] in EXITO_INTERCEPCION
            elif tipo == 'Duel':
                d = e['duel']
                if d.get('type', {}).get('name') == 'Tackle':
                    c['entradas'] += d['outcome']['name'] in EXITO_DUELO
            if sobre_balon and loc:
                c['x_suma'] += loc[0]
                c['x_n'] += 1
        for pid, c in cont.items():
            filas.append({'partido_id': mid, 'jugadora_id': pid, **c})
    return pd.DataFrame(filas).fillna(0), posiciones


def posicion_principal(contador):
    grupos = Counter()
    for nombre, n in contador.items():
        grupos[GRUPOS_POSICION.get(nombre, 'Otra')] += n
    return grupos.most_common(1)[0][0]
