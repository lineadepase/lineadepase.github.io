"""Comprueba que portada, galería y exportaciones reflejan el mismo partido."""
from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image
from segunda_edicion import match_statistics, percentage_text

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

    def handle_endtag(self, tag: str) -> None:
        if tag == 'figure' and self._in_home:
            self._in_home = False
        if tag == 'article' and self._in_gallery:
            self._in_gallery = False
        if tag == 'article' and self._in_statistics:
            self._in_statistics = False


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

    printable_score = f'{goals_home}-{goals_away}'
    print(f'Marcador sincronizado: J{int(expected_round):02d}, {expected_date}, {home} {printable_score} {away}; portada, galería, SVG y PNG correctos.')


if __name__ == '__main__':
    main()
