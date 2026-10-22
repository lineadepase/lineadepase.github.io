"""Pruebas de invariantes del motor Python. Ejecutar: python -m unittest discover -s juego_futbol/tests -v"""
import importlib.util
from pathlib import Path
import random
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ldp_football_engine", ROOT / "main.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


class TestMotor(unittest.TestCase):
    def test_ocasion_xg_acotada(self):
        random.seed(123)
        for ataque, defensa in [(20, 20), (90, 50), (30, 100)]:
            for _ in range(500):
                etiqueta, xg = engine.generar_ocasion_xg(ataque, defensa)
                self.assertTrue(etiqueta)
                self.assertGreaterEqual(xg, 0)
                self.assertLessEqual(xg, 1)

    def test_jugador_roundtrip(self):
        j = engine.Jugador("Prueba", "DEL", 75)
        restored = engine.Jugador.from_dict(j.to_dict())
        self.assertEqual(j.to_dict(), restored.to_dict())

    def test_formaciones_once(self):
        for formacion, posiciones in engine.FORMACIONES.items():
            self.assertEqual(sum(posiciones.values()), 11, formacion)


if __name__ == "__main__":
    unittest.main()
