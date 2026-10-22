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


    def test_calendario_ida_vuelta_sin_duplicados(self):
        nombres = ["A", "B", "C", "D"]
        jornadas = engine.generar_calendario_nombres(nombres)
        self.assertEqual(len(jornadas), 6)
        encuentros = [partido for jornada in jornadas for partido in jornada]
        self.assertEqual(len(encuentros), 12)
        self.assertEqual(len(set(encuentros)), 12)
        for jornada in jornadas:
            self.assertEqual(len(jornada), 2)
            self.assertEqual(set(x for partido in jornada for x in partido), set(nombres))

    def test_simulacion_actualiza_estadisticas_y_puntos(self):
        random.seed(42)
        local = engine.Equipo("Local")
        visitante = engine.Equipo("Visitante")
        engine.crear_plantilla_base(local)
        engine.crear_plantilla_base(visitante)
        local.convocar_once_automatico()
        visitante.convocar_once_automatico()
        engine.simular_partido(local, visitante, mostrar_detalle=False)
        self.assertEqual(local.partidos_jugados, 1)
        self.assertEqual(visitante.partidos_jugados, 1)
        self.assertEqual(local.goles_a_favor, visitante.goles_en_contra)
        self.assertEqual(visitante.goles_a_favor, local.goles_en_contra)
        self.assertIn((local.puntos, visitante.puntos), [(3, 0), (0, 3), (1, 1)])
        self.assertEqual(local.xg_favor, visitante.xg_contra)
        self.assertEqual(visitante.xg_favor, local.xg_contra)

    def test_guardado_y_carga_partida(self):
        import tempfile
        random.seed(42)
        club = engine.Equipo("Equipo prueba")
        engine.crear_plantilla_base(club)
        club.convocar_once_automatico()
        mercado = [engine.Jugador("Fichaje", "DEL", 77)]
        calendario = engine.generar_calendario_nombres(["Equipo prueba", "Rival"])
        with tempfile.TemporaryDirectory() as temp:
            ruta = str(Path(temp) / "partida.json")
            engine.guardar_partida(ruta, 2, 1, [club], mercado, calendario)
            temporada, jornada, equipos, cargado_mercado, cargado_calendario = engine.cargar_partida(ruta)
        self.assertEqual((temporada, jornada), (2, 1))
        self.assertEqual(equipos[0].nombre, club.nombre)
        self.assertEqual(cargado_mercado[0].nombre, "Fichaje")
        self.assertEqual(cargado_calendario, calendario)



if __name__ == "__main__":
    unittest.main()
