"""Protege el corte temporal y las salidas del prototipo sin tocar el sitio."""
import importlib.util
from pathlib import Path
import unittest
import sys
import json
from tempfile import TemporaryDirectory
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import linea2_experiencias as experiences

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

class StudioTests(unittest.TestCase):
    def test_opciones_del_taller_y_pareja_inicial(self):
        archive = '<select id="comparar-jornada-a"><option value="2026/27|13">J13 · A &amp; B</option><option value="2026/27|12">J12</option></select><select id="otro"><option value="incorrecto">Ignorar</option></select>'
        html = module.studio(archive)
        self.assertIn('name="jornada_a"', html)
        self.assertIn('name="jornada_b"', html)
        self.assertIn('value="2026/27|13" selected', html)
        self.assertIn('value="2026/27|12" selected', html)
        self.assertIn('A &amp; B', html)
        self.assertNotIn('incorrecto', html)
        self.assertIn('method="get"', html)

    def test_mapa_usa_temporadas_reales_cuando_el_selector_del_taller_esta_vacio(self):
        archive='<select id="comparar-jornada-a"><option value="2026/27|13">J13</option><option value="2025/26|12">J12</option></select><select id="temporada-mapa" data-temporada-mapa></select>'
        html=module.studio(archive)
        self.assertIn('id="studio-mapa-temporada"',html)
        self.assertIn('value="2026/27">2026/27',html)
        self.assertIn('value="2025/26">2025/26',html)
        self.assertIn('name="mapa-formato"',html)

    def test_sin_pareja_no_inventa_opciones(self):
        self.assertIn('necesita dos jornadas', module.studio('<select id="comparar-jornada-a"><option value="1">Una</option></select>'))

class PackageTests(unittest.TestCase):
    def test_explorador_solo_publica_datos_hasta_el_corte_y_omite_metricas_incompletas(self):
        data={'corte':'2026-11-21','partidos':[match(rival='</script><script>alert(1)</script>',completo=False,tiros_zaragoza=999),match('2026-12-01',rival='Futuro')]}
        html=experiences.season(data)
        payload=html.split('id="temporada-datos">',1)[1].split('</script>',1)[0]
        parsed=json.loads(payload)
        self.assertEqual(len(parsed['partidos']),1)
        self.assertIsNone(parsed['partidos'][0]['tiros_zaragoza'])
        self.assertNotIn('Futuro',html)
        self.assertNotIn('<script>alert',html)
        self.assertIn('&lt;/script&gt;',html)

    def test_identidad_de_jornada_requiere_fecha_rival_y_numero(self):
        archive='<tr data-jornada="13" data-fecha-partido="2026-11-20" data-rival="Rival &lt;A&gt;" data-comparison-id="2026/27|13"></tr><tr data-jornada="13" data-fecha-partido="2025-11-20" data-rival="Rival &lt;A&gt;" data-comparison-id="2025/26|13"></tr>'
        html=experiences.season({'corte':'2026-11-21','partidos':[match()]},archive)
        self.assertIn('data-compare-id="2026/27|13"',html)
        self.assertNotIn('2025/26|13',html)
        unmatched=experiences.season({'corte':'2026-11-21','partidos':[match(rival='Otro')]},archive)
        self.assertNotIn('data-compare-id',unmatched)

    def test_regeneracion_estable_y_sin_modificar_portada_publica(self):
        with TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'datos').mkdir()
            (root/'archivo-visual').mkdir()
            (root/'datalab-prototipo').mkdir()
            (root/'index.html').write_text('Portada conservada',encoding='utf-8')
            (root/'datos/zaragoza.json').write_text(json.dumps({'corte':'2026-11-21','partidos':[match(completo=True)]}),encoding='utf-8')
            (root/'archivo-visual/index.html').write_text('<select id="comparar-jornada-a"><option value="2026/27|13">J13</option><option value="2026/27|12">J12</option></select>',encoding='utf-8')
            with patch.object(module,'R',root),patch.object(module,'D',root/'datalab-prototipo'),patch('linea2_catalogo.load_catalogue',return_value=[]):
                module.build()
                first=(root/'datalab-prototipo/index.html').read_bytes()
                module.build()
                self.assertEqual(first,(root/'datalab-prototipo/index.html').read_bytes())
            html=first.decode('utf-8')
            self.assertIn('noindex,nofollow',html)
            self.assertIn('linea2-core.js',html)
            self.assertIn('linea2-experiencias.js',html)
            self.assertIn('titulo-explorador',html)
            self.assertEqual((root/'index.html').read_text(encoding='utf-8'),'Portada conservada')

class AreaPagesTests(unittest.TestCase):
    def test_paginas_separadas_con_sus_scripts_y_sin_indexacion(self):
        import linea2_paginas
        with TemporaryDirectory() as temp:
            root=Path(temp)
            fragments={key:f'<section id="{key}"><h2 id="titulo-{key}">{value[0]}</h2></section>' for key,value in module.sections.items()}
            fragments['zaragoza']+='<script type="application/json" id="temporada-datos">{"partidos":[]}</script>'
            linea2_paginas.build_pages(root,module.sections,fragments)
            self.assertEqual(len(list(root.rglob('index.html'))),9)
            datalab=(root/'datalab/index.html').read_text(encoding='utf-8')
            self.assertIn('linea2-lab.js',datalab)
            self.assertNotIn('linea2-reto.js',datalab)
            self.assertNotIn('linea2-temporada.js',datalab)
            self.assertIn('noindex,nofollow',datalab)
            self.assertIn('aria-current="page">DataLab',datalab)
            studio=(root/'studio/index.html').read_text(encoding='utf-8')
            self.assertIn('id="temporada-datos"',studio)
            self.assertNotIn('linea2-temporada.js',studio)
            first={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('index.html')}
            linea2_paginas.build_pages(root,module.sections,fragments)
            self.assertEqual(first,{str(p.relative_to(root)):p.read_bytes() for p in root.rglob('index.html')})

class CatalogueTests(unittest.TestCase):
    def test_catalogo_real_y_etiquetas_sin_presentar_lecturas_como_juegos(self):
        import linea2_catalogo as catalog
        resources=catalog.load_catalogue(module.R)
        self.assertEqual(len(resources),35)
        play=[r for r in resources if 'play' in r['areas']]
        self.assertEqual(len(play),7)
        self.assertEqual(next(r for r in play if r['id']=='balance')['tipo'],'Registro editorial')
        html=catalog.catalogue('media',resources)
        self.assertIn('ldp_origen=media#modelo-xg',html)
        self.assertIn('Contexto y límites',html)
        self.assertIn('liga-f-perfiles',catalog.catalogue('datalab',resources))
        self.assertIn('pendientes de investigación',catalog.catalogue('datalab',resources))

    def test_catalogo_rechaza_rutas_inexistentes_y_escapa_textos(self):
        import linea2_catalogo as catalog
        with TemporaryDirectory() as temp:
            root=Path(temp);(root/'datos').mkdir();(root/'pieza').mkdir();(root/'pieza/index.html').write_text('<h1>Una pieza</h1>',encoding='utf-8')
            item=dict(id='pieza',titulo='<Pieza>',url='pieza/',areas=['play'],tipo='Lectura',instruccion='Mira <esto>',contexto='Fuente',limite='Límite')
            file=root/'datos/linea2-catalogo.json'
            file.write_text(json.dumps(dict(version=1,recursos=[item])),encoding='utf-8')
            self.assertEqual(len(catalog.load_catalogue(root)),1)
            self.assertIn('&lt;Pieza&gt;',catalog.catalogue('play',[item]))
            for invalid in ['../fuera.html','no-existe/','https://example.com/','pieza/?parametro=1']:
                file.write_text(json.dumps(dict(version=1,recursos=[item|dict(url=invalid)])),encoding='utf-8')
                with self.subTest(url=invalid),self.assertRaises(ValueError):catalog.load_catalogue(root)

if __name__ == '__main__':
    unittest.main()
