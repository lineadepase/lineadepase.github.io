"""Protege el corte temporal y las salidas del prototipo sin tocar el sitio."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('linea2', Path(__file__).resolve().parents[1] / 'linea2.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def match(day='2026-11-20', **values):
    return dict(fecha=day, jornada=13, rival='Rival <A>', sede='Casa', goles_favor=2, goles_contra=1) | values

class SnapshotTests(unittest.TestCase):
    def render(self, matches):
        return module.snapshot({'corte': '2026-11-21', 'partidos': matches})

    def test_orden_no_cambia_ultimo_resultado(self):
        old = match('2026-11-10', jornada=12, rival='Anterior')
        self.assertEqual(self.render([old, match()]), self.render([match(), old]))
        self.assertIn('Jornada 13', self.render([match(), old]))

    def test_excluye_futuro_y_partidos_sin_marcador(self):
        result = self.render([match(), match('2026-11-25', rival='Futuro'), match('2026-11-21', rival='Pendiente', goles_favor=None)])
        self.assertNotIn('Futuro', result)
        self.assertNotIn('Pendiente', result)
        self.assertIn('Jornada 13', result)

    def test_sin_partidos_no_inventa_resultado(self):
        self.assertIn('No hay resultados', self.render([]))

    def test_rechaza_marcadores_invalidos(self):
        for score in [-1, True, 1.5, '2']:
            with self.subTest(score=score), self.assertRaises(ValueError):
                self.render([match(goles_favor=score)])

    def test_escapa_nombre_y_muestra_fecha(self):
        text = self.render([match()])
        self.assertIn('Rival &lt;A&gt;', text)
        self.assertIn('2026-11-20', text)
        self.assertIn('CORTE 2026-11-21', text)

    def test_separa_copa_de_liga(self):
        text = module.snapshot({'corte':'2026-11-21', 'partidos':[], 'copa':[match()]})
        self.assertIn('No hay resultados de liga', text)

if __name__ == '__main__':
    unittest.main()
