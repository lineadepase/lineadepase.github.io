"""Casos de solución conocida; no dependen de descargar datos de fútbol."""
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'codigo'))
import caracteristicas as car  # noqa: E402
import perfiles as pf  # noqa: E402
from datos import minutos_eventos, reloj_minutos  # noqa: E402


def base(n=60):
    rng = np.random.default_rng(1)
    d = pd.DataFrame({'jugadora_id': range(n), 'jugadora': [f'J{i}' for i in range(n)], 'equipo': 'X',
                      'posicion': ['Portera'] * 2 + ['Central'] * (n - 2), 'partidos': 20,
                      'minutos': [1000.0] * (n - 5) + [500.0] * 5})
    for v in pf.VARIABLES:
        d[v] = rng.uniform(1, 10, n)
    d['altura_media'] = rng.uniform(30, 80, n)
    return d


class PerfilesTests(unittest.TestCase):
    def test_filtra_porteras_y_minutos(self):
        d, z, usadas, _ = pf.preparar(base())
        self.assertTrue((d.minutos >= 900).all())
        self.assertFalse((d.posicion == 'Portera').any())
        self.assertEqual(len(d), 55 - 2)  # 55 con minutos suficientes, 2 de ellas porteras

    def test_estandarizacion(self):
        _, z, _, _ = pf.preparar(base())
        np.testing.assert_allclose(z.mean(), 0, atol=1e-9)
        np.testing.assert_allclose(z.std(ddof=0), 1, atol=1e-9)

    def test_descarta_variable_redundante(self):
        d = base()
        d['pases_prog_90'] = d['xt_neto_90'] * 2 + 1  # correlación 1 con la primera variable
        _, _, usadas, descartadas = pf.preparar(d)
        self.assertIn('xt_neto_90', usadas)
        self.assertIn('pases_prog_90', descartadas)

    def test_kmeans_recupera_grupos_separados(self):
        rng = np.random.default_rng(2)
        z = pd.DataFrame(np.vstack([rng.normal(c, 0.2, (30, 4)) for c in (-5, 0, 5)]))
        verdad = np.repeat([0, 1, 2], 30)
        from sklearn.metrics import adjusted_rand_score
        m = pf.kmeans(z, 3)
        self.assertEqual(adjusted_rand_score(verdad, m.labels_), 1.0)
        self.assertGreater(pf.estabilidad(z, 3, m.labels_, remuestras=10), 0.95)

    def test_nombres_de_perfil_son_una_permutacion(self):
        c = pd.DataFrame({'xt_neto_90': [0.1, 0.2, 1.7, -0.3], 'altura_media': [-1.0, 0.0, 1.2, 1.1]})
        orden = pf.nombrar(c)
        self.assertEqual(sorted(orden.values()), [0, 1, 2, 3])
        self.assertEqual(orden[2], 3)   # mayor xT -> desequilibrantes
        self.assertEqual(orden[0], 0)   # la más atrasada de las restantes -> iniciadoras
        self.assertEqual(orden[3], 2)   # la más adelantada de las dos que quedan -> las de área

    def test_minutos_con_cambio(self):
        ev = [{'type': {'name': 'Starting XI'}, 'period': 1, 'timestamp': '00:00:00.000', 'index': 1,
               'tactics': {'lineup': [{'player': {'id': 1}}, {'player': {'id': 2}}]}},
              {'type': {'name': 'Substitution'}, 'period': 2, 'timestamp': '00:30:00.000', 'index': 2, 'player': {'id': 1},
               'substitution': {'replacement': {'id': 3}}}]
        m = minutos_eventos(ev)
        self.assertEqual((m[1], m[2], m[3]), (75.0, 90.0, 15.0))
        self.assertEqual(reloj_minutos('47:10', 1), 45.0)

    def test_pase_progresivo_y_largo(self):
        self.assertAlmostEqual(car.distancia((120, 40)), 0)
        partido = [{'match_id': 1}]
        pase = lambda ini, fin, ok=True, **extra: {
            'period': 1, 'player': {'id': 9}, 'type': {'name': 'Pass'}, 'location': ini,
            'pass': {'end_location': fin, 'length': float(np.hypot(fin[0] - ini[0], fin[1] - ini[1])),
                     **({} if ok else {'outcome': {'name': 'Incomplete'}}), **extra}, 'position': {'name': 'Center Back'}}
        eventos = [pase([30, 40], [60, 40]),                 # progresivo (30 yardas más cerca) y largo
                   pase([60, 40], [64, 40]),                 # corto, no progresivo
                   pase([30, 40], [60, 40], ok=False),       # fallado: no progresivo
                   pase([30, 40], [60, 40], cross=True)]     # cuenta además como centro
        df, _ = car.extraer(partido, {'data/events/1.json': eventos})
        fila = df.iloc[0]
        self.assertEqual((fila.pases, fila.pases_ok, fila.pases_prog, fila.pases_largos, fila.centros), (4, 3, 2, 3, 1))

    def test_posicion_principal(self):
        from collections import Counter
        self.assertEqual(car.posicion_principal(Counter({'Left Back': 5, 'Center Back': 2})), 'Lateral')
        self.assertEqual(car.posicion_principal(Counter({'Center Back': 3, 'Left Center Back': 3, 'Left Back': 5})), 'Central')


if __name__ == '__main__':
    unittest.main()
