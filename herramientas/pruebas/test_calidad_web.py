from pathlib import Path
import sys,tempfile,unittest
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from calidad_web import metadata,imagenes

class CalidadWeb(unittest.TestCase):
    def test_conserva_imagen_editorial_y_elimina_tarjetas_contradictorias(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);Image.new('RGB',(1200,675)).save(root/'editorial.webp')
            html='<head><meta property="og:image" content="https://lineadepase.com/editorial.webp"><meta property="og:image" content="https://lineadepase.com/generica.png"><meta property="og:title" content="Artículo"><meta property="og:title" content="Otro"></head><main></main>'
            result=metadata(html,root)
            self.assertEqual(result.count('property="og:image"'),1)
            self.assertEqual(result.count('property="og:title"'),1)
            self.assertIn('name="twitter:image" content="https://lineadepase.com/editorial.webp"',result)
            self.assertNotIn('generica.png',result)
            self.assertEqual(metadata(result,root),result)

    def test_imagen_reserva_espacio_sin_cambiar_el_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'foto.png';Image.new('RGB',(1600,900)).save(source)
            original=source.read_bytes()
            result=imagenes('<img src="foto.png" alt="Descripción">',root/'index.html',root)
            self.assertIn('width="1600" height="900"',result)
            self.assertEqual(source.read_bytes(),original)
            self.assertEqual(imagenes(result,root/'index.html',root),result)

if __name__=='__main__':unittest.main()
