"""Regresiones del ciclo de publicación: portada, archivo e imágenes."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from previas import guardar, publicar_liga, sincronizar, ordenar, con_imagen, partido_iniciado


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
                             'alt':f'Rival {jornada}','titulo':f'Previa {jornada}','etiqueta':'Liga','resumen':'Contexto',
                             'hora':'21:00','estadio':'Estadio de prueba','fecha_publicacion':'2026-10-26','fecha_actualizacion':'2026-10-28'})
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
        self.assertIn('Publicada el 26/10/2026',home)
        self.assertIn('Actualizada el 28/10/2026',home)

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

    def test_proxima_cita_antes_que_una_fecha_posterior_y_archivadas(self):
        entries=[{'fecha_partido':'2026-10-31'},{'fecha_partido':'2026-10-27'},{'fecha_partido':'2026-10-23'}]
        self.assertEqual([x['fecha_partido'] for x in ordenar(entries,'2026-10-27')],['2026-10-27','2026-10-31','2026-10-23'])
        self.assertEqual([x['fecha_partido'] for x in ordenar(entries,'2026-10-28')],['2026-10-31','2026-10-27','2026-10-23'])

    def test_alias_comparte_canonica_con_la_noticia_permanente(self):
        self.publish(10)
        alias=(self.root/'proyectos/real-zaragoza/previa.html').read_text(encoding='utf-8')
        self.assertIn('rel="canonical" href="https://lineadepase.com/proyectos/real-zaragoza/previa-jornada-10.html"',alias)

    def test_ficha_compartir_y_fechas_son_homogeneos_e_idempotentes(self):
        entry={'imagen':'assets/j10.webp','ancho':1200,'alto':675,'alt':'Previa',
               'pagina':'proyectos/real-zaragoza/previa-jornada-10.html','titulo':'Zaragoza – Rival',
               'fecha_partido':'2026-10-31','fecha_publicacion':'2026-10-27','fecha_actualizacion':'2026-10-28',
               'hora':'21:00','estadio':'Ibercaja Estadio','competicion':'Primera Federación · J10'}
        raw='<head><link rel="canonical" href="https://lineadepase.com/proyectos/real-zaragoza/previa.html"><script type="application/ld+json">{"@context":"https://schema.org","@type":"Article"}</script></head><main><section class="cab-proyecto"><h1>Zaragoza – Rival</h1></section></main>'
        first=con_imagen(raw,entry)
        second=con_imagen(first,entry)
        self.assertEqual(second.count('<!-- ficha-previa -->'),1)
        self.assertEqual(second.count('<!-- compartir-previa -->'),1)
        self.assertIn('Publicado el 27/10/2026 · Revisado el 28/10/2026',second)
        self.assertIn('Ibercaja Estadio',second)
        self.assertIn('21:00 h (hora peninsular)',second)
        self.assertIn('calendario/previa-jornada-10.ics',second)
        self.assertIn('Añadir al calendario (.ics)',second)
        self.assertIn('estado-partido.js',second)
        self.assertIn('datePublished',second)
        self.assertIn('dateModified',second)
        self.assertEqual(first,second)

    def test_centro_partido_expone_solo_datos_registrados_y_fuentes(self):
        entry={'imagen':'assets/j10.webp','ancho':1200,'alto':675,'alt':'Previa',
               'pagina':'proyectos/real-zaragoza/previa-copa.html','titulo':'Tudelano – Zaragoza',
               'fecha_partido':'2026-10-27','fecha_publicacion':'2026-10-27','hora':'21:00',
               'estadio':'Ciudad de Tudela','centro_partido':{
                   'fecha_verificacion':'2026-10-27T16:09:00+01:00','fuentes':[{'nombre':'CD Tudelano oficial','url':'https://cdtudelano.com/actualidad/entradas-copa-del-rey-zaragoza/'}]}}
        raw='<head></head><main><section class="cab-proyecto"><h1>Tudelano – Zaragoza</h1></section></main>'
        first=con_imagen(raw,entry)
        second=con_imagen(first,entry)
        self.assertEqual(first,second)
        self.assertEqual(first.count('<!-- centro-partido -->'),1)
        self.assertIn('Esta ficha no ofrece marcador en directo',first)
        self.assertIn('Pendiente de actualización editorial.',first)
        self.assertIn('Pendientes de confirmación en esta ficha.',first)
        self.assertIn('https://cdtudelano.com/actualidad/entradas-copa-del-rey-zaragoza/',first)
        self.assertIn('Comprobado el 27/10/2026 a las 16:09 (hora peninsular)',first)

    def test_validador_editorial_acepta_tercera_persona_y_hasta_dos_fuentes(self):
        from previas import validar_noticia_previa
        markup='<p>El Zaragoza llega a la cita tras tres victorias.</p><a href="https://club.example/">Club</a><a href="https://liga.example/">Liga</a>'
        validar_noticia_previa(markup)

    def test_validador_editorial_rechaza_exceso_de_fuentes_y_apelaciones(self):
        from previas import validar_noticia_previa
        sources=''.join(f'<a href="https://fuente.example/{i}">Fuente</a>' for i in range(3))
        with self.assertRaisesRegex(ValueError,'máximo de dos fuentes'):
            validar_noticia_previa('<p>El encuentro en Tudela</p>'+sources)
        with self.assertRaisesRegex(ValueError,'tercera persona'):
            validar_noticia_previa('<p>Puedes seguir el partido en Tudela.</p>')

    def test_registro_exige_confirmacion_horaria_y_fuentes_antes_de_publicar_una_cronica(self):
        from datetime import datetime, timedelta
        from zoneinfo import ZoneInfo
        from previas import registro
        fixture={'pagina':'proyectos/real-zaragoza/previa-copa.html','imagen':'assets/j10.webp','fecha_partido':'2026-10-26','hora':'21:00',
                 'postpartido_url':'proyectos/real-zaragoza/cronica.html',
                 'resultado_confirmado':{'marcador':'2-1','fecha_verificacion':'2026-10-26T21:30:00+01:00',
                    'fuentes':[{'nombre':'Club','url':'https://club.example/resultado'}]}}
        (self.root/'assets/j10.webp').write_bytes(b'image-fixture')
        (self.root/'proyectos/real-zaragoza/cronica.html').write_text('<main>Crónica</main>',encoding='utf-8')
        (self.root/'assets/j10.webp').write_bytes(b'image-fixture')
        without_result=dict(fixture); without_result.pop('resultado_confirmado')
        guardar(self.root/'datos/previas.json',json.dumps([without_result]))
        with self.assertRaisesRegex(ValueError,'confirmación editorial conjunta'):
            registro(self.root)
        guardar(self.root/'datos/previas.json',json.dumps([fixture]))
        # La confirmación debe llegar después del inicio previsto.
        fixture['resultado_confirmado']['fecha_verificacion']='2026-10-26T20:59:00+01:00'
        guardar(self.root/'datos/previas.json',json.dumps([fixture]))
        with self.assertRaisesRegex(ValueError,'antes de la hora'):
            registro(self.root)
        fixture['resultado_confirmado']['fecha_verificacion']='2026-10-26T21:30:00+01:00'
        guardar(self.root/'datos/previas.json',json.dumps([fixture]))
        self.assertEqual(len(registro(self.root)),1)
        from datetime import datetime, timedelta, timezone
        future=(datetime.now(timezone.utc)+timedelta(days=1)).astimezone(ZoneInfo('Europe/Madrid'))
        fixture['resultado_confirmado']['fecha_verificacion']=future.isoformat(timespec='seconds')
        guardar(self.root/'datos/previas.json',json.dumps([fixture]))
        with self.assertRaisesRegex(ValueError,'no puede estar en el futuro'):
            registro(self.root)
        fixture.pop('resultado_confirmado')
        guardar(self.root/'datos/previas.json',json.dumps([fixture]))
        with self.assertRaisesRegex(ValueError,'confirmación editorial conjunta'):
            registro(self.root)

    def test_portada_solo_publica_marcador_y_cronica_con_confirmacion_registrada(self):
        from datetime import datetime, timedelta
        from zoneinfo import ZoneInfo
        self.publish(10)
        entry=json.loads((self.root/'datos/previas.json').read_text(encoding='utf-8'))[0]
        now=datetime.now(ZoneInfo('Europe/Madrid'))
        kickoff=now.date()-timedelta(days=1)
        entry['fecha_partido']=kickoff.isoformat()
        entry['fecha_publicacion']=kickoff.isoformat()
        entry['postpartido_url']='proyectos/real-zaragoza/cronica-j10.html'
        entry['resultado_confirmado']={'marcador':'2-1','fecha_verificacion':now.isoformat(timespec='seconds'),
            'fuentes':[{'nombre':'Real Zaragoza','url':'https://club.example/resultado'}]}
        (self.root/'proyectos/real-zaragoza/cronica-j10.html').write_text('<main>Crónica</main>',encoding='utf-8')
        guardar(self.root/'datos/previas.json',json.dumps([entry]))
        html=publicar_liga(10,'<head></head><main><section class="cab-proyecto"><h1>Rival 10</h1></section></main>',self.root)
        home=(self.root/'index.html').read_text(encoding='utf-8')
        article=(self.root/entry['pagina']).read_text(encoding='utf-8')
        self.assertIn('data-resultado-confirmado="true"',home)
        self.assertIn('data-marcador="2-1"',home)
        self.assertIn('Resultado confirmado · 2-1',home)
        self.assertIn('class="marcador-previa"',home)
        self.assertIn('Leer la crónica o el análisis',home)
        self.assertIn('Releer la previa',home)
        self.assertIn('Resultado confirmado: 2-1',article)
        self.assertIn('href="https://club.example/resultado"',article)
        self.assertIn('Real Zaragoza',article)

    def test_portada_no_da_por_disputado_un_partido_sin_confirmacion(self):
        from datetime import datetime, timedelta
        from zoneinfo import ZoneInfo
        self.publish(10)
        entries=json.loads((self.root/'datos/previas.json').read_text(encoding='utf-8'))
        entries[0]['fecha_partido']=(datetime.now(ZoneInfo('Europe/Madrid')).date()-timedelta(days=1)).isoformat()
        guardar(self.root/'datos/previas.json',json.dumps(entries))
        from previas import portada
        portada(self.root)
        home=(self.root/'index.html').read_text(encoding='utf-8')
        self.assertIn('Pendiente de confirmación editorial',home)
        self.assertNotIn('marcador-previa',home)
        self.assertNotIn('Partido disputado',home)
        self.assertNotIn('Leer la crónica o el análisis',home)

    def test_centro_partido_rechaza_mas_de_dos_fuentes_y_fechas_sin_zona(self):
        from previas import registro
        fixture={'imagen':'assets/j10.webp','pagina':'proyectos/real-zaragoza/previa-copa.html',
                 'centro_partido':{'fecha_verificacion':'2026-10-27T16:09:00+01:00',
                                   'fuentes':[{'nombre':f'Fuente {i}','url':f'https://example.com/{i}'} for i in range(3)]}}
        (self.root/'assets/j10.webp').write_bytes(b'image-fixture')
        guardar(self.root/'datos/previas.json',json.dumps([fixture]))
        with self.assertRaisesRegex(ValueError,'una o dos fuentes'):
            registro(self.root)
        fixture['centro_partido']['fuentes']=fixture['centro_partido']['fuentes'][:1]
        fixture['centro_partido']['fecha_verificacion']='2026-10-27T16:09:00'
        guardar(self.root/'datos/previas.json',json.dumps([fixture]))
        with self.assertRaisesRegex(ValueError,'zona horaria'):
            registro(self.root)

    def test_generador_ics_convierte_hora_de_madrid_a_utc_y_es_estable(self):
        from previas import calendar_event, escribir_calendario
        entry={'pagina':'proyectos/real-zaragoza/previa-copa-tudelano-20261027.html',
               'fecha_partido':'2026-10-27','fecha_publicacion':'2026-10-27','hora':'21:00',
               'titulo':'CD Tudelano – Real Zaragoza','estadio':'Estadio Ciudad de Tudela',
               'resumen':'Noche de Copa'}
        event=calendar_event(entry)
        self.assertIn('DTSTART:20261027T200000Z',event)
        self.assertIn('DTEND:20261027T223000Z',event)
        self.assertIn('SUMMARY:CD Tudelano – Real Zaragoza',event)
        self.assertIn('DESCRIPTION:Noche de Copa\\nhttps://lineadepase.com/',event)
        self.assertTrue(event.endswith('\r\n'))
        first=escribir_calendario(entry,self.root).read_bytes()
        second=escribir_calendario(entry,self.root).read_bytes()
        self.assertEqual(first,second)

    def test_indicador_de_inicio_reconoce_el_horario_local_y_el_cambio_de_hora(self):
        from datetime import datetime
        from zoneinfo import ZoneInfo
        entry={'fecha_partido':'2026-10-27','hora':'21:00'}
        before=datetime(2026,10,27,20,59,tzinfo=ZoneInfo('Europe/Madrid'))
        at=datetime(2026,10,27,21,0,tzinfo=ZoneInfo('Europe/Madrid'))
        self.assertFalse(partido_iniciado(entry,before))
        self.assertTrue(partido_iniciado(entry,at))

    def test_regenerar_crea_calendario_ics(self):
        self.publish(10)
        event=(self.root/'calendario/previa-jornada-10.ics').read_text(encoding='utf-8')
        self.assertIn('SUMMARY:Previa 10',event)
        self.assertIn('LOCATION:Estadio de prueba',event)


if __name__ == '__main__':
    unittest.main()
