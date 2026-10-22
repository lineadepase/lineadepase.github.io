"""Versión de consola del juego de gestión de fútbol (sin Pygame)."""
import random
import time


# --- 1. ESTRUCTURA DE DATOS Y CLASES BÁSICAS ---

class Jugador:
    def __init__(self, nombre, posicion, media, moral=80, cansancio=0):
        self.nombre = nombre
        self.posicion = posicion  # POR, DEF, CEN, DEL
        self.media = media        # De 1 a 100
        self.moral = moral        # De 0 a 100
        self.cansancio = cansancio  # De 0 a 100 (a mayor cansancio, menor rendimiento)

    def rendimiento_real(self):
        # El rendimiento baja si hay cansancio y sube/baja según la moral
        factor_cansancio = 1 - (self.cansancio / 200)
        factor_moral = self.moral / 100
        return int(self.media * factor_cansancio * factor_moral)


class Equipo:
    def __init__(self, nombre, presupuesto=10000000):
        self.nombre = nombre
        self.presupuesto = presupuesto
        self.plantilla = []
        self.alineacion_titular = []
        self.puntos = 0
        self.goles_a_favor = 0
        self.goles_en_contra = 0
        self.partidos_jugados = 0

    def agregar_jugador(self, jugador):
        self.plantilla.append(jugador)

    def convocar_once_automatico(self):
        """Selecciona el mejor once disponible basado en el rendimiento."""
        ordenados = sorted(self.plantilla, key=lambda j: j.rendimiento_real(), reverse=True)
        self.alineacion_titular = ordenados[:11]

    def calcular_fuerza_equipo(self):
        if not self.alineacion_titular:
            self.convocar_once_automatico()
        return sum(j.rendimiento_real() for j in self.alineacion_titular) / len(self.alineacion_titular)


# --- 2. GESTIÓN DE PLANTILLA Y MENÚ PRINCIPAL ---

def gestionar_plantilla(equipo):
    while True:
        print(f"\n--- PLANTILLA DE {equipo.nombre.upper()} ---")
        print(f"{'No.':<4} {'Nombre':<20} {'Pos':<5} {'Media':<7} {'Moral':<7} {'Cansancio'}")
        print("-" * 55)
        for i, j in enumerate(equipo.plantilla):
            print(f"{i+1:<4} {j.nombre:<20} {j.posicion:<5} {j.media:<7} {j.moral:<7} {j.cansancio}%")

        print("\nOpciones:")
        print("1. Ver once titular actual")
        print("2. Auto-convocar mejor once")
        print("3. Volver al menú principal")

        opcion = input("Elige una opción: ")
        if opcion == "1":
            print("\n--- ONCE TITULAR ---")
            for j in equipo.alineacion_titular:
                print(f"- {j.nombre} ({j.posicion}) | Media: {j.media} | Rendimiento: {j.rendimiento_real()}")
            input("\nPresiona Enter para continuar...")
        elif opcion == "2":
            equipo.convocar_once_automatico()
            print("¡Once titular actualizado con los jugadores en mejor forma!")
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")


# --- 3. MOTOR DE SIMULACIÓN DE PARTIDOS ---

def simular_partido(equipo_local, equipo_visitante):
    print(f"\n⚽ ¡COMIENZA EL PARTIDO: {equipo_local.nombre} vs {equipo_visitante.nombre}!")
    time.sleep(1)

    fuerza_local = equipo_local.calcular_fuerza_equipo() + 3  # Factor campo
    fuerza_visitante = equipo_visitante.calcular_fuerza_equipo()

    goles_local = 0
    goles_visitante = 0

    # Simulación por eventos (minutos clave)
    for minuto in [15, 30, 45, 60, 75, 90]:
        print(f"[{minuto}'] Rodando el balón...")

        # Probabilidad de ocasión basada en la fuerza relativa
        if random.random() < fuerza_local / (fuerza_local + fuerza_visitante):
            if random.random() < 0.35:  # Probabilidad de acierto en la ocasión
                goles_local += 1
                print(f"   GOOOOOOL de {equipo_local.nombre}! ⚽")
        else:
            if random.random() < 0.35:
                goles_visitante += 1
                print(f"   GOOOOOOL de {equipo_visitante.nombre}! ⚽")

        time.sleep(0.5)

    # Actualizar estadísticas de la liga
    equipo_local.partidos_jugados += 1
    equipo_visitante.partidos_jugados += 1

    equipo_local.goles_a_favor += goles_local
    equipo_local.goles_en_contra += goles_visitante
    equipo_visitante.goles_a_favor += goles_visitante
    equipo_visitante.goles_en_contra += goles_local

    marcador = f"{equipo_local.nombre} {goles_local} - {goles_visitante} {equipo_visitante.nombre}"
    if goles_local > goles_visitante:
        equipo_local.puntos += 3
        resultado_str = f"Victoria local: {marcador}"
    elif goles_local < goles_visitante:
        equipo_visitante.puntos += 3
        resultado_str = f"Victoria visitante: {marcador}"
    else:
        equipo_local.puntos += 1
        equipo_visitante.puntos += 1
        resultado_str = f"Empate: {marcador}"

    print(f"\n🏁 ¡FINAL DEL PARTIDO!\nResultado Final: {resultado_str}\n")

    # Desgaste post-partido de los jugadores
    for j in equipo_local.alineacion_titular + equipo_visitante.alineacion_titular:
        j.cansancio = min(100, j.cansancio + random.randint(15, 30))


# --- 4. BUCLE DE TEMPORADA / CLASIFICACIÓN ---

def mostrar_clasificacion(equipos):
    print("\n" + "=" * 45)
    print(f"{'CLASIFICACIÓN LIGA':^45}")
    print("=" * 45)
    print(f"{'Pos':<4} {'Equipo':<20} {'PTS':<5} {'PJ':<5} {'GF':<5} {'GC'}")
    print("-" * 45)

    # Ordenar por puntos y luego por diferencia de goles
    ordenados = sorted(equipos, key=lambda e: (e.puntos, e.goles_a_favor - e.goles_en_contra), reverse=True)

    for i, eq in enumerate(ordenados):
        print(f"{i+1:<4} {eq.nombre:<20} {eq.puntos:<5} {eq.partidos_jugados:<5} {eq.goles_a_favor:<5} {eq.goles_en_contra}")
    print("=" * 45)


# --- EJEMPLO DE PRUEBA / FLUJO PRINCIPAL ---
if __name__ == "__main__":
    mi_equipo = Equipo("Real Zaragoza")
    mi_equipo.agregar_jugador(Jugador("Poussin", "POR", 72))
    mi_equipo.agregar_jugador(Jugador("Alejandro Francés", "DEF", 75))
    mi_equipo.agregar_jugador(Jugador("Gisain", "DEF", 73))
    mi_equipo.agregar_jugador(Jugador("Maikel Mesa", "CEN", 76))
    mi_equipo.agregar_jugador(Jugador("Francho", "CEN", 77))
    mi_equipo.agregar_jugador(Jugador("Valera", "DEL", 74))
    for i in range(1, 6):
        mi_equipo.agregar_jugador(Jugador(f"jugador_{i}", "CEN", 70))

    rival = Equipo("SD Huesca")
    rival.agregar_jugador(Jugador("Fernández", "POR", 71))
    rival.agregar_jugador(Jugador("Pulido", "DEF", 74))
    rival.agregar_jugador(Jugador("Martínez", "DEF", 72))
    rival.agregar_jugador(Jugador("Sielva", "CEN", 75))
    rival.agregar_jugador(Jugador("Javi M.", "CEN", 73))
    rival.agregar_jugador(Jugador("Obeng", "DEL", 74))
    for i in range(1, 6):
        rival.agregar_jugador(Jugador(f"rival_jug_{i}", "DEF", 69))

    lista_equipos = [mi_equipo, rival]

    while True:
        print(f"\n--- MENÚ PRINCIPAL: {mi_equipo.nombre} ---")
        print("1. Ver Clasificación")
        print("2. Gestionar Plantilla / Alineación")
        print(f"3. Jugar Siguiente Partido (contra {rival.nombre})")
        print("4. Salir")

        op = input("Selecciona una opción: ")
        if op == "1":
            mostrar_clasificacion(lista_equipos)
        elif op == "2":
            gestionar_plantilla(mi_equipo)
        elif op == "3":
            simular_partido(mi_equipo, rival)
        elif op == "4":
            print("¡Hasta la próxima!")
            break
        else:
            print("Opción inválida.")
