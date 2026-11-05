"""Estandarización, PCA, agrupamiento y elección del número de perfiles.

Reglas fijadas antes de mirar los grupos:
- Jugadoras de campo con al menos MINIMO minutos.
- Variables: tasas por 90; log1p en las muy asimétricas; puntuación z; de cada
  par con correlación mayor de 0,85 se queda la que va antes en VARIABLES.
- Número de perfiles k entre 4 y 7 (con 2 o 3 solo se separaría defensa de ataque),
  con al menos 8 jugadoras por perfil; gana el k con mejor media entre silueta y
  estabilidad (índice de Rand ajustado en 200 remuestras, ambos reescalados 0-1
  entre los k candidatos).
- k-means es el método principal; Ward jerárquico, el contraste.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score

ESTUDIO = Path(__file__).resolve().parents[1]
SALIDA = ESTUDIO / 'datos' / 'salida'
MINIMO = 900
SEMILLA = 20261105
VARIABLES = ['xt_neto_90', 'pases_prog_90', 'cond_prog_90', 'pases_90', 'pct_pases', 'pases_largos_90',
             'pases_clave_90', 'centros_90', 'altura_media', 'recepciones_area_90', 'tiros_90', 'xg_90',
             'regates_90', 'presiones_90', 'pct_presion_rival', 'recuperaciones_90', 'intercepciones_90',
             'entradas_90']
NOMBRES = {'xt_neto_90': 'Amenaza (xT) por 90', 'pases_prog_90': 'Pases progresivos', 'cond_prog_90': 'Conducciones progresivas',
           'pases_90': 'Pases', 'pct_pases': '% de pases', 'pases_largos_90': 'Pases largos', 'pases_clave_90': 'Pases de tiro',
           'centros_90': 'Centros', 'altura_media': 'Altura en el campo', 'recepciones_area_90': 'Recepciones en el área',
           'tiros_90': 'Tiros', 'xg_90': 'xG', 'regates_90': 'Regates', 'presiones_90': 'Presiones',
           'pct_presion_rival': '% presión arriba', 'recuperaciones_90': 'Recuperaciones',
           'intercepciones_90': 'Intercepciones', 'entradas_90': 'Entradas ganadas'}


def preparar(base, minimo=MINIMO, con_xt=True):
    d = base[(base.minutos >= minimo) & (base.posicion != 'Portera')].reset_index(drop=True)
    variables = [v for v in VARIABLES if con_xt or v != 'xt_neto_90']
    x = d[variables].copy()
    for v in variables:
        if abs(x[v].skew()) > 1 and x[v].min() >= 0:
            x[v] = np.log1p(x[v])
    corr = x.corr().abs()
    quitar = [b for i, a in enumerate(variables) for b in variables[i + 1:] if corr.loc[a, b] > 0.85 and b not in ()]
    # La primera de cada par se conserva; la segunda se descarta (sin cascada sobre las ya descartadas).
    descartadas = []
    for i, a in enumerate(variables):
        if a in descartadas:
            continue
        for b in variables[i + 1:]:
            if b not in descartadas and corr.loc[a, b] > 0.85:
                descartadas.append(b)
    usadas = [v for v in variables if v not in descartadas]
    z = (x[usadas] - x[usadas].mean()) / x[usadas].std(ddof=0)
    return d, z, usadas, descartadas


def kmeans(z, k, semilla=SEMILLA, n_init=50):
    return KMeans(n_clusters=k, n_init=n_init, random_state=semilla).fit(z)


def estabilidad(z, k, referencia, remuestras=200):
    rng = np.random.default_rng(SEMILLA)
    valores = []
    for _ in range(remuestras):
        idx = rng.integers(0, len(z), len(z))
        m = KMeans(n_clusters=k, n_init=10, random_state=int(rng.integers(1e9))).fit(z.iloc[idx])
        valores.append(adjusted_rand_score(referencia, m.predict(z)))
    return float(np.mean(valores))


def elegir_k(z, ks=range(4, 8)):
    filas = []
    for k in ks:
        m = kmeans(z, k)
        tam = np.bincount(m.labels_)
        filas.append({'k': k, 'silueta': silhouette_score(z, m.labels_), 'estabilidad_rand': estabilidad(z, k, m.labels_),
                      'jugadoras_min_grupo': int(tam.min()), 'tamanos': ' / '.join(map(str, sorted(tam, reverse=True)))})
    t = pd.DataFrame(filas)
    esc = lambda s: (s - s.min()) / (s.max() - s.min()) if s.max() > s.min() else s * 0
    t['puntuacion'] = (esc(t.silueta) + esc(t.estabilidad_rand)) / 2
    valido = t[t.jugadoras_min_grupo >= 8]
    return t, int(valido.sort_values('puntuacion', ascending=False).k.iloc[0])


NOMBRES_PERFIL = ['Iniciadoras', 'Pulmones', 'Las de área', 'Desequilibrantes']


def nombrar(centros):
    """Con k = 4 asigna el nombre según el centro de cada grupo; devuelve {grupo: orden}.

    Desequilibrantes: mayor xT. Iniciadoras: las que juegan más atrás de las restantes.
    Las de área: las más adelantadas de las dos que quedan. Pulmones: el resto.
    """
    restantes = list(centros.index)
    d = centros.xt_neto_90.idxmax(); restantes.remove(d)
    i = centros.loc[restantes, 'altura_media'].idxmin(); restantes.remove(i)
    a = centros.loc[restantes, 'altura_media'].idxmax(); restantes.remove(a)
    return {i: 0, restantes[0]: 1, a: 2, d: 3}


def ejecutar():
    base = pd.read_csv(SALIDA / 'jugadoras_base.csv')
    d, z, usadas, descartadas = preparar(base)
    tabla_k, k = elegir_k(z)
    modelo = kmeans(z, k)
    centros = pd.DataFrame(modelo.cluster_centers_, columns=usadas)
    orden = nombrar(centros) if k == 4 else {g: g for g in range(k)}
    modelo.labels_ = np.array([orden[g] for g in modelo.labels_])
    centros = centros.rename(index=orden).sort_index()
    d['perfil'] = modelo.labels_
    d['perfil_nombre'] = d.perfil.map(lambda g: NOMBRES_PERFIL[g] if k == 4 else f'Perfil {g + 1}')
    pca = PCA(n_components=2, random_state=SEMILLA).fit(z)
    comp = pca.transform(z)
    d['pc1'], d['pc2'] = comp[:, 0], comp[:, 1]
    dist = np.linalg.norm(z.to_numpy()[:, None, :] - centros.to_numpy()[None], axis=2)
    d['distancia_centro'] = dist[np.arange(len(d)), d.perfil]
    segunda = np.sort(dist, axis=1)[:, 1]
    d['entre_dos'] = segunda / d.distancia_centro.clip(lower=1e-9) < 1.15
    ward = AgglomerativeClustering(n_clusters=k, linkage='ward').fit_predict(z)
    d['perfil_ward'] = ward
    sens = {'k': k, 'variables_usadas': usadas, 'variables_descartadas': descartadas, 'jugadoras': len(d),
            'silueta_kmeans': float(silhouette_score(z, d.perfil)),
            'rand_kmeans_vs_ward': float(adjusted_rand_score(d.perfil, ward)),
            'varianza_pca': [float(v) for v in pca.explained_variance_ratio_]}
    d600, z600, _, _ = preparar(base, 600)
    m600 = kmeans(z600, k)
    comunes = d600.jugadora_id.isin(d.jugadora_id)
    ref = d.set_index('jugadora_id').perfil
    sens['rand_900_vs_600'] = float(adjusted_rand_score(ref.loc[d600.jugadora_id[comunes]].to_numpy(), m600.labels_[comunes.to_numpy()]))
    sens['jugadoras_600'] = len(d600)
    dz, zz, _, _ = preparar(base, MINIMO, con_xt=False)
    mz = kmeans(zz, k)
    sens['rand_con_vs_sin_xt'] = float(adjusted_rand_score(d.perfil, mz.labels_))
    cargas = pd.DataFrame(pca.components_.T, index=usadas, columns=['pc1', 'pc2'])
    # Guardado: tablas con z de cada variable para los radares.
    for v in usadas:
        d[f'z_{v}'] = z[v]
    # Prototipo: las más cercanas al centro. Cima: las que más destacan en lo que define al perfil.
    d['prototipo'] = d.groupby('perfil').distancia_centro.rank(method='first')
    definitorias = {g: list(centros.loc[g].nlargest(3).index) for g in centros.index}
    d['puntuacion_perfil'] = [z.loc[i, definitorias[p]].mean() for i, p in zip(d.index, d.perfil)]
    d['cima'] = d.groupby('perfil').puntuacion_perfil.rank(ascending=False, method='first')
    resumen = d.groupby(['perfil', 'perfil_nombre']).agg(jugadoras=('jugadora_id', 'size'), minutos_medios=('minutos', 'mean'),
                                                       **{v: (v, 'mean') for v in VARIABLES}).reset_index()
    resumen['variables_definitorias'] = [', '.join(NOMBRES[v] for v in definitorias[g]) for g in resumen.perfil]
    resumen.round(3).to_csv(SALIDA / 'perfiles_resumen.csv', index=False)
    centros.round(3).to_csv(SALIDA / 'perfiles_centros_z.csv', index_label='perfil')
    pd.crosstab(d.perfil_nombre, d.posicion).to_csv(SALIDA / 'perfiles_por_posicion.csv')
    pd.crosstab(d.equipo, d.perfil_nombre).to_csv(SALIDA / 'perfiles_por_equipo.csv')
    d.round(4).to_csv(SALIDA / 'jugadoras_perfiles.csv', index=False)
    tabla_k.round(4).to_csv(SALIDA / 'seleccion_k.csv', index=False)
    cargas.round(3).to_csv(SALIDA / 'cargas_pca.csv')
    (SALIDA / 'sensibilidad.json').write_text(json.dumps(sens, indent=1, ensure_ascii=False), encoding='utf-8')
    return d, tabla_k, sens


if __name__ == '__main__':
    d, t, s = ejecutar()
    print(t.round(3).to_string()); print(json.dumps(s, indent=1, ensure_ascii=False))
