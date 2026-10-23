"""Versión de consola del juego de gestión de fútbol. Conserva el flujo de menús y simulación de la primera implementación; el motor que pruebo automáticamente está en main.py y la versión web vive en index.html."""
"""Versión de consola del juego de gestión de fútbol (sin Pygame)."""
import random
import time
import json
import os

# --- 1. CONFIGURACIÓN TÁCTICA Y CLASES ---

# Cada formación indica cuántos jugadores necesito por línea; todas suman once.
FORMACIONES = {
    "4-4-2": {"POR": 1, "DEF": 4, "CEN": 4, "DEL": 2},
    "4-3-3": {"POR": 1, "DEF": 4, "CEN": 3, "DEL": 3},
    "5-3-2": {"POR": 1, "DEF": 5, "CEN": 3, "DEL": 2},
}

# Los multiplicadores convierten el estilo elegido en ataque, defensa y desgaste físico.
ESTILOS = {
    "Ofensivo": {"ataque": 1.15, "defensa": 0.90, "desgaste": 1.2},
    "Equilibrado": {"ataque": 1.00, "defensa": 1.00, "desgaste": 1.0},
    "Defensivo": {"ataque": 0.85, "defensa": 1.15, "desgaste": 0.9},
}

# Mantengo nombres ficticios con humor y los separo por posición para formar plantillas legibles.
NOMBRES_RIVALES = {
    "POR": ["Iker Guantes", "Marga Parapenaltis", "Paco Manoplas"],
    "DEF": ["Rafa Rechaces", "Blas Banderín", "Tino Tobillo", "Lola Cerrojazo", "Nico Nopuedo"],
    "CEN": ["Pili Pasecorto", "Rolo Rondo", "Mauri MediaVuelta", "Cris Cañito", "Fede FueraJuego"],
    "DEL": ["Golo Goloso", "Rita Remates", "Charly Trallazo", "Tere Taconazo"],
}


class Jugador:
    """Representa a un futbolista ficticio y reúne sus atributos deportivos, físicos y económicos."""
    def __init__(self, nombre, posicion, media, moral=80, cansancio=0, precio=2000000,
                 salario=15000, goles=0, xg_acumulado=0.0, lesionado=0):
        """Creo el jugador con valores de partida; los parámetros opcionales permiten reconstruirlo desde un guardado."""
        self.nombre = nombre
        self.posicion = posicion  # POR, DEF, CEN, DEL
        self.media = media
        self.moral = moral
        self.cansancio = cansancio
        self.precio = precio
        self.salario = salario    # Coste por jornada
        self.goles = goles
        self.xg_acumulado = xg_acumulado
        self.lesionado = lesionado

    def rendimiento_real(self):
        """Calculo el rendimiento disponible hoy: una lesión lo anula y la fatiga y la moral lo ajustan."""
        if self.lesionado > 0:
            return 0
        factor_cansancio = 1 - (self.cansancio / 200)
        factor_moral = self.moral / 100
        return int(self.media * factor_cansancio * factor_moral)

    def to_dict(self):
        """Convierto el estado del jugador a un diccionario sencillo para guardarlo como JSON."""
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, data):
        """Reconstruyo un jugador a partir de los datos previamente guardados."""
        return cls(**data)


class Equipo:
    """Agrupa plantilla, once, táctica, economía y estadísticas acumuladas de un club ficticio."""
    def __init__(self, nombre, presupuesto=12000000, formacion="4-4-2", estilo="Equilibrado", aforo=25000):
        """Inicializo los datos del club y dejo listas vacías para jugadores y alineación."""
        self.nombre = nombre
        self.presupuesto = presupuesto
        self.aforo = aforo
        self.plantilla = []
        self.alineacion_titular = []
        self.formacion = formacion
        self.estilo = estilo
        self.puntos = 0
        self.goles_a_favor = 0
        self.goles_en_contra = 0
        self.xg_favor = 0.0
        self.xg_contra = 0.0
        self.partidos_jugados = 0

    def agregar_jugador(self, jugador):
        """Añado un futbolista a la plantilla del equipo."""
        self.plantilla.append(jugador)

    def masa_salarial_jornada(self):
        """Sumo los salarios de todos los jugadores para conocer el gasto de una jornada."""
        return sum(j.salario for j in self.plantilla)

    def convocar_once_automatico(self):
        """Selecciono los mejores jugadores disponibles por posición y completo los puestos vacíos con el resto."""
        esquema = FORMACIONES[self.formacion]
        disponibles = [j for j in self.plantilla if j.lesionado == 0]
        titulares = []

        for pos, cantidad in esquema.items():
            candidatos = [j for j in disponibles if j.posicion == pos]
            candidatos.sort(key=lambda j: j.rendimiento_real(), reverse=True)
            seleccionados = candidatos[:cantidad]
            titulares.extend(seleccionados)
            for s in seleccionados:
                disponibles.remove(s)

        # Si faltan efectivos en alguna línea, rellenar con los mejores disponibles
        while len(titulares) < 11 and disponibles:
            disponibles.sort(key=lambda j: j.rendimiento_real(), reverse=True)
            titulares.append(disponibles.pop(0))

        self.alineacion_titular = titulares

    def calcular_fuerzas(self):
        """Obtengo ataque y defensa a partir del once, su rendimiento actual y los multiplicadores del estilo."""
        if len(self.alineacion_titular) < 11 or any(j.lesionado > 0 for j in self.alineacion_titular):
            self.convocar_once_automatico()
        if not self.alineacion_titular:
            return 50, 50

        media_base = sum(j.rendimiento_real() for j in self.alineacion_titular) / len(self.alineacion_titular)
        mod = ESTILOS[self.estilo]
        return media_base * mod["ataque"], media_base * mod["defensa"]

    def reiniciar_estadisticas_liga(self):
        """Borro los datos que pertenecen a la competición anterior y recupero a la plantilla para empezar otra temporada."""
        self.puntos = 0
        self.goles_a_favor = 0
        self.goles_en_contra = 0
        self.xg_favor = 0.0
        self.xg_contra = 0.0
        self.partidos_jugados = 0
        for j in self.plantilla:
            j.goles = 0
            j.xg_acumulado = 0.0
            j.cansancio = 0
            j.lesionado = 0

    def to_dict(self):
        """Serializo el equipo, su plantilla y los nombres del once para conservar también la alineación manual."""
        return {
            "nombre": self.nombre,
            "presupuesto": self.presupuesto,
            "aforo": self.aforo,
            "formacion": self.formacion,
            "estilo": self.estilo,
            "puntos": self.puntos,
            "goles_a_favor": self.goles_a_favor,
            "goles_en_contra": self.goles_en_contra,
            "xg_favor": round(self.xg_favor, 2),
            "xg_contra": round(self.xg_contra, 2),
            "partidos_jugados": self.partidos_jugados,
            "plantilla": [j.to_dict() for j in self.plantilla],
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruyo el club y enlazo los nombres guardados con los objetos de jugador creados."""
        eq = cls(data["nombre"], data["presupuesto"], data["formacion"], data["estilo"], data.get("aforo", 25000))
        eq.puntos = data["puntos"]
        eq.goles_a_favor = data["goles_a_favor"]
        eq.goles_en_contra = data["goles_en_contra"]
        eq.xg_favor = data.get("xg_favor", 0.0)
        eq.xg_contra = data.get("xg_contra", 0.0)
        eq.partidos_jugados = data["partidos_jugados"]
        eq.plantilla = [Jugador.from_dict(j) for j in data["plantilla"]]
        eq.convocar_once_automatico()
        return eq


# --- 2. MOTOR DE SIMULACIÓN CON xG, POSESIÓN Y FINANZAS ---

def elegir_rematador(alineacion):
    """Elijo quién finaliza la jugada dando más peso a los delanteros y menos a defensas y centrocampistas."""
    pesos = {"DEL": 55, "CEN": 30, "DEF": 14}
    return random.choices(alineacion, weights=[pesos.get(j.posicion, 1) for j in alineacion], k=1)[0]


def generar_ocasion_xg(atq, dfn):
    """Genera el tipo de ocasión y su valor xG según la superioridad ofensiva."""
    ratio = atq / (atq + dfn)  # En torno a 0.50 en duelos igualados
    tiro_tipo = random.random()

    if tiro_tipo < 0.18 * (ratio * 2):
        return "Ocasión clara dentro del área", round(random.uniform(0.32, 0.55), 2)
    elif tiro_tipo < 0.55:
        return "Remate desde posición media", round(random.uniform(0.10, 0.25), 2)
    else:
        return "Disparo lejano o forzado", round(random.uniform(0.03, 0.09), 2)


def simular_partido(local, visitante, mostrar_detalle=True):
    """Simulo las fases del encuentro y actualizo marcador, xG, puntos, economía, cansancio y lesiones."""
    if mostrar_detalle:
        print(f"\n⚽ ¡PARTIDO: {local.nombre} ({local.formacion}) vs {visitante.nombre} ({visitante.formacion})!")

    atq_local, def_local = local.calcular_fuerzas()
    atq_vis, def_vis = visitante.calcular_fuerzas()

    # Factor campo (+3 para el local)
    atq_local += 3
    def_local += 3

    posesion_local = int(round((atq_local / (atq_local + atq_vis)) * 100))
    posesion_vis = 100 - posesion_local

    goles_local, goles_vis = 0, 0
    tiros_local, tiros_vis = 0, 0
    xg_partido_local, xg_partido_vis = 0.0, 0.0

    # 8 tramos de partido para generar un volumen realista de tiros y xG
    for minuto in [10, 22, 35, 45, 55, 68, 80, 90]:
        # Probabilidad de que haya un tiro en este tramo (80%)
        if random.random() < 0.80:
            if random.random() < (atq_local / (atq_local + atq_vis)):
                tiros_local += 1
                rematador = elegir_rematador(local.alineacion_titular)
                desc, xg_tiro = generar_ocasion_xg(atq_local, def_vis)
                # Ajuste por calidad individual del rematador
                prob_gol = min(0.85, xg_tiro * (rematador.rendimiento_real() / 72))

                xg_partido_local += xg_tiro
                rematador.xg_acumulado = round(rematador.xg_acumulado + xg_tiro, 2)

                if random.random() < prob_gol:
                    goles_local += 1
                    rematador.goles += 1
                    if mostrar_detalle:
                        print(f"[{minuto}'] ¡GOOOOL de {rematador.nombre} ({local.nombre})! [{desc} | xG: {xg_tiro:.2f}] ⚽")
                elif mostrar_detalle and xg_tiro >= 0.30:
                    print(f"[{minuto}'] ¡Uy! {rematador.nombre} ({local.nombre}) falla una ocasión clara (xG: {xg_tiro:.2f}).")
            else:
                tiros_vis += 1
                rematador = elegir_rematador(visitante.alineacion_titular)
                desc, xg_tiro = generar_ocasion_xg(atq_vis, def_local)
                prob_gol = min(0.85, xg_tiro * (rematador.rendimiento_real() / 72))

                xg_partido_vis += xg_tiro
                rematador.xg_acumulado = round(rematador.xg_acumulado + xg_tiro, 2)

                if random.random() < prob_gol:
                    goles_vis += 1
                    rematador.goles += 1
                    if mostrar_detalle:
                        print(f"[{minuto}'] ¡GOOOOL de {rematador.nombre} ({visitante.nombre})! [{desc} | xG: {xg_tiro:.2f}] ⚽")
                elif mostrar_detalle and xg_tiro >= 0.30:
                    print(f"[{minuto}'] ¡Paradón! {rematador.nombre} ({visitante.nombre}) perdona una clara (xG: {xg_tiro:.2f}).")
        if mostrar_detalle:
            time.sleep(0.15)

    # Actualizar estadísticas del club
    local.partidos_jugados += 1
    visitante.partidos_jugados += 1
    local.goles_a_favor += goles_local
    local.goles_en_contra += goles_vis
    visitante.goles_a_favor += goles_vis
    visitante.goles_en_contra += goles_local

    local.xg_favor = round(local.xg_favor + xg_partido_local, 2)
    local.xg_contra = round(local.xg_contra + xg_partido_vis, 2)
    visitante.xg_favor = round(visitante.xg_favor + xg_partido_vis, 2)
    visitante.xg_contra = round(visitante.xg_contra + xg_partido_local, 2)

    if goles_local > goles_vis:
        local.puntos += 3
    elif goles_local < goles_vis:
        visitante.puntos += 3
    else:
        local.puntos += 1
        visitante.puntos += 1

    # Economía: taquilla para el local y salarios en ambos clubes
    asistencia = int(local.aforo * random.uniform(0.70, 0.95))
    recaudacion = asistencia * 20  # 20€ entrada media
    local.presupuesto += recaudacion

    salarios_loc = local.masa_salarial_jornada()
    salarios_vis = visitante.masa_salarial_jornada()
    local.presupuesto -= salarios_loc
    visitante.presupuesto -= salarios_vis

    if mostrar_detalle:
        print("-" * 62)
        print(f"🏁 FINAL: {local.nombre} {goles_local} - {goles_vis} {visitante.nombre}")
        print(f"📊 Estadísticas | Posesión: {posesion_local}% - {posesion_vis}% | Tiros: {tiros_local} - {tiros_vis} | xG: {xg_partido_local:.2f} - {xg_partido_vis:.2f}")
        print(f"💶 Taquilla {local.nombre}: +{recaudacion:,} € ({asistencia:,} espect.) | Salarios pagados: -{salarios_loc:,} €")
        print("-" * 62)

    # Gestión de fatiga y lesiones
    for eq in [local, visitante]:
        for j in eq.plantilla:
            if j not in eq.alineacion_titular and j.lesionado > 0:
                j.lesionado -= 1
        mult_desgaste = ESTILOS[eq.estilo]["desgaste"]
        for j in eq.alineacion_titular:
            j.cansancio = min(100, j.cansancio + int(random.randint(14, 24) * mult_desgaste))
            if random.random() < (0.12 if j.cansancio > 75 else 0.02):
                j.lesionado = random.randint(1, 3)
                if mostrar_detalle:
                    print(f"🚑 Lesión: {j.nombre} ({eq.nombre}) estará {j.lesionado} jornada(s) de baja.")


# --- 3. MENÚS DE PLANTILLA (CON CAMBIOS MANUALES), MERCADO (COMPRA/VENTA) Y TABLAS ---

def menu_tactica_y_plantilla(equipo):
    """Muestro la gestión del once y permito cambiar jugadores, formación o estilo desde la consola."""
    if not equipo.alineacion_titular:
        equipo.convocar_once_automatico()

    while True:
        print(f"\n--- GESTIÓN DE {equipo.nombre.upper()} ---")
        print(f"Esquema: {equipo.formacion} | Estilo: {equipo.estilo} | Masa Salarial: {equipo.masa_salarial_jornada():,} €/jornada")
        print(f"{'No.':<3} {'Nombre':<16} {'Pos':<4} {'Med':<4} {'Rend':<5} {'Cans':<5} {'Goles':<5} {'xG':<6} {'Estado'}")
        print("-" * 68)
        for i, j in enumerate(equipo.plantilla):
            es_titular = j in equipo.alineacion_titular
            marca = "*" if es_titular else " "
            estado = f"Baja ({j.lesionado}j)" if j.lesionado > 0 else ("Titular" if es_titular else "Suplente")
            print(f"{i+1:<2}{marca} {j.nombre:<16} {j.posicion:<4} {j.media:<4} {j.rendimiento_real():<5} {j.cansancio:<4}% {j.goles:<5} {j.xg_acumulado:<6.2f} {estado}")

        print("\nOpciones:")
        print("1. Sustituir jugador manualmente en el once (Titular <-> Suplente)")
        print("2. Auto-convocar mejor once según esquema")
        print("3. Cambiar Formación (4-4-2, 4-3-3, 5-3-2)")
        print("4. Cambiar Estilo (Ofensivo, Equilibrado, Defensivo)")
        print("5. Volver")

        op = input("Elige una opción: ")
        # Al simular una jornada, se juegan también los encuentros entre rivales
        # para mantener una clasificación completa, no solo el partido del usuario.
        if op == "1":
            try:
                id_out = int(input("Número del jugador TITULAR que sale: ")) - 1
                id_in = int(input("Número del jugador SUPLENTE que entra: ")) - 1
            except ValueError:
                print("❌ Introduce números válidos.")
                continue
            if 0 <= id_out < len(equipo.plantilla) and 0 <= id_in < len(equipo.plantilla):
                j_out = equipo.plantilla[id_out]
                j_in = equipo.plantilla[id_in]
                if j_out not in equipo.alineacion_titular:
                    print("❌ El primer jugador elegido no está en el once titular.")
                elif j_in in equipo.alineacion_titular:
                    print("❌ El segundo jugador ya es titular.")
                elif j_in.lesionado > 0:
                    print("❌ No puedes alinear a un jugador lesionado.")
                else:
                    equipo.alineacion_titular.remove(j_out)
                    equipo.alineacion_titular.append(j_in)
                    print(f"🔄 Cambio realizado: Entra {j_in.nombre} por {j_out.nombre}.")
            else:
                print("❌ Número fuera de rango.")
        elif op == "2":
            equipo.convocar_once_automatico()
            print("✅ Once titular reordenado automáticamente.")
        elif op == "3":
            f = input("Formación (4-4-2 / 4-3-3 / 5-3-2): ").strip()
            if f in FORMACIONES:
                equipo.formacion = f
                equipo.convocar_once_automatico()
                print(f"✅ Formación cambiada a {f}.")
            else:
                print("❌ Formación no reconocida.")
        elif op == "4":
            e = input("Estilo (Ofensivo / Equilibrado / Defensivo): ").strip().capitalize()
            if e in ESTILOS:
                equipo.estilo = e
                print(f"✅ Estilo cambiado a {e}.")
            else:
                print("❌ Estilo no reconocido.")
        elif op == "5":
            break
        else:
            print("Opción no válida.")


def mostrar_mercado(equipo, mercado_disponible):
    """Presento el mercado y proceso compras y ventas comprobando índices y presupuesto disponible."""
    while True:
        print(f"\n--- MERCADO Y FINANZAS ({equipo.nombre}) ---")
        print(f"Presupuesto: {equipo.presupuesto:,} € | Salarios por jornada: {equipo.masa_salarial_jornada():,} €")
        print("\nJugadores en el mercado para COMPRAR:")
        for i, j in enumerate(mercado_disponible):
            print(f"  {i+1}. {j.nombre:<16} | {j.posicion} | Media: {j.media} | Precio: {j.precio:,} € | Sueldo: {j.salario:,} €/j")

        print("\nOpciones:")
        print("1. Comprar jugador del mercado")
        print("2. Vender jugador de mi plantilla (Recibes el 80% de su valor)")
        print("3. Volver")

        op = input("Elige una opción: ")
        if op == "1":
            try:
                idx = int(input("Número del jugador a comprar: ")) - 1
            except ValueError:
                print("❌ Entrada no válida.")
                continue
            if 0 <= idx < len(mercado_disponible):
                jug = mercado_disponible[idx]
                if equipo.presupuesto >= jug.precio:
                    equipo.presupuesto -= jug.precio
                    equipo.agregar_jugador(jug)
                    mercado_disponible.pop(idx)
                    print(f"✅ ¡Has fichado a {jug.nombre}!")
                else:
                    print("❌ Presupuesto insuficiente.")
            else:
                print("❌ Número fuera de rango.")
        elif op == "2":
            if len(equipo.plantilla) <= 11:
                print("❌ No puedes vender jugadores si te quedas con menos de 11 efectivos.")
                continue
            for i, j in enumerate(equipo.plantilla):
                valor_venta = int(j.precio * 0.8)
                print(f"  {i+1}. {j.nombre:<16} ({j.posicion}, Media {j.media}) -> Venta: {valor_venta:,} €")
            try:
                idx = int(input("Número del jugador a vender (0 para cancelar): ")) - 1
            except ValueError:
                print("❌ Entrada no válida.")
                continue
            if 0 <= idx < len(equipo.plantilla):
                jug = equipo.plantilla.pop(idx)
                if jug in equipo.alineacion_titular:
                    equipo.alineacion_titular.remove(jug)
                ingreso = int(jug.precio * 0.8)
                equipo.presupuesto += ingreso
                mercado_disponible.append(jug)
                print(f"💶 Has vendido a {jug.nombre} por {ingreso:,} €.")
            elif idx != -1:
                print("❌ Número fuera de rango.")
        elif op == "3":
            break
        else:
            print("Opción no válida.")


def ordenar_clasificacion(equipos):
    """Ordeno la liga por puntos, diferencia de goles, goles a favor y nombre para desempates estables."""
    return sorted(equipos, key=lambda eq: (
        -eq.puntos,
        -(eq.goles_a_favor - eq.goles_en_contra),
        -eq.goles_a_favor,
        eq.nombre.casefold(),
    ))


def mostrar_clasificacion_y_metricas(equipos):
    """Ordeno los equipos y comparo resultados, xG y producción goleadora de los jugadores."""
    print("\n" + "=" * 72)
    print(f"{'CLASIFICACIÓN LIGA + MÉTRICAS xG':^72}")
    print("=" * 72)
    print(f"{'Pos':<4} {'Equipo':<18} {'PTS':<5} {'PJ':<4} {'GF':<4} {'GC':<4} {'DG':<5} {'xG':<6} {'xGA':<6} {'G - xG'}")
    print("-" * 72)
    ordenados = ordenar_clasificacion(equipos)
    for i, eq in enumerate(ordenados):
        dg = eq.goles_a_favor - eq.goles_en_contra
        diff_xg = eq.goles_a_favor - eq.xg_favor
        print(f"{i+1:<4} {eq.nombre:<18} {eq.puntos:<5} {eq.partidos_jugados:<4} {eq.goles_a_favor:<4} {eq.goles_en_contra:<4} {dg:<+5d} {eq.xg_favor:<6.2f} {eq.xg_contra:<6.2f} {diff_xg:<+6.2f}")
    print("=" * 72)

    print(f"\n{'RANKING GOLEADORES (Goles vs xG)':^55}")
    print("-" * 55)
    todos = [(j, eq.nombre) for eq in equipos for j in eq.plantilla if j.goles > 0 or j.xg_acumulado >= 0.5]
    todos.sort(key=lambda x: (x[0].goles, x[0].xg_acumulado), reverse=True)
    print(f"{'Jugador':<18} {'Equipo':<18} {'Goles':<6} {'xG':<6} {'Dif'}")
    for jug, eq_nom in todos[:8]:
        dif = jug.goles - jug.xg_acumulado
        print(f"{jug.nombre:<18} {eq_nom:<18} {jug.goles:<6} {jug.xg_acumulado:<6.2f} {dif:+5.2f}")


# --- 4. CENTRO TÉCNICO, GUARDADO Y CAMBIO DE TEMPORADA ---

def centro_tecnico(equipo):
    """Aplico una acción de descanso o entrenamiento a la plantilla y limito los cambios a valores razonables."""
    print("\n--- CENTRO TÉCNICO ---")
    print("1. Descansar plantilla (-30% cansancio, +10 moral)")
    print("2. Entrenamiento táctico (+15% cansancio, opción de subir media)")
    op = input("Elige una opción (Enter para cancelar): ")
    if op == "1":
        for j in equipo.plantilla:
            j.cansancio = max(0, j.cansancio - 30)
            j.moral = min(100, j.moral + 10)
        print("💤 La plantilla ha descansado.")
    elif op == "2":
        for j in equipo.plantilla:
            if j.lesionado == 0:
                j.cansancio = min(100, j.cansancio + 15)
                if random.random() < 0.18 and j.media < 92:
                    j.media += 1
                    print(f"⭐ ¡{j.nombre} mejora su media a {j.media}!")
        print("💪 Sesión de entrenamiento completada.")


def generar_calendario_nombres(nombres_equipos):
    """Creo una liga a doble vuelta con el método de rotación; la vuelta invierte la localía de cada cruce."""
    n = len(nombres_equipos)  # se asume número par de equipos
    l = nombres_equipos[:]
    ida = []
    for _ in range(n - 1):
        ida.append([(l[i], l[n - 1 - i]) for i in range(n // 2)])
        l = [l[0]] + [l[-1]] + l[1:-1]
    vuelta = [[(vis, loc) for loc, vis in j] for j in ida]
    return ida + vuelta


def guardar_partida(archivo, temporada, jornada_actual, equipos, mercado, calendario):
    """Convierto equipos y mercado a JSON legible y escribo la partida en la ruta indicada."""
    datos = {
        "temporada": temporada,
        "jornada_actual": jornada_actual,
        "equipos": [e.to_dict() for e in equipos],
        "mercado": [j.to_dict() for j in mercado],
        "calendario": calendario,
    }
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"💾 Partida guardada en '{archivo}'.")


def cargar_partida(archivo):
    """Leo el JSON, valido su estructura antes de reconstruir los objetos y devuelvo el estado de la temporada."""
    if not os.path.exists(archivo):
        print("❌ No hay archivo de guardado.")
        return None
    with open(archivo, "r", encoding="utf-8") as f:
        d = json.load(f)
    equipos = [Equipo.from_dict(e) for e in d["equipos"]]
    mercado = [Jugador.from_dict(j) for j in d["mercado"]]
    return d.get("temporada", 1), d["jornada_actual"], equipos, mercado, d["calendario"]


# --- 5. INICIALIZACIÓN Y BUCLE MULTITEMPORADA ---

def crear_plantilla_base(equipo, es_usuario=False):
    """Creo una plantilla inicial: nombres humorísticos propios para el usuario y nombres diferenciados para los rivales."""
    if es_usuario:
        base = [
            ("Paco Manoplas", "POR", 72), ("Rafa Rechaces", "DEF", 75), ("Tino Tobillo", "DEF", 73),
            ("Blas Banderín", "DEF", 71), ("Lola Cerrojazo", "DEF", 72), ("Nico Nopuedo", "DEF", 70),
            ("Pili Pasecorto", "CEN", 77), ("Rolo Rondo", "CEN", 75), ("Mauri MediaVuelta", "CEN", 76),
            ("Cris Cañito", "CEN", 74), ("Fede FueraJuego", "CEN", 70), ("Golo Goloso", "DEL", 74),
            ("Rita Remates", "DEL", 75), ("Charly Trallazo", "DEL", 73),
        ]
        for nom, pos, med in base:
            equipo.agregar_jugador(Jugador(nom, pos, med, precio=med * 35000, salario=med * 220))
    else:
        posiciones = ["POR"] + ["DEF"] * 5 + ["CEN"] * 5 + ["DEL"] * 3
        contadores = {pos: 0 for pos in NOMBRES_RIVALES}
        apodo = equipo.nombre.split()[0]
        for pos in posiciones:
            med = random.randint(70, 75)
            nombres = NOMBRES_RIVALES[pos]
            nombre = f"{nombres[contadores[pos] % len(nombres)]} ({apodo})"
            contadores[pos] += 1
            equipo.agregar_jugador(Jugador(nombre, pos, med, precio=med * 35000, salario=med * 200))


if __name__ == "__main__":
    # Esta parte solo se ejecuta al abrir el archivo directamente, no al importarlo
    # desde las pruebas. Primero preparo el estado inicial y después entro en el menú.
    ARCHIVO_SAVE = "partida_guardada.json"
    temporada = 1

    # El club jugable y los tres rivales comparten las mismas clases y reglas.
    mi_equipo = Equipo("FC Pase y Pifia", presupuesto=8000000, aforo=30000)
    crear_plantilla_base(mi_equipo, es_usuario=True)
    mi_equipo.convocar_once_automatico()

    rivales = [Equipo("Atlético Siestense", aforo=9000), Equipo("Unión Deportiva Patapalo", aforo=22000), Equipo("Deportivo Balón Perdido", aforo=29000)]
    for r in rivales:
        crear_plantilla_base(r, es_usuario=False)
        r.convocar_once_automatico()

    lista_equipos = [mi_equipo] + rivales

    mercado = [
        Jugador("Crispín Chutapiedras", "CEN", 76, precio=2800000, salario=18000),
        Jugador("Pipo Puntería", "CEN", 76, precio=3000000, salario=19000),
        Jugador("Tere Taconazo", "DEL", 74, precio=2200000, salario=15000),
        Jugador("Benito Banderazo", "DEF", 74, precio=2100000, salario=14500),
    ]

    # El calendario contiene seis jornadas; jornada_actual apunta a la siguiente
    # que queda por disputar, así que también sirve para reanudar una partida.
    calendario = generar_calendario_nombres([e.nombre for e in lista_equipos])
    jornada_actual = 0

    # Bucle de la carrera: mostrar estado, pedir una acción y modificar solo lo
    # necesario. Cuando se completan las jornadas, se ofrecen premios y otra campaña.
    while True:
        mapa_equipos = {e.nombre: e for e in lista_equipos}
        mi_equipo = mapa_equipos["FC Pase y Pifia"]

        # El cierre se ejecuta una sola vez antes de permitir avanzar de temporada.
        if jornada_actual >= len(calendario):
            print(f"\n🏆 ¡FIN DE LA TEMPORADA {temporada}!")
            mostrar_clasificacion_y_metricas(lista_equipos)

            # Premios por clasificación final
            ordenados = ordenar_clasificacion(lista_equipos)
            premios = [5000000, 3500000, 2500000, 1500000]
            for idx, eq in enumerate(ordenados):
                premio = premios[idx] if idx < len(premios) else 1000000
                eq.presupuesto += premio
                if eq == mi_equipo:
                    print(f"\n💶 Has terminado en {idx+1}ª posición. Recibes un premio de {premio:,} € para la próxima campaña.")

            cont = input("\n¿Quieres iniciar la siguiente temporada conservando tu plantilla y presupuesto? (s/n): ").strip().lower()
            if cont == "s":
                temporada += 1
                jornada_actual = 0
                for eq in lista_equipos:
                    eq.reiniciar_estadisticas_liga()
                calendario = generar_calendario_nombres([e.nombre for e in lista_equipos])
                continue
            else:
                break

        print(f"\n========== TEMPORADA {temporada} | JORNADA {jornada_actual + 1} de {len(calendario)} ==========")
        for loc_nom, vis_nom in calendario[jornada_actual]:
            print(f"  • {loc_nom} vs {vis_nom}")

        print(f"\nPresupuesto: {mi_equipo.presupuesto:,} €")
        print("1. Jugar Jornada")
        print("2. Clasificación, Tabla xG y Goleadores")
        print("3. Plantilla, Táctica y Cambios Manuales")
        print("4. Mercado y Finanzas (Comprar / Vender)")
        print("5. Centro Técnico (Entrenar / Descansar)")
        print("6. Guardar Partida")
        print("7. Cargar Partida")
        print("8. Salir")

        # Cada opción delega en una función concreta para que el bucle principal
        # coordine el flujo sin mezclar aquí la lógica de cada pantalla.
        op = input("Selecciona una opción: ")
        if op == "1":
            for loc_nom, vis_nom in calendario[jornada_actual]:
                es_mi_partido = mi_equipo.nombre in (loc_nom, vis_nom)
                simular_partido(mapa_equipos[loc_nom], mapa_equipos[vis_nom], mostrar_detalle=es_mi_partido)
            jornada_actual += 1
        elif op == "2":
            mostrar_clasificacion_y_metricas(lista_equipos)
        elif op == "3":
            menu_tactica_y_plantilla(mi_equipo)
        elif op == "4":
            mostrar_mercado(mi_equipo, mercado)
        elif op == "5":
            centro_tecnico(mi_equipo)
        elif op == "6":
            guardar_partida(ARCHIVO_SAVE, temporada, jornada_actual, lista_equipos, mercado, calendario)
        elif op == "7":
            cargado = cargar_partida(ARCHIVO_SAVE)
            if cargado:
                temporada, jornada_actual, lista_equipos, mercado, calendario = cargado
        elif op == "8":
            break
        else:
            print("Opción no válida.")
