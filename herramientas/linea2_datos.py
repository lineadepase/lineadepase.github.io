"""Contrasta resultados, cobertura y procedencia local sin completar cifras."""
import csv
from datetime import date
import json
from pathlib import Path


def audit(root):
    data = json.loads((root / 'datos/zaragoza.json').read_text(encoding='utf-8'))
    group = json.loads((root / 'datos/comparador-grupo2.json').read_text(encoding='utf-8'))
    folder = root / 'analisis/real-zaragoza/datos/entrada'
    with (folder / 'partidos.csv').open(encoding='utf-8-sig', newline='') as stream:
        source = {int(row['jornada']): row for row in csv.DictReader(stream) if row['competicion'] == 'Primera Federación'}
    with (folder / 'estadisticas.csv').open(encoding='utf-8-sig', newline='') as stream:
        statistics = {(row['partido_id'],row['metrica']):row for row in csv.DictReader(stream) if row['periodo']=='Partido' and row['calidad']=='ok'}
    with (folder / 'tiros.csv').open(encoding='utf-8-sig', newline='') as stream:
        shots = {row['partido_id']:row for row in csv.DictReader(stream)}
    errors, rows = [], []
    seen = set()
    for match in data['partidos']:
        number = match['jornada']
        if number in seen:
            errors.append(f'Jornada duplicada: {number}')
        seen.add(number)
        original = source.get(number)
        if not original:
            errors.append(f'J{number}: sin procedencia local')
            continue
        for field in ['fecha', 'rival', 'sede']:
            if match[field] != original[field]:
                errors.append(f'J{number}: discrepancia en {field}')
        for field in ['goles_favor', 'goles_contra']:
            if type(match[field]) is not int or match[field] < 0 or match[field] != int(original[field]):
                errors.append(f'J{number}: marcador inconsistente')
        if date.fromisoformat(match['fecha']) > date.fromisoformat(data['corte']):
            errors.append(f'J{number}: fecha posterior al corte')
        if not original['fuente_url'].startswith('https://'):
            errors.append(f'J{number}: falta URL de fuente')
        if match.get('completo') is True:
            for field in ['tiros_zaragoza', 'tiros_rival', 'posesion_pct']:
                value = match.get(field)
                if not isinstance(value, (float, int)) or isinstance(value, bool) or value < 0:
                    errors.append(f'J{number}: ficha completa sin {field} válido')
            shot_source=shots.get(original['partido_id'])
            if not shot_source or shot_source.get('completo')!='si' or not shot_source.get('fuente_url','').startswith('https://'):
                errors.append(f'J{number}: falta ficha de tiros completa con fuente')
            else:
                for field in ['tiros_zaragoza','tiros_rival','posesion_pct']:
                    if match.get(field)!=float(shot_source[field]):
                        errors.append(f'J{number}: {field} no coincide con tiros.csv')
            for field,metric,column in [('tiros_zaragoza','tiros','zaragoza'),('tiros_rival','tiros','valor_rival'),('posesion_pct','posesion_pct','zaragoza')]:
                record=statistics.get((original['partido_id'],metric))
                if record and match.get(field)!=float(record[column]):
                    errors.append(f'J{number}: {field} difiere de estadisticas.csv')
            if isinstance(match.get('posesion_pct'),(int,float)) and match['posesion_pct'] > 100:
                errors.append(f'J{number}: posesión fuera de rango')
        rows.append({'jornada': number, 'fecha': match['fecha'], 'rival': match['rival'],
                     'fuente': original['fuente_url'], 'metricas_validadas': match.get('completo') is True})
    if set(source) != seen:
        errors.append('El conjunto de jornadas de origen no coincide con el JSON')
    return {'corte_zaragoza': data['corte'], 'corte_grupo': group['fecha'],
            'jornada_zaragoza': data['jornada'], 'jornada_grupo': group['jornada'],
            'resultados': len(rows), 'fichas_completas': sum(r['metricas_validadas'] for r in rows),
            'fichas_pendientes': [r['jornada'] for r in rows if not r['metricas_validadas']],
            'alcance': 'Consistencia con archivos de origen locales; no certifica todas las fuentes externas ni actualiza el corte.',
            'errores': errors, 'jornadas': rows}


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    result = audit(root)
    (root / 'documentacion/linea2-revision-datos.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'jornadas'}, ensure_ascii=False))
    raise SystemExit(bool(result['errores']))


def coverage_note(data, group):
    from html import escape
    from cortes import nota_corte_grupo
    available = sum(m.get('completo') is True for m in data['partidos'])
    note = nota_corte_grupo(group['jornada'],group['fecha'],data['jornada'],data['corte'])
    return '<aside class="catalogue-note" aria-label="Cobertura y cortes de los datos"><h3>Antes de comparar</h3><p>'+escape(note)+'</p><p>'+str(available)+' fichas estadísticas completas de '+str(len(data['partidos']))+' resultados. Las demás siguen pendientes y no aportan valores a las medias.</p><a href="../datos-en-revision/">Revisar discrepancias y fuentes →</a></aside>'
