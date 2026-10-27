"""Regresiones del ciclo de publicación: portada, archivo e imágenes."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from previas import guardar, publicar_liga, sincronizar


class PublicacionPrevias(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for folder in ('datos', 'assets', 'proyectos/real-zaragoza'):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        guardar(self.root/'index.html', '<head></head><main><section class="actualidad-editorial actualidad-compacta">Último análisis</section></main>')
        guardar(self.root/'sitemap.xml', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"/>')
        self.entries = []
        self.add_entry(10)

    def tearDown(self):
        self.temp.cleanup()

    def add_entry(self, jornada):
        image = f'assets/j{jornada}.webp'
        (self.root/image).write_bytes(b'image-fixture')
        self.entries.append({'jornada':jornada,'pagina':f'proyectos/real-zaragoza/previa-jornada-{jornada}.html',
                             'fecha_partido':f'2026-11-{jornada:02}', 'imagen':image,'ancho':1200,'alto':675,
                             'alt':f'Rival {jornada}','titulo':f'Previa {jornada}','etiqueta':'Liga','resumen':'Contexto'})
        guardar(self.root/'datos/previas.json', json.dumps(self.entries))

    def publish(self, jornada):
        html = f'<head><link rel="canonical" href="https://lineadepase.com/proyectos/real-zaragoza/previa.html"></head><main><section class="cab-proyecto"><h1>Rival {jornada}</h1></section><p>Datos {jornada}</p></main>'
        result = publicar_liga(jornada, html, self.root)
        guardar(self.root/'proyectos/real-zaragoza/previa.html', result)
        sincronizar(self.root)

    def test_siguiente_jornada_conserva_archivo_y_cambia_imagen(self):
        self.publish(10)
        old = (self.root/self.entries[0]['pagina']).read_text(encoding='utf-8')
        self.entries = json.loads((self.root/'datos/previas.json').read_text(encoding='utf-8'))
        self.add_entry(11)
        self.publish(11)
        self.assertEqual(old, (self.root/self.entries[0]['pagina']).read_text(encoding='utf-8'))
        current = (self.root/'proyectos/real-zaragoza/previa.html').read_text(encoding='utf-8')
        self.assertIn('j11.webp',current)
        self.assertNotIn('j10.webp',current)
        home = (self.root/'index.html').read_text(encoding='utf-8')
        self.assertIn('previa-jornada-10.html',home)
        self.assertIn('previa-jornada-11.html',home)

    def test_regenerar_portada_no_duplica_y_preserva_noticia(self):
        self.publish(10)
        sincronizar(self.root)
        home = (self.root/'index.html').read_text(encoding='utf-8')
        self.assertEqual(home.count('id="titulo-previas"'),1)
        self.assertIn('Último análisis',home)
        current = (self.root/'proyectos/real-zaragoza/previa.html').read_text(encoding='utf-8')
        self.assertEqual(current.count('<!-- imagen-previa -->'),1)
        self.assertIn('Datos 10',current)

    def test_sin_imagen_no_publica(self):
        (self.root/'assets/j10.webp').unlink()
        before = (self.root/'index.html').read_bytes()
        with self.assertRaisesRegex(ValueError,'Falta la imagen'):
            self.publish(10)
        self.assertEqual(before,(self.root/'index.html').read_bytes())
        self.assertFalse((self.root/self.entries[0]['pagina']).exists())


if __name__ == '__main__':
    unittest.main()
