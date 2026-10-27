# Plantilla editorial: crónica pospartido

Duplica esta estructura después del encuentro. Sustituye las indicaciones entre corchetes por hechos confirmados y borra cualquier bloque que no aporte información. Esta plantilla no se publica vacía.

## Titular

{Equipo local} {marcador} {equipo visitante}: {hecho principal del partido}

## Entradilla

{Resultado, competición y consecuencia inmediata. Una frase.}

## El partido

{Cómo se desarrolló el encuentro y qué cambió con el marcador. Mantener el relato en tercera persona.}

## Las acciones decisivas

- {Minuto y acción confirmados, si los hubo.}
- {Incidencia que cambió el partido, solo si está verificada.}

## La lectura del juego

{Dos o tres observaciones concretas sobre progresión, área, transiciones o balón parado. Separar los datos de la interpretación; no atribuir causalidad a una cifra por sí sola.}

## Qué deja el resultado

{Efecto en la eliminatoria, clasificación o próximo encuentro, con el dato actualizado.}

## Fuentes

Incluir una o dos fuentes primarias como máximo. Añadir la fecha y hora de comprobación en hora peninsular. Si una cifra no se puede confirmar, omitirla.

## Revisión antes de publicar

- Resultado, goleadores y minutos coinciden con la fuente elegida.
- El texto está en tercera persona, sin dirigirse al lector ni hablar como si fuera una crónica automática.
- Cada cifra aporta contexto y tiene una fuente comprobable.
- Las imágenes conservan su crédito y texto alternativo.
- Solo después de confirmar el marcador, añadir `postpartido_url` y `resultado_confirmado` en `datos/previas.json`. El bloque `resultado_confirmado` requiere `marcador`, `fecha_verificacion` con zona horaria peninsular y una o dos fuentes oficiales. Sin esos datos, la portada no anuncia un resultado ni enlaza la crónica.

Ejemplo de registro (sustituir por datos comprobados):

```json
"postpartido_url": "proyectos/real-zaragoza/jornada-N.html",
"resultado_confirmado": {
  "marcador": "G–G",
  "fecha_verificacion": "AAAA-MM-DDThh:mm:ss+01:00",
  "fuentes": [{"nombre": "Fuente oficial", "url": "https://..."}]
}
```
