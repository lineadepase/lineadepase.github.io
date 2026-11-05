# Liga F 2023/24: perfiles de jugadoras

¿Qué tipos de jugadora hay en la Liga F según lo que hacen en el campo, más allá de su posición? El estudio agrupa a 220 jugadoras con al menos 900 minutos y salen cuatro perfiles: iniciadoras, pulmones, las de área y desequilibrantes. Se publica en [Línea de pase](https://lineadepase.com/proyectos/liga-f-perfiles/).

Es un análisis histórico: la temporada 2023/24 es la única de la Liga F con datos abiertos de StatsBomb.

## Estructura

```
liga-f-perfiles/
├── codigo/
│   ├── datos.py            descarga fijada a un commit de StatsBomb y minutos jugados (como en liga-f-xt)
│   ├── modelo.py           modelo de xT de liga-f-xt, reutilizado
│   ├── caracteristicas.py  variables por jugadora y partido a partir de los eventos
│   ├── base.py             tabla de jugadoras con sus variables por 90 minutos
│   ├── perfiles.py         estandarización, PCA, k-means, silueta y estabilidad, sensibilidad
│   ├── graficos.py         gráficos de web, LinkedIn, Facebook e Instagram
│   ├── web.py              página del estudio y textos de las redes
│   └── ejecutar.py         ejecuta todo en orden
├── datos/salida/           resultados agregados (no contiene eventos de StatsBomb)
├── documentacion/          manifiesto de descargas con SHA-256 y cobertura
├── graficos/               PNG y SVG: web y LinkedIn 1600×900, Facebook 1200×630, Instagram 1080×1350
├── publicaciones/          carrusel de Instagram (8 diapositivas), textos de cada red y textos alternativos
├── pruebas/                pruebas con soluciones conocidas
├── recursos/statsbomb.png  logotipo del proveedor, obligatorio en lo publicado
└── requirements.txt
```

## Método

1. Se calculan 18 variables por 90 minutos con los eventos de los 240 partidos: progresión con pases y conducciones, pases largos y de tiro, centros, amenaza esperada (xT, el modelo de liga-f-xt con validación cruzada por partidos), altura media de las acciones, recepciones en el área, regates, tiros, xG, presiones, recuperaciones, intercepciones y entradas.
2. Se incluyen las jugadoras de campo con al menos 900 minutos (220). Las variables asimétricas pasan por log1p, se estandarizan (z) y, de cada par con correlación mayor de 0,85, se conserva una: quedan 14.
3. PCA para el mapa; k-means (50 inicios) para los grupos, con Ward jerárquico como contraste.
4. Número de perfiles entre 4 y 7, con al menos 8 jugadoras por grupo, fijado antes de mirar los resultados: gana el que mejor combina silueta y estabilidad (índice de Rand ajustado en 200 remuestras de jugadoras). Resultado: 4 perfiles (`datos/salida/seleccion_k.csv`).
5. Cada perfil recibe nombre según su centro (`perfiles.nombrar`). Las «más típicas» son las más cercanas al centro; las que «más lo llevan al extremo», las que más destacan en las tres variables que definen el perfil.
6. Sensibilidad en `datos/salida/sensibilidad.json`: 600 minutos, sin xT y Ward frente a k-means.

## Cómo ejecutarlo

Desde esta carpeta:

```
pip install -r requirements.txt
python codigo/ejecutar.py --cache <carpeta privada para los datos>
python -m pytest pruebas
```

La primera ejecución descarga unos 700 MB de eventos y alineaciones. Esa carpeta no se sube al repositorio: el acuerdo de StatsBomb no permite redistribuir sus datos. Con `--solo-agrupar` se parte de `datos/salida/jugadoras_base.csv` sin descargar nada.

## Fotos de las jugadoras

Los gráficos identifican a cada jugadora con una chapa de iniciales y el color de su perfil. Si se coloca una foto con licencia propia en `recursos/fotos/<nombre-en-minúsculas-con-guiones>.jpg` (por ejemplo `aitana-bonmati.jpg`), el gráfico la usa en lugar de las iniciales. Las fotos que se usen deben citar su autor y licencia en la publicación.

## Fuentes

- Datos: [StatsBomb Open Data](https://github.com/hudl/open-data), commit `4b73468`. Su [acuerdo de uso](https://github.com/hudl/open-data/blob/4b73468fc5b0f1950f9f66fada70ad3a4f9327cb/LICENSE.pdf) permite publicar análisis, prohíbe redistribuir los datos y su uso comercial, y pide el logotipo en lo publicado.
- Modelo de xT: [Karun Singh](https://karun.in/blog/expected-threat.html), implementación propia (ver [liga-f-xt](../liga-f-xt/)).

Análisis personal. Sin relación con ningún club ni competición.
