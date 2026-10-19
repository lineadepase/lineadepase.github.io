# -----------------------------------------------------------------------------
# Comprobación 2: minutos jugados por cada jugador
#
# Reglas (las mismas que en calculos.py):
#   - Titular: juega desde el minuto 0 hasta el minuto en que sale.
#     Si no le cambian, juega 90.
#   - Suplente: juega desde el minuto en que entra hasta el 90.
#
# Límites que conviene tener en cuenta (también están en el README):
#   - No cuento el descuento: un partido completo son 90 minutos.
#   - Si un suplente vuelve a salir, termina en el minuto de salida.
#   - Las expulsiones con minuto registrado son salidas sin cambio.
#
# Sumo los minutos de todos los partidos de liga y comparo con la columna
# «minutos» de datos/salida/jugadores.csv.
# -----------------------------------------------------------------------------

MINUTOS_PARTIDO <- 90

comprobar_minutos <- function(datos) {
  alineaciones <- datos$alineaciones
  cambios <- datos$cambios

  # Voy partido a partido y guardo una tabla pequeña con (jugador, minutos)
  # para cada uno. Al final las junto todas.
  filas <- list()
  for (id in unique(alineaciones$partido_id)) {
    once <- alineaciones$jugador[alineaciones$partido_id == id]
    cambios_partido <- cambios[cambios$partido_id == id, ]

    # Titulares: match() busca a cada titular en la columna «sale» de los
    # cambios. Si lo encuentra, juega hasta ese minuto; si no, hasta el 90.
    sale <- ifelse(once %in% cambios_partido$sale,
                   cambios_partido$minuto[match(once, cambios_partido$sale)],
                   MINUTOS_PARTIDO)
    tarjetas <- datos$tarjetas
    expulsados <- tarjetas[tarjetas$partido_id == id &
      tarjetas$tarjeta %in% c("Roja", "Segunda amarilla") & !is.na(tarjetas$minuto), ]
    for (i in seq_along(once)) {
      m <- expulsados$minuto[expulsados$jugador == once[i]]
      if (length(m)) sale[i] <- min(sale[i], m, MINUTOS_PARTIDO)
    }
    filas[[length(filas) + 1]] <- data.frame(jugador = once, minutos = sale)

    # Suplentes: los que entran, desde su minuto hasta el 90
    finales <- rep(MINUTOS_PARTIDO, nrow(cambios_partido))
    for (i in seq_along(cambios_partido$entra)) {
      jugador <- cambios_partido$entra[i]
      m <- c(cambios_partido$minuto[cambios_partido$sale == jugador],
             expulsados$minuto[expulsados$jugador == jugador])
      if (length(m)) finales[i] <- min(finales[i], m)
    }
    filas[[length(filas) + 1]] <- data.frame(jugador = cambios_partido$entra,
                                             minutos = finales - cambios_partido$minuto)
  }

  # Sumo por jugador los minutos de todos los partidos
  minutos <- aggregate(minutos ~ jugador, data = do.call(rbind, filas), FUN = sum)

  comparar(minutos, datos$py_jugadores, clave = "jugador", columnas = "minutos",
           que = "Los minutos por jugador no coinciden con Python")

  invisible(minutos)
}
