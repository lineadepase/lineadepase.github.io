# Esquema de la base de datos

Documento generado por `cargar.py --documentar`. No se edita a mano: cambia `manifiesto.py` y vuelve a generarlo.

## `espana_eurocopa_redes`

Redes de pases de España en la Eurocopa femenina 2025.
Origen: `analisis/espana-eurocopa-redes/datos/salida/`.

### `espana_eurocopa_redes.conexiones`

Pases entre cada pareja pasadora-receptora en cada partido. Filas: 491. Clave: partido_id, pasadora, receptora. Archivo: `espana-eurocopa-redes/datos/salida/conexiones.csv`.

| Columna | Tipo |
|---|---|
| `pasadora` | VARCHAR |
| `receptora` | VARCHAR |
| `pases` | BIGINT |
| `partido_id` | BIGINT |
| `rival` | VARCHAR |

### `espana_eurocopa_redes.jugadoras_partido`

Métricas de red de cada jugadora en cada partido (intermediación, PageRank, posición media). Filas: 66. Clave: partido_id, jugadora. Archivo: `espana-eurocopa-redes/datos/salida/jugadoras_partido.csv`.

| Columna | Tipo |
|---|---|
| `jugadora` | VARCHAR |
| `pases_red` | BIGINT |
| `intermediacion` | DOUBLE |
| `pagerank` | DOUBLE |
| `x` | DOUBLE |
| `y` | DOUBLE |
| `toques` | BIGINT |
| `partido_id` | BIGINT |
| `rival` | VARCHAR |
| `fase` | VARCHAR |

### `espana_eurocopa_redes.jugadoras_torneo`

Medias de red de cada jugadora en todo el torneo. Filas: 18. Clave: jugadora. Archivo: `espana-eurocopa-redes/datos/salida/jugadoras_torneo.csv`.

| Columna | Tipo |
|---|---|
| `jugadora` | VARCHAR |
| `redes` | BIGINT |
| `pases_red_media` | DOUBLE |
| `intermediacion_media` | DOUBLE |
| `pagerank_medio` | DOUBLE |
| `nombre` | VARCHAR |

### `espana_eurocopa_redes.partidos`

Un partido de España en la Eurocopa con las métricas de su red de pases. Filas: 6. Clave: partido_id. Archivo: `espana-eurocopa-redes/datos/salida/partidos.csv`.

| Columna | Tipo |
|---|---|
| `partido_id` | BIGINT |
| `fecha` | DATE |
| `fase` | VARCHAR |
| `rival` | VARCHAR |
| `resultado` | VARCHAR |
| `parte_corte` | BIGINT |
| `minuto_corte` | DOUBLE |
| `minutos_red` | DOUBLE |
| `pases_red` | BIGINT |
| `pases_por_minuto` | DOUBLE |
| `jugadoras` | BIGINT |
| `conexiones` | BIGINT |
| `densidad` | DOUBLE |
| `centralizacion` | DOUBLE |
| `pareja_principal` | VARCHAR |
| `pases_pareja_principal` | BIGINT |
| `jugadora_mas_central` | VARCHAR |

## `futbol_femenino`

Licencias de fútbol femenino por territorio (CSD) frente a la población (INE).
Origen: `analisis/futbol-femenino/datos/salida/`.

### `futbol_femenino.criterio_seleccion`

Territorios que cumplen el criterio de selección del análisis. Filas: 17. Clave: territorio. Archivo: `futbol-femenino/datos/salida/criterio_seleccion.csv`.

| Columna | Tipo |
|---|---|
| `territorio` | VARCHAR |
| `hombres_2025` | BIGINT |
| `mujeres_2023` | BIGINT |
| `mujeres_2025` | BIGINT |
| `mujeres_1_enero_2025` | BIGINT |
| `total_2025` | BIGINT |
| `por_mil_mujeres` | DOUBLE |
| `pct_femenino` | DOUBLE |
| `crecimiento_pct` | DOUBLE |
| `aumento_licencias` | BIGINT |
| `cumple` | BOOLEAN |

### `futbol_femenino.indicadores`

Licencias por territorio, por mil mujeres y crecimiento 2023-2025. Filas: 20. Clave: territorio. Archivo: `futbol-femenino/datos/salida/indicadores.csv`.

| Columna | Tipo |
|---|---|
| `territorio` | VARCHAR |
| `hombres_2025` | BIGINT |
| `mujeres_2023` | BIGINT |
| `mujeres_2025` | BIGINT |
| `mujeres_1_enero_2025` | BIGINT |
| `total_2025` | BIGINT |
| `por_mil_mujeres` | DOUBLE |
| `pct_femenino` | DOUBLE |
| `crecimiento_pct` | DOUBLE |
| `aumento_licencias` | BIGINT |

## `grupo2_simulacion`

Simulación Monte Carlo del grupo 2: probabilidades de ascenso, play-off y descenso.
Origen: `analisis/grupo2-simulacion/datos/salida/`.

### `grupo2_simulacion.distribucion_puestos`

Probabilidad de acabar en cada puesto (columnas 1 a 20) para cada equipo. Filas: 20. Clave: equipo. Archivo: `grupo2-simulacion/datos/salida/distribucion_puestos.csv`.

| Columna | Tipo |
|---|---|
| `equipo` | VARCHAR |
| `1` | DOUBLE |
| `2` | DOUBLE |
| `3` | DOUBLE |
| `4` | DOUBLE |
| `5` | DOUBLE |
| `6` | DOUBLE |
| `7` | DOUBLE |
| `8` | DOUBLE |
| `9` | DOUBLE |
| `10` | DOUBLE |
| `11` | DOUBLE |
| `12` | DOUBLE |
| `13` | DOUBLE |
| `14` | DOUBLE |
| `15` | DOUBLE |
| `16` | DOUBLE |
| `17` | DOUBLE |
| `18` | DOUBLE |
| `19` | DOUBLE |
| `20` | DOUBLE |

### `grupo2_simulacion.evolucion_zaragoza`

Cómo han cambiado las probabilidades del Zaragoza jornada a jornada. Filas: 10. Clave: jornada. Archivo: `grupo2-simulacion/datos/salida/evolucion_zaragoza.csv`.

| Columna | Tipo |
|---|---|
| `jornada` | BIGINT |
| `ascenso_directo` | DOUBLE |
| `ascenso_o_playoff` | DOUBLE |
| `descenso` | DOUBLE |
| `puntos_medios` | DOUBLE |

### `grupo2_simulacion.fuerzas_equipos`

Goles esperados a favor y en contra de cada equipo en el modelo. Filas: 20. Clave: equipo. Archivo: `grupo2-simulacion/datos/salida/fuerzas_equipos.csv`.

| Columna | Tipo |
|---|---|
| `equipo` | VARCHAR |
| `goles_a_favor_esperados` | DOUBLE |
| `goles_en_contra_esperados` | DOUBLE |

### `grupo2_simulacion.partidos_zaragoza`

Probabilidades 1X2 y goles esperados de los partidos pendientes del Zaragoza. Filas: 26. Clave: local, visitante. Archivo: `grupo2-simulacion/datos/salida/partidos_zaragoza.csv`.

| Columna | Tipo |
|---|---|
| `local` | VARCHAR |
| `visitante` | VARCHAR |
| `goles_local_esperados` | DOUBLE |
| `goles_visitante_esperados` | DOUBLE |
| `victoria_local` | DOUBLE |
| `empate` | DOUBLE |
| `victoria_visitante` | DOUBLE |

### `grupo2_simulacion.probabilidades`

Probabilidad de ascenso directo, play-off y descenso de cada equipo, con puntos esperados. Filas: 20. Clave: equipo. Archivo: `grupo2-simulacion/datos/salida/probabilidades.csv`.

| Columna | Tipo |
|---|---|
| `equipo` | VARCHAR |
| `ascenso_directo` | DOUBLE |
| `playoff` | DOUBLE |
| `descenso` | DOUBLE |
| `puesto_medio` | DOUBLE |
| `puntos_medios` | DOUBLE |
| `puntos_p10` | DOUBLE |
| `puntos_p90` | DOUBLE |
| `ascenso_o_playoff` | DOUBLE |

## `liga_f_xt`

Amenaza esperada (xT) de las jugadoras de la Liga F con StatsBomb Open Data.
Origen: `analisis/liga-f-xt/datos/salida/`.

### `liga_f_xt.cobertura_validacion`

Control de calidad por partido: eventos, duplicados y coordenadas inválidas. Filas: 240. Clave: partido_id. Archivo: `liga-f-xt/datos/salida/cobertura_validacion.csv`.

| Columna | Tipo |
|---|---|
| `partido_id` | BIGINT |
| `fecha` | DATE |
| `jornada` | BIGINT |
| `eventos` | BIGINT |
| `duplicados` | BIGINT |
| `sin_coordenadas` | BIGINT |
| `coordenadas_invalidas` | BIGINT |
| `acciones_seleccionadas` | BIGINT |
| `intervalos_posicion_invertidos` | BIGINT |

### `liga_f_xt.jugadoras_xt`

xT neto, por 90 minutos y por 100 acciones de cada jugadora, con intervalo al 95 %. Filas: 401. Clave: jugadora_id, equipo. Archivo: `liga-f-xt/datos/salida/jugadoras_xt.csv`.

| Columna | Tipo |
|---|---|
| `jugadora_id` | BIGINT |
| `jugadora` | VARCHAR |
| `equipo` | VARCHAR |
| `partidos` | BIGINT |
| `minutos` | DOUBLE |
| `xt_neto` | DOUBLE |
| `xt_positivo` | DOUBLE |
| `xt_con_perdidas` | DOUBLE |
| `acciones` | DOUBLE |
| `xt_neto_90` | DOUBLE |
| `ic95_inferior` | DOUBLE |
| `ic95_superior` | DOUBLE |
| `xt_por_100_acciones` | DOUBLE |
| `elegible_900` | BOOLEAN |

### `liga_f_xt.resumen_tipos`

xT total repartido por tipo de acción (pase o conducción). Filas: 2. Clave: tipo. Archivo: `liga-f-xt/datos/salida/resumen_tipos.csv`.

| Columna | Tipo |
|---|---|
| `tipo` | VARCHAR |
| `acciones` | BIGINT |
| `completadas` | BIGINT |
| `xt_neto` | DOUBLE |
| `xt_positivo` | DOUBLE |

### `liga_f_xt.superficie_xt`

Matriz 8x12 de valor de amenaza por zona del campo. Filas: 8. Clave: sin clave natural. Archivo: `liga-f-xt/datos/salida/superficie_xt.csv`.

| Columna | Tipo |
|---|---|
| `0` | DOUBLE |
| `1` | DOUBLE |
| `2` | DOUBLE |
| `3` | DOUBLE |
| `4` | DOUBLE |
| `5` | DOUBLE |
| `6` | DOUBLE |
| `7` | DOUBLE |
| `8` | DOUBLE |
| `9` | DOUBLE |
| `10` | DOUBLE |
| `11` | DOUBLE |

## `real_zaragoza`

Seguimiento del Real Zaragoza 2026/27 en Primera Federación (grupo 2).
Origen: `analisis/real-zaragoza/datos/salida/`.

### `real_zaragoza.clasificacion`

Clasificación del grupo 2 tras la última jornada, con ranking de ataque y defensa. Filas: 20. Clave: tras_jornada, equipo. Archivo: `real-zaragoza/datos/salida/clasificacion.csv`.

| Columna | Tipo |
|---|---|
| `tras_jornada` | BIGINT |
| `posicion` | BIGINT |
| `equipo` | VARCHAR |
| `pj` | BIGINT |
| `g` | BIGINT |
| `e` | BIGINT |
| `p` | BIGINT |
| `gf` | BIGINT |
| `gc` | BIGINT |
| `puntos` | BIGINT |
| `fuente_url` | VARCHAR |
| `dg` | BIGINT |
| `puntos_por_partido` | DOUBLE |
| `puesto_ataque` | BIGINT |
| `puesto_defensa` | BIGINT |

### `real_zaragoza.goles`

Un gol (a favor o en contra) con minuto, tramo, goleador y datos del partido. Filas: 41. Clave: sin clave natural. Archivo: `real-zaragoza/datos/salida/goles.csv`.

| Columna | Tipo |
|---|---|
| `partido_id` | BIGINT |
| `sentido` | VARCHAR |
| `jugador` | VARCHAR |
| `minuto` | BIGINT |
| `anadido` | BIGINT |
| `parte` | BIGINT |
| `penalti` | BOOLEAN |
| `propia_puerta` | BOOLEAN |
| `asistencia` | VARCHAR |
| `fuente_url` | VARCHAR |
| `minuto_texto` | VARCHAR |
| `tramo` | VARCHAR |
| `rol_goleador` | VARCHAR |
| `competicion` | VARCHAR |
| `jornada` | BIGINT |
| `fecha` | DATE |
| `sede` | VARCHAR |
| `rival` | VARCHAR |

### `real_zaragoza.grupo2_equipos`

Estadísticas avanzadas (xG, tiros, posesión) de los 20 equipos del grupo 2. Filas: 20. Clave: equipo. Archivo: `real-zaragoza/datos/salida/grupo2_equipos.csv`.

| Columna | Tipo |
|---|---|
| `equipo` | VARCHAR |
| `posicion` | BIGINT |
| `pj` | BIGINT |
| `puntos` | BIGINT |
| `gf` | BIGINT |
| `gc` | BIGINT |
| `xpts` | DOUBLE |
| `tiros` | DOUBLE |
| `tiros_contra` | DOUBLE |
| `posesion` | DOUBLE |
| `duelos` | DOUBLE |
| `pj_xg` | BIGINT |
| `puntos_xg` | BIGINT |
| `xg` | DOUBLE |
| `xg_contra` | DOUBLE |
| `gf_xg` | BIGINT |
| `gc_xg` | BIGINT |
| `tiros_xg` | DOUBLE |
| `tiros_contra_xg` | DOUBLE |
| `dentro` | DOUBLE |
| `dg` | BIGINT |
| `xg_pp` | DOUBLE |
| `xg_contra_pp` | DOUBLE |
| `xg_dif_pp` | DOUBLE |
| `eficacia` | DOUBLE |
| `eficacia_def` | DOUBLE |
| `xg_por_tiro` | DOUBLE |
| `xg_por_tiro_contra` | DOUBLE |
| `pct_dentro` | DOUBLE |
| `dif_puntos` | DOUBLE |

### `real_zaragoza.grupo2_equipos_solo_sofascore`

Igual que grupo2_equipos pero solo con partidos de una fuente (control de sensibilidad). Filas: 20. Clave: equipo. Archivo: `real-zaragoza/datos/salida/grupo2_equipos_solo_sofascore.csv`.

| Columna | Tipo |
|---|---|
| `equipo` | VARCHAR |
| `posicion` | BIGINT |
| `pj` | BIGINT |
| `puntos` | BIGINT |
| `gf` | BIGINT |
| `gc` | BIGINT |
| `xpts` | DOUBLE |
| `tiros` | DOUBLE |
| `tiros_contra` | DOUBLE |
| `posesion` | DOUBLE |
| `duelos` | DOUBLE |
| `pj_xg` | BIGINT |
| `puntos_xg` | BIGINT |
| `xg` | DOUBLE |
| `xg_contra` | DOUBLE |
| `gf_xg` | BIGINT |
| `gc_xg` | BIGINT |
| `tiros_xg` | DOUBLE |
| `tiros_contra_xg` | DOUBLE |
| `dentro` | DOUBLE |
| `dg` | BIGINT |
| `xg_pp` | DOUBLE |
| `xg_contra_pp` | DOUBLE |
| `xg_dif_pp` | DOUBLE |
| `eficacia` | DOUBLE |
| `eficacia_def` | DOUBLE |
| `xg_por_tiro` | DOUBLE |
| `xg_por_tiro_contra` | DOUBLE |
| `pct_dentro` | DOUBLE |
| `dif_puntos` | DOUBLE |

### `real_zaragoza.jugadores`

Resumen de temporada por jugador: partidos, minutos, goles y asistencias. Filas: 25. Clave: jugador. Archivo: `real-zaragoza/datos/salida/jugadores.csv`.

| Columna | Tipo |
|---|---|
| `jugador` | VARCHAR |
| `partidos` | BIGINT |
| `titularidades` | BIGINT |
| `minutos` | DOUBLE |
| `goles` | BIGINT |
| `asistencias` | BIGINT |
| `participaciones_con_minutos` | BIGINT |
| `participaciones_por_90` | DOUBLE |
| `minutos_por_participacion` | DOUBLE |

### `real_zaragoza.minutos_partido`

Minutos jugados por cada futbolista en cada partido. Filas: 192. Clave: partido_id, jugador. Archivo: `real-zaragoza/datos/salida/minutos_partido.csv`.

| Columna | Tipo |
|---|---|
| `partido_id` | BIGINT |
| `jugador` | VARCHAR |
| `rol` | VARCHAR |
| `entra` | BIGINT |
| `sale` | DOUBLE |
| `minutos` | DOUBLE |

### `real_zaragoza.participacion_goles`

Goles, asistencias y participaciones de cada jugador. Filas: 12. Clave: jugador. Archivo: `real-zaragoza/datos/salida/participacion_goles.csv`.

| Columna | Tipo |
|---|---|
| `jugador` | VARCHAR |
| `goles` | BIGINT |
| `asistencias` | BIGINT |
| `participaciones` | BIGINT |

### `real_zaragoza.partidos_copa`

Partidos de Copa del Rey del Zaragoza (el identificador empieza en 101). Filas: 1. Clave: partido_id. Archivo: `real-zaragoza/datos/salida/partidos_copa.csv`.

| Columna | Tipo |
|---|---|
| `partido_id` | BIGINT |
| `competicion` | VARCHAR |
| `jornada` | VARCHAR |
| `fecha` | DATE |
| `sede` | VARCHAR |
| `rival` | VARCHAR |
| `goles_favor` | BIGINT |
| `goles_contra` | BIGINT |
| `gf_descanso` | BIGINT |
| `gc_descanso` | BIGINT |
| `fuente_url` | VARCHAR |
| `puntos` | BIGINT |
| `resultado` | VARCHAR |
| `diferencia_goles` | BIGINT |
| `porteria_cero` | BOOLEAN |
| `puntos_acumulados` | VARCHAR |

### `real_zaragoza.partidos_liga`

Un partido de liga del Zaragoza con resultado, puntos, estadísticas del partido y posición del rival. Filas: 12. Clave: partido_id. Archivo: `real-zaragoza/datos/salida/partidos_liga.csv`.

| Columna | Tipo |
|---|---|
| `partido_id` | BIGINT |
| `competicion` | VARCHAR |
| `jornada` | BIGINT |
| `fecha` | DATE |
| `sede` | VARCHAR |
| `rival` | VARCHAR |
| `goles_favor` | BIGINT |
| `goles_contra` | BIGINT |
| `gf_descanso` | BIGINT |
| `gc_descanso` | BIGINT |
| `fuente_url_x` | VARCHAR |
| `puntos` | BIGINT |
| `resultado` | VARCHAR |
| `diferencia_goles` | BIGINT |
| `porteria_cero` | BOOLEAN |
| `puntos_acumulados` | BIGINT |
| `posicion_rival` | BIGINT |
| `tiros_zaragoza` | DOUBLE |
| `tiros_rival` | DOUBLE |
| `a_puerta_zaragoza` | DOUBLE |
| `a_puerta_rival` | DOUBLE |
| `posesion_pct` | DOUBLE |
| `completo` | BOOLEAN |
| `fuente` | VARCHAR |
| `nota` | VARCHAR |
| `fuente_url_y` | VARCHAR |

### `real_zaragoza.proximos`

Próximo partido del Zaragoza, con la posición del rival. Filas: 1. Clave: jornada, competicion. Archivo: `real-zaragoza/datos/salida/proximos.csv`.

| Columna | Tipo |
|---|---|
| `jornada` | BIGINT |
| `competicion` | VARCHAR |
| `fecha` | DATE |
| `sede` | VARCHAR |
| `rival` | VARCHAR |
| `fuente_url` | VARCHAR |
| `posicion_rival` | BIGINT |

### `real_zaragoza.resumen_sede`

Puntos, goles y porterías a cero del Zaragoza en casa y fuera. Filas: 2. Clave: sede. Archivo: `real-zaragoza/datos/salida/resumen_sede.csv`.

| Columna | Tipo |
|---|---|
| `sede` | VARCHAR |
| `partidos` | BIGINT |
| `puntos` | BIGINT |
| `goles_favor` | BIGINT |
| `goles_contra` | BIGINT |
| `porterias_cero` | BIGINT |
| `puntos_por_partido` | DOUBLE |

### `real_zaragoza.video_carril`

Goles por carril de la jugada (a favor y en contra), de la revisión en vídeo. Filas: 4. Clave: carril. Archivo: `real-zaragoza/datos/salida/video/carril.csv`.

| Columna | Tipo |
|---|---|
| `carril` | VARCHAR |
| `Favor` | BIGINT |
| `Contra` | BIGINT |

### `real_zaragoza.video_inicio`

Goles según cómo empezó la jugada (a favor y en contra). Filas: 5. Clave: inicio. Archivo: `real-zaragoza/datos/salida/video/inicio.csv`.

| Columna | Tipo |
|---|---|
| `inicio` | VARCHAR |
| `Favor` | BIGINT |
| `Contra` | BIGINT |

### `real_zaragoza.video_sofascore_partidos`

Métricas del rival por partido (una columna por métrica) recogidas de Sofascore. Filas: 8. Clave: partido_id. Archivo: `real-zaragoza/datos/salida/video/sofascore_partidos.csv`.

| Columna | Tipo |
|---|---|
| `partido_id` | BIGINT |
| `amarillas_rival` | DOUBLE |
| `balones_largos_ok_rival` | DOUBLE |
| `balones_largos_total_rival` | DOUBLE |
| `centros_ok_rival` | DOUBLE |
| `centros_total_rival` | DOUBLE |
| `corners_rival` | DOUBLE |
| `despejes_rival` | DOUBLE |
| `desposeido_rival` | DOUBLE |
| `duelos_aereos_ok_rival` | DOUBLE |
| `duelos_aereos_total_rival` | DOUBLE |
| `duelos_ganados_pct_rival` | DOUBLE |
| `duelos_suelo_ok_rival` | DOUBLE |
| `duelos_suelo_total_rival` | DOUBLE |
| `entradas_rival` | DOUBLE |
| `entradas_ganadas_pct_rival` | DOUBLE |
| `entradas_ultimo_tercio_rival` | DOUBLE |
| `faltas_rival` | DOUBLE |
| `faltas_recibidas_ultimo_tercio_rival` | DOUBLE |
| `fueras_juego_rival` | DOUBLE |
| `goles_evitados_rival` | DOUBLE |
| `intercepciones_rival` | DOUBLE |
| `ocasiones_claras_rival` | DOUBLE |
| `ocasiones_claras_falladas_rival` | DOUBLE |
| `ocasiones_claras_gol_rival` | DOUBLE |
| `palos_rival` | DOUBLE |
| `paradas_rival` | DOUBLE |
| `pases_rival` | DOUBLE |
| `pases_al_hueco_rival` | DOUBLE |
| `pases_buenos_rival` | DOUBLE |
| `pases_ultimo_tercio_rival` | DOUBLE |
| `perdidas_en_conduccion_rival` | DOUBLE |
| `posesion_pct_rival` | DOUBLE |
| `recuperaciones_rival` | DOUBLE |
| `regates_ok_rival` | DOUBLE |
| `regates_total_rival` | DOUBLE |
| `rojas_rival` | DOUBLE |
| `saques_banda_rival` | DOUBLE |
| `saques_meta_rival` | DOUBLE |
| `saques_puerta_rival` | DOUBLE |
| `tiros_rival` | DOUBLE |
| `tiros_a_puerta_rival` | DOUBLE |
| `tiros_al_palo_rival` | DOUBLE |
| `tiros_bloqueados_rival` | DOUBLE |
| `tiros_dentro_area_rival` | DOUBLE |
| `tiros_fuera_rival` | DOUBLE |
| `tiros_fuera_area_rival` | DOUBLE |
| `tiros_libres_rival` | DOUBLE |
| `xg_rival` | DOUBLE |
| `xgot_rival` | DOUBLE |
| `amarillas_zgz` | DOUBLE |
| `balones_largos_ok_zgz` | DOUBLE |
| `balones_largos_total_zgz` | DOUBLE |
| `centros_ok_zgz` | DOUBLE |
| `centros_total_zgz` | DOUBLE |
| `corners_zgz` | DOUBLE |
| `despejes_zgz` | DOUBLE |
| `desposeido_zgz` | DOUBLE |
| `duelos_aereos_ok_zgz` | DOUBLE |
| `duelos_aereos_total_zgz` | DOUBLE |
| `duelos_ganados_pct_zgz` | DOUBLE |
| `duelos_suelo_ok_zgz` | DOUBLE |
| `duelos_suelo_total_zgz` | DOUBLE |
| `entradas_zgz` | DOUBLE |
| `entradas_ganadas_pct_zgz` | DOUBLE |
| `entradas_ultimo_tercio_zgz` | DOUBLE |
| `faltas_zgz` | DOUBLE |
| `faltas_recibidas_ultimo_tercio_zgz` | DOUBLE |
| `fueras_juego_zgz` | DOUBLE |
| `goles_evitados_zgz` | DOUBLE |
| `intercepciones_zgz` | DOUBLE |
| `ocasiones_claras_zgz` | DOUBLE |
| `ocasiones_claras_falladas_zgz` | DOUBLE |
| `ocasiones_claras_gol_zgz` | DOUBLE |
| `palos_zgz` | DOUBLE |
| `paradas_zgz` | DOUBLE |
| `pases_zgz` | DOUBLE |
| `pases_al_hueco_zgz` | DOUBLE |
| `pases_buenos_zgz` | DOUBLE |
| `pases_ultimo_tercio_zgz` | DOUBLE |
| `perdidas_en_conduccion_zgz` | DOUBLE |
| `posesion_pct_zgz` | DOUBLE |
| `recuperaciones_zgz` | DOUBLE |
| `regates_ok_zgz` | DOUBLE |
| `regates_total_zgz` | DOUBLE |
| `rojas_zgz` | DOUBLE |
| `saques_banda_zgz` | DOUBLE |
| `saques_meta_zgz` | DOUBLE |
| `saques_puerta_zgz` | DOUBLE |
| `tiros_zgz` | DOUBLE |
| `tiros_a_puerta_zgz` | DOUBLE |
| `tiros_al_palo_zgz` | DOUBLE |
| `tiros_bloqueados_zgz` | DOUBLE |
| `tiros_dentro_area_zgz` | DOUBLE |
| `tiros_fuera_zgz` | DOUBLE |
| `tiros_fuera_area_zgz` | DOUBLE |
| `tiros_libres_zgz` | DOUBLE |
| `xg_zgz` | DOUBLE |
| `xgot_zgz` | DOUBLE |

### `real_zaragoza.video_ultimo_pase`

Goles según el tipo del último pase (a favor y en contra). Filas: 10. Clave: ultimo_pase. Archivo: `real-zaragoza/datos/salida/video/ultimo_pase.csv`.

| Columna | Tipo |
|---|---|
| `ultimo_pase` | VARCHAR |
| `Favor` | BIGINT |
| `Contra` | BIGINT |

### `real_zaragoza.video_zona_remate`

Goles según la zona del remate (a favor y en contra). Filas: 6. Clave: zona_remate. Archivo: `real-zaragoza/datos/salida/video/zona_remate.csv`.

| Columna | Tipo |
|---|---|
| `zona_remate` | VARCHAR |
| `Favor` | BIGINT |
| `Contra` | BIGINT |

## `comun` (vistas entre proyectos)

- `comun.v_grupo2_actual`: Clasificación del grupo 2 tras la última jornada unida a la simulación (une real_zaragoza y grupo2_simulacion).
