"""Comprueba que portada, galería y exportaciones reflejan el mismo partido."""
from __future__ import annotations

from html.parser import HTMLParser
import csv
from datetime import date as date_type
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from PIL import Image
from segunda_edicion import match_statistics, percentage_text, archive_round_name, visual_season, fixture_for

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets' / 'ilustraciones'


class VisualLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.home: dict[str, str] | None = None
        self.gallery: dict[str, str] | None = None
        self.statistics: dict[str, str] | None = None
        self.home_image = ''
        self.gallery_image = ''
        self.statistics_image = ''
        self.archive_rows: list[dict[str, str]] = []
        self.archive_links: list[str] = []
        self._in_archive = False
        self._in_home = False
        self._in_gallery = False
        self._in_statistics = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or '' for key, value in attrs}
        classes = values.get('class', '').split()
        if tag == 'figure' and 'resultado-portada-visual' in classes:
            self.home = values
            self._in_home = True
        if tag == 'article' and 'tarjeta-galeria-visual' in classes and values.get('data-coleccion-visual') == 'jornada':
            self.gallery = values
            self._in_gallery = True
        if tag == 'article' and 'tarjeta-galeria-visual' in classes and values.get('data-coleccion-visual') == 'estadistica':
            self.statistics = values
            self._in_statistics = True
        if tag == 'img' and self._in_home:
            self.home_image = values.get('src', '')
        if tag == 'img' and self._in_gallery:
            self.gallery_image = values.get('src', '')
        if tag == 'img' and self._in_statistics:
            self.statistics_image = values.get('src', '')
        if tag == 'tbody':
            self._in_archive = True
        if tag == 'tr' and self._in_archive:
            self.archive_rows.append(values)
        if tag == 'a' and self._in_archive:
            self.archive_links.append(values.get('href', ''))

    def handle_endtag(self, tag: str) -> None:
        if tag == 'figure' and self._in_home:
            self._in_home = False
        if tag == 'article' and self._in_gallery:
            self._in_gallery = False
        if tag == 'article' and self._in_statistics:
            self._in_statistics = False
        if tag == 'tbody':
            self._in_archive = False


def main() -> None:
    data = json.loads((ROOT / 'datos' / 'zaragoza.json').read_text(encoding='utf-8'))
    match = max(data['partidos'], key=lambda row: int(row['jornada']))
    fixture = next((row for row in data.get('fichas', []) if str(row.get('partido_id')) == str(match.get('partido_id'))), None)
    stats = match_statistics(match, fixture)
    expected_round = str(match['jornada'])
    expected_date = match['fecha']
    months = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
    expected_display_date = f'{expected_date[8:10]} {months[int(expected_date[5:7])-1]} {expected_date[:4]}'
    home = match['rival'] if match['sede'] == 'Fuera' else 'Real Zaragoza'
    away = 'Real Zaragoza' if match['sede'] == 'Fuera' else match['rival']
    goals_home = match['goles_contra'] if match['sede'] == 'Fuera' else match['goles_favor']
    goals_away = match['goles_favor'] if match['sede'] == 'Fuera' else match['goles_contra']

    pages = VisualLinks()
    pages.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
    pages.feed((ROOT / 'galeria-visual' / 'index.html').read_text(encoding='utf-8'))
    pages.feed((ROOT / 'archivo-visual' / 'index.html').read_text(encoding='utf-8'))
    if pages.home is None or pages.gallery is None:
        raise RuntimeError('Falta la tarjeta del último partido en portada o galería.')
    for name, attrs in [('portada', pages.home), ('galería', pages.gallery)]:
        if attrs.get('data-jornada') != expected_round or attrs.get('data-fecha-partido') != expected_date:
            raise RuntimeError(f'La jornada o fecha de {name} no coincide con datos/zaragoza.json.')
    if pages.home_image != 'assets/ilustraciones/resultado-real-zaragoza-ultima-jornada.png':
        raise RuntimeError('La portada no enlaza la exportación PNG actual.')
    if pages.gallery_image != '../assets/ilustraciones/resultado-real-zaragoza-ultima-jornada.png':
        raise RuntimeError('La galería no reutiliza la misma exportación PNG que la portada.')

    svg_root = ET.parse(ART / 'resultado-real-zaragoza-ultima-jornada.svg').getroot()
    title = svg_root.findtext('{*}title') or ''
    description = svg_root.findtext('{*}desc') or ''
    expected_score = f'{goals_home}–{goals_away}'
    for value in (expected_round, expected_display_date, home, away, expected_score):
        if value not in title + ' ' + description:
            raise RuntimeError(f'El SVG no refleja el último partido: falta {value!r}.')

    exports = [
        ('resultado-real-zaragoza-ultima-jornada.png', (1200, 630)),
        ('resultado-real-zaragoza-ultima-jornada-cuadrado.png', (1080, 1080)),
    ]
    for filename, dimensions in exports:
        path = ART / filename
        with Image.open(path) as image:
            if image.size != dimensions:
                raise RuntimeError(f'{filename}: dimensiones {image.size}; esperadas {dimensions}.')
            if image.info.get('jornada') != expected_round or image.info.get('fecha_partido') != expected_date:
                raise RuntimeError(f'{filename}: los metadatos PNG no coinciden con la jornada y fecha actuales.')
        if path.stat().st_size > 100_000:
            raise RuntimeError(f'{filename} supera 100 KB.')

    stats_svg = ART / 'estadisticas-real-zaragoza-ultima-jornada.svg'
    stats_png = ART / 'estadisticas-real-zaragoza-ultima-jornada.png'
    if stats:
        if pages.statistics is None or pages.statistics.get('data-jornada') != expected_round or pages.statistics.get('data-fecha-partido') != expected_date:
            raise RuntimeError('La tarjeta de estadísticas de la galería no coincide con el partido actual.')
        if pages.statistics_image != '../assets/ilustraciones/estadisticas-real-zaragoza-ultima-jornada.png':
            raise RuntimeError('La galería no enlaza la miniatura de estadísticas actual.')
        statistics_description = ET.parse(stats_svg).getroot().findtext('{*}desc') or ''
        for value in (expected_display_date, percentage_text(stats['posesion_pct']), str(stats['tiros_zaragoza']), str(stats['tiros_rival'])):
            if value not in statistics_description:
                raise RuntimeError(f'El gráfico estadístico no coincide con la ficha completa: falta {value!r}.')
        if 'a_puerta_zaragoza' in stats:
            for value in (str(stats['a_puerta_zaragoza']), str(stats['a_puerta_rival'])):
                if value not in statistics_description:
                    raise RuntimeError(f'El gráfico no refleja los tiros a puerta validados: falta {value!r}.')
        with Image.open(stats_png) as image:
            if image.size != (1200, 630) or image.info.get('jornada') != expected_round or image.info.get('fecha_partido') != expected_date:
                raise RuntimeError('La miniatura de estadísticas no coincide con la jornada/fecha o dimensiones esperadas.')
            if 'a_puerta_zaragoza' in stats and (image.info.get('a_puerta_zaragoza') != str(stats['a_puerta_zaragoza']) or image.info.get('a_puerta_rival') != str(stats['a_puerta_rival'])):
                raise RuntimeError('Los tiros a puerta del PNG no coinciden con los valores validados.')
        if stats_png.stat().st_size > 100_000:
            raise RuntimeError('La miniatura estadística supera 100 KB.')
    elif pages.statistics is not None or stats_svg.exists() or stats_png.exists():
        raise RuntimeError('Se ha publicado un gráfico estadístico sin cobertura completa.')

    archive_results = ART / 'archivo-jornadas'
    archive_stats = ART / 'estadisticas-jornadas'
    expected_matches = {(visual_season(row), int(row['jornada'])): row for row in data['partidos']}
    if len(pages.archive_rows) != len(expected_matches):
        raise RuntimeError(f'El archivo visual muestra {len(pages.archive_rows)} jornadas; se esperaban {len(expected_matches)}.')
    actual_rounds = {row.get('data-comparison-id') for row in pages.archive_rows}
    expected_rounds = {f'{season}|{round_num}' for season, round_num in expected_matches}
    if actual_rounds != expected_rounds:
        raise RuntimeError('Las jornadas del índice visual no coinciden con datos/zaragoza.json.')
    archive_html = (ROOT / 'archivo-visual' / 'index.html').read_text(encoding='utf-8')
    required_archive_controls = (
        'id="archivo-temporada"', 'id="archivo-rival"',
        'id="comparar-jornada-a"', 'id="comparar-jornada-b"',
        'data-panel-comparacion="a"', 'data-panel-comparacion="b"',
        'data-recuento-archivo', 'archivo-visual.js', 'archivo-visual.css',
        'id="titulo-resumen-0"', 'data-compartir-comparacion',
        'data-descargar-comparacion="svg"', 'data-descargar-comparacion="png"',
        'id="formato-comparacion"', 'data-controles-descarga', 'data-incluir-metricas',
        'data-incluir-pie', 'data-aviso-stories', 'data-aviso-carrusel',
        'data-sin-cabecera', 'data-mostrar-marca', 'data-descargas-individuales', 'data-descargas-carrusel',
        'frase-carrusel', 'ejemplos-frase-carrusel', 'data-contador-frase-carrusel', 'data-preview-carrusel',
        'data-guardar-comparacion', 'data-restablecer-opciones', 'data-copiar-imagen',
        'data-preset-selector', 'data-guardar-preset', 'data-borrar-preset', 'data-miniaturas-formatos',
        'data-miniatura-formato="apaisado"', 'data-miniatura-formato="cuadrado"', 'data-miniatura-formato="vertical"',
        'data-miniatura-formato="historias"', 'data-miniatura-formato="carrusel"',
        'data-paleta-visual', 'data-aviso-contraste', 'value="contraste"', 'value="papel"',
        'data-encuadre-visual', 'data-densidad-visual', 'data-guia-zonas', 'data-miniatura-zonas',
        'data-comparar-estilos', 'data-vista-encuadre="a"', 'data-vista-densidad="a"',
        'data-texto-alternativo', 'data-generar-texto-alternativo', 'data-copiar-texto-alternativo',
        'data-formato-kit', 'data-descargar-kit',
        'data-hoja-plantilla="portada"', 'data-hoja-plantilla="social-vertical"',
        'data-temporada-mapa', 'data-formato-mapa', 'data-tipo-mapa', 'data-descargar-mapa', 'data-kit-estimaciones',
        'data-lamina-mapa', 'data-texto-mapa', 'data-restablecer-texto-mapa', 'data-preview-mapa-img',
        'data-rival-mapa', 'data-desde-mapa', 'data-hasta-mapa', 'data-forma-reciente', 'data-racha-temporada', 'data-forma-rival', 'data-forma-rival-estado', 'data-descargar-carrusel-temporada', 'data-compartir-mapa', 'id="datos-forma-rivales"',
        'data-nombre-enlace-mapa', 'data-guardar-enlace-mapa', 'data-enlaces-guardados', 'data-estado-enlaces-guardados',
        'data-exportar-enlaces-mapa', 'data-importar-enlaces-mapa', 'data-archivo-enlaces-mapa',
        'data-generar-qr-enlace', 'data-descargar-qr-enlace', 'data-copiar-qr-enlace', 'data-nombre-qr-enlace', 'data-color-qr-enlace', 'data-tamano-qr-enlace', 'data-vista-qr-enlace',
        'social-cuadrada', 'social-vertical',
        'data-descargar-comparacion="webp"', 'Carrusel · 2 diapositivas cuadradas',
        '1080 × 1080', '1080 × 1350', '1080 × 1920', '1200 × 630',
        'data-completa="1"', 'estado-cobertura completa',
    )
    missing_controls = [marker for marker in required_archive_controls if marker not in archive_html]
    if missing_controls:
        raise RuntimeError('Faltan elementos del archivo comparador: ' + ', '.join(missing_controls))
    if archive_html.count('data-comparison-id="') != len(expected_matches):
        raise RuntimeError('El índice no conserva una fila y datos filtrables para cada jornada.')
    complete_count = sum(bool(match_statistics(record, fixture_for(data, record))) for record in data['partidos'])
    if archive_html.count('estado-cobertura completa') != complete_count:
        raise RuntimeError('La insignia de cobertura no coincide con las fichas completas.')
    rival_script = re.search(r'<script type="application/json" id="datos-forma-rivales">(.*?)</script>', archive_html, re.S)
    if not rival_script:
        raise RuntimeError('Falta el conjunto generado de resultados recientes de los rivales.')
    actual_rival_form = json.loads(rival_script.group(1))
    aliases = {'Cartagena':'FC Cartagena','Antequera':'Antequera CF','Gimnàstic':'Gimnàstic de Tarragona','Gimnastic':'Gimnàstic de Tarragona','Real Jaen':'Real Jaén','Hercules':'Hércules','Alcorcon':'Alcorcón'}
    expected_rival_form: dict[str, list[dict[str, object]]] = {}
    results_path = ROOT / 'analisis' / 'real-zaragoza' / 'datos' / 'entrada' / 'grupo2_resultados.csv'
    with results_path.open(encoding='utf-8-sig', newline='') as source:
        for result in csv.DictReader(source):
            try:
                home_goals, away_goals, round_num = int(result['goles_local']), int(result['goles_visitante']), int(result['jornada'])
            except (KeyError, TypeError, ValueError):
                continue
            date = result.get('fecha', '')
            home = aliases.get(result.get('local', ''), result.get('local', ''))
            away = aliases.get(result.get('visitante', ''), result.get('visitante', ''))
            try:
                date_type.fromisoformat(date)
            except ValueError:
                continue
            if round_num < 1 or home_goals < 0 or away_goals < 0 or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date) or not home or not away or home == away:
                continue
            if home != 'Real Zaragoza': expected_rival_form.setdefault(home, []).append({'jornada':round_num,'fecha':date,'rival':away,'goles_favor':home_goals,'goles_contra':away_goals})
            if away != 'Real Zaragoza': expected_rival_form.setdefault(away, []).append({'jornada':round_num,'fecha':date,'rival':home,'goles_favor':away_goals,'goles_contra':home_goals})
    expected_rival_form = {team:sorted(matches,key=lambda item:(item['fecha'],item['jornada']),reverse=True)[:5] for team,matches in expected_rival_form.items()}
    if actual_rival_form != expected_rival_form:
        raise RuntimeError('La forma de los rivales no se regeneró con los resultados válidos actuales del CSV.')
    for season in {season for season, _ in expected_matches}:
        if f'Muestra disponible · {season}' not in archive_html:
            raise RuntimeError(f'Falta un resumen independiente para la temporada {season}.')
    archive_script = (ROOT / 'assets' / 'archivo-visual.js').read_text(encoding='utf-8')
    qr_library = ROOT / 'assets' / 'vendor' / 'qrcodegen.js'
    if not qr_library.is_file() or 'assets/vendor/qrcodegen.js' not in archive_html:
        raise RuntimeError('Falta la biblioteca QR local o no está incluida en la página del archivo.')
    saved_link_features = ('exportSeasonSavedLinks', 'importSeasonSavedLinks', 'makeSeasonLinkQr', 'downloadSeasonLinkQr', 'copySeasonLinkQr', 'seasonImportJsonText', 'selecciones-mapa-linea-de-pase.json', '40mm', '60mm', '#2f6b45', 'zipStored(files)', 'LEEME.txt', 'image/png', 'data-fijar-enlace-mapa', 'data-subir-enlace-mapa', 'data-bajar-enlace-mapa', 'saveSeasonSavedLinks', 'window.qrcodegen.QrCode.encodeText')
    missing_saved_link_features = [marker for marker in saved_link_features if marker not in archive_script]
    if missing_saved_link_features:
        raise RuntimeError('Faltan funciones para transferir, ordenar o generar QR: ' + ', '.join(missing_saved_link_features))
    if "rowA.dataset.completa === '1' && rowB.dataset.completa === '1'" not in archive_script or 'row.hidden = !show' not in archive_script or 'jornada_a' not in archive_script or 'navigator.clipboard.writeText' not in archive_script or "url.searchParams.set('temporada'" not in archive_script or "url.searchParams.set('rival'" not in archive_script or 'navigator.clipboard.write([new ClipboardItem' not in archive_script or 'preferencesKey' not in archive_script or 'favoriteKey' not in archive_script or 'builtInPresets' not in archive_script or 'social-cuadrada' not in archive_script or 'social-vertical' not in archive_script or 'paletteSelect' not in archive_script or 'updateContrastNotice' not in archive_script or 'minimum >= 4.5' not in archive_script or 'framingSelect' not in archive_script or 'densitySelect' not in archive_script or "density === 'esencial'" not in archive_script or "framing === 'protagonista'" not in archive_script or 'updateSafeZoneGuide' not in archive_script or 'updateStyleComparisons' not in archive_script or 'downloadSocialKit' not in archive_script or 'describeRows' not in archive_script or 'texto-alternativo.txt' not in archive_script or 'readPersonalPresets' not in archive_script or 'updateFormatThumbnails' not in archive_script or 'data-restablecer-opciones' not in archive_script or 'canvas.toBlob' not in archive_script or 'comparisonSvg(' not in archive_script or 'cuadrado' not in archive_script or 'vertical' not in archive_script or 'historias' not in archive_script or 'carrusel' not in archive_script or 'zipStored(files)' not in archive_script or 'includeHeader' not in archive_script or 'showBrand' not in archive_script or 'contextText' not in archive_script or 'index===0?carouselContext' not in archive_script or 'slice(0,72)' not in archive_script or 'image/webp' not in archive_script or 'captionToggle?.checked' not in archive_script or 'metricsToggle?.checked' not in archive_script or 'seasonPosterSvg' not in archive_script or 'updateContactSheet' not in archive_script or 'scheduleKitEstimates' not in archive_script or 'No disponible' not in archive_script or 'seasonPosterPageSize' not in archive_script or 'posterOutcome' not in archive_script or 'seasonPosterDescription' not in archive_script or 'lamina-${String(index+1).padStart(2,' not in archive_script or 'updateSeasonForm' not in archive_script or 'seasonCarouselSvg' not in archive_script or 'downloadSeasonCarousel' not in archive_script or 'seasonPosterRival' not in archive_script or 'row.dataset.fechaPartido>=seasonPosterFrom.value' not in archive_script or 'updateOpponentRecentForm' not in archive_script or 'seasonOpponentForms' not in archive_script or 'restoreSeasonPosterFromUrl' not in archive_script or 'mapa-temporada' not in archive_script or 'seasonSavedLinksKey' not in archive_script or 'saveNamedSeasonPosterLink' not in archive_script or 'applySavedSeasonPosterLink' not in archive_script or "historias:{width:1080,height:1920" not in archive_script:
        raise RuntimeError('Los filtros o el requisito de métricas completas no están activos en el script del archivo.')
    for row in pages.archive_rows:
        round_num = int(row['data-jornada'])
        season = visual_season(next(record for record in data['partidos'] if int(record['jornada']) == round_num and visual_season(record) == row.get('data-temporada')))
        if row.get('data-fecha-partido') != expected_matches[(season, round_num)]['fecha']:
            raise RuntimeError(f'La fecha de J{round_num:02d} en el índice visual no coincide con datos/zaragoza.json.')
    for (season, round_num), record in expected_matches.items():
        round_name = archive_round_name(record, data['partidos'])
        for extension in ('svg', 'png'):
            path = archive_results / f'{round_name}.{extension}'
            if not path.is_file():
                raise RuntimeError(f'Falta el gráfico archivado: {path.name}.')
            if extension == 'png':
                with Image.open(path) as image:
                    if image.size != (1200, 630):
                        raise RuntimeError(f'{path.name}: dimensiones {image.size}; esperadas (1200, 630).')
                    if image.info.get('jornada') != str(round_num) or image.info.get('fecha_partido') != record['fecha']:
                        raise RuntimeError(f'{path.name}: metadatos de jornada/fecha incorrectos.')
                    if image.info.get('temporada') != season:
                        raise RuntimeError(f'{path.name}: metadato de temporada incorrecto.')
                if path.stat().st_size > 100_000:
                    raise RuntimeError(f'{path.name} supera 100 KB.')
        fixture_row = next((row for row in data.get('fichas', []) if str(row.get('partido_id')) == str(record.get('partido_id'))), None)
        archived_metrics = match_statistics(record, fixture_row)
        stats_svg_path = archive_stats / f'{round_name}.svg'
        stats_png_path = archive_stats / f'{round_name}.png'
        if archived_metrics:
            if not stats_svg_path.is_file() or not stats_png_path.is_file():
                raise RuntimeError(f'Falta el gráfico estadístico archivado para J{round_num:02d}.')
            with Image.open(stats_png_path) as image:
                if image.size != (1200, 630) or image.info.get('jornada') != str(round_num) or image.info.get('fecha_partido') != record['fecha']:
                    raise RuntimeError(f'{stats_png_path.name}: dimensiones o metadatos incorrectos.')
                if image.info.get('temporada') != season:
                    raise RuntimeError(f'{stats_png_path.name}: metadato de temporada incorrecto.')
                if image.info.get('posesion_pct') != str(archived_metrics['posesion_pct']):
                    raise RuntimeError(f'{stats_png_path.name}: posesión no coincide con los datos validados.')
                for field in ('tiros_zaragoza', 'tiros_rival'):
                    if image.info.get(field) != str(archived_metrics[field]):
                        raise RuntimeError(f'{stats_png_path.name}: {field} no coincide con los datos validados.')
                if 'a_puerta_zaragoza' in archived_metrics:
                    for field in ('a_puerta_zaragoza', 'a_puerta_rival'):
                        if image.info.get(field) != str(archived_metrics[field]):
                            raise RuntimeError(f'{stats_png_path.name}: {field} no coincide con los datos validados.')
            if stats_png_path.stat().st_size > 100_000:
                raise RuntimeError(f'{stats_png_path.name} supera 100 KB.')
        elif stats_svg_path.exists() or stats_png_path.exists():
            raise RuntimeError(f'Hay estadísticas archivadas para J{round_num:02d} sin cobertura validada.')
    for (season, round_num), record in expected_matches.items():
        round_name = archive_round_name(record, data['partidos'])
        expected_link = f'../assets/ilustraciones/archivo-jornadas/{round_name}.png'
        if expected_link not in pages.archive_links:
            raise RuntimeError(f'El índice no enlaza el PNG de J{round_num:02d}.')
        fixture_row = next((row for row in data.get('fichas', []) if str(row.get('partido_id')) == str(record.get('partido_id'))), None)
        if match_statistics(record, fixture_row):
            expected_stats_link = f'../assets/ilustraciones/estadisticas-jornadas/{round_name}.png'
            if expected_stats_link not in pages.archive_links:
                raise RuntimeError(f'El índice no enlaza el PNG estadístico de J{round_num:02d}.')

    printable_score = f'{goals_home}-{goals_away}'
    print(f'Marcador sincronizado: J{int(expected_round):02d}, {expected_date}, {home} {printable_score} {away}; portada, galería y archivo de {len(expected_matches)} jornadas verificados.')


if __name__ == '__main__':
    main()
