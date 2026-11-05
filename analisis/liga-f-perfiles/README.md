# Liga F 2023/24: perfiles de jugadoras

Plan de la investigación de noviembre (estado: planificada; desarrollo del 9 al 20 de noviembre, publicación el 26). Esta carpeta solo contiene el esqueleto; el código, los datos de salida y los gráficos llegarán en esta misma rama.

## Pregunta

¿Qué tipos de jugadora hay en la Liga F según lo que hacen con el balón y sin él, más allá de la posición que figura en la alineación? ¿Cuántos perfiles distintos se sostienen con los datos y quiénes los representan mejor?

## Datos

- [StatsBomb Open Data](https://github.com/hudl/open-data): Liga F 2023/24, la única temporada de la competición disponible (240 partidos, jornadas 1 a 30). Es la misma que usa la investigación [liga-f-xt](../liga-f-xt/), con el mismo commit fijado y su acuerdo de uso: se pueden publicar análisis, no redistribuir los datos, y el logotipo del proveedor va en lo publicado.
- Eventos usados: pases (con destino, altura y resultado), conducciones, presiones, recuperaciones, duelos, intercepciones, tiros, regates y faltas. Los minutos se reconstruyen con el once, los cambios y las expulsiones, como en liga-f-xt.
- Filtro: mínimo de minutos por jugadora (propuesta: 900, igual que en xT; alternativa: 600 para ampliar la muestra).

## Variables (por 90 minutos)

| Familia | Variables |
|---|---|
| Progresión | pases progresivos, conducciones progresivas, xT neto por 90 (reutilizando el modelo de liga-f-xt) |
| Construcción | pases intentados, % de pases completados, pases largos, centros |
| Zona | altura media de las acciones y proporción en el último tercio |
| Defensa | presiones (y % en campo rival), recuperaciones, intercepciones, duelos ganados |
| Remate | tiros, tiros en el área, regates intentados |

Se evita meter variables casi redundantes: se revisa la correlación y se descartan las que pasen de 0,85.

## Método

1. Estandarizar cada variable (puntuación z) para que ninguna domine por escala; las tasas muy asimétricas, con transformación logarítmica previa.
2. PCA solo para visualizar y para ver qué ejes explican la variación; el agrupamiento se hace sobre las variables estandarizadas (o sobre las componentes que acumulan el 80 %, a decidir con ambas versiones).
3. K-means como método principal y clustering jerárquico (Ward) como contraste.
4. Número de grupos entre 2 y 8, elegido con tres criterios a la vez: coeficiente de silueta, estabilidad (índice de Rand ajustado entre agrupaciones de 200 remuestras de jugadoras) y que cada perfil tenga al menos 8 jugadoras e interpretación futbolística clara. Si silueta y estabilidad no apoyan ningún número con claridad, se dice y se presenta el más interpretable con esa advertencia.
5. Comprobaciones de sensibilidad: 600 frente a 900 minutos, con y sin xT, k-means frente a jerárquico.

## Qué se mostrará

- Radar por perfil (valores z medios de las variables principales).
- Mapa de jugadoras: las dos primeras componentes del PCA, coloreadas por perfil.
- Las jugadoras más representativas de cada perfil (las más cercanas al centro del grupo), con su pertenencia dudosa señalada cuando están entre dos grupos.
- Formatos: web y LinkedIn 1600 × 900, Facebook 1200 × 630, Instagram 1080 × 1350; logotipo de StatsBomb y fuente visibles.

## Límites

- Una sola temporada: describe 2023/24, no la forma actual de ninguna jugadora.
- Las jugadoras del Barcelona dominan muchas variables de posesión y progresión: el contexto del equipo contamina el perfil. Se mostrará el reparto de cada perfil por equipo y se probará a ajustar por equipo.
- Sin tracking ni movimientos sin balón; las presiones y recuperaciones dependen de cómo se registre cada partido.
- Los grupos son una simplificación: se presentan como perfiles útiles, no como categorías reales. Las porteras se excluyen y la posición registrada solo se usa para interpretar.
- Con unas 150-200 jugadoras por encima del mínimo, la estabilidad de los grupos pequeños es limitada.

## Estructura prevista

```
liga-f-perfiles/
├── codigo/      descarga fijada, variables por 90, agrupamiento y gráficos; un solo script (ejecutar.py)
├── datos/salida/  resultados agregados, sin eventos de StatsBomb
├── graficos/
├── pruebas/     minutos, estandarización, silueta con soluciones conocidas
└── requirements.txt
```

Análisis personal. Sin relación con ningún club ni competición.
