"""Versión de consola del juego de gestión de fútbol (sin Pygame)."""
import random
import time


# --- 1. CLASES Y ESTRUCTURA DE DATOS ---

class Jugador:
    def __init__(self, nombre, posicion, media, moral=80, cansancio=0, precio=2000000):
        self.nombre = nombre
        self.posicion = posicion  # POR, DEF, CEN, DEL
        self.media = media        # De 1 a 100
        self.moral = moral        # De 0 a 100
        self.cansancio = cansancio  # De 0 a 100
        self.precio = precio      # Valor en mercado

    def rendimiento_real(self):
        factor_cansancio = 1 - (self.cansancio / 200)
        factor_moral = self.moral / 100
        return int(self.media * factor_cansancio * factor_moral)


class Equipo:
    def __init__(self, nombre, presupuesto=12000000):
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
        ordenados = sorted(self.plantilla, key=lambda j: j.rendimiento_real(), reverse=True)
        self.alineacion_titular = ordenados[:11]

    def calcular_fuerza_equipo(self):
        if not self.alineacion_titular:
            self.convocar_once_automatico()
        if not self.alineacion_titular:
            return 50  # Valor por defecto si no hay jugadores
        return sum(j.rendimiento_real() for j in self.alineacion_titular) / len(self.alineacion_titular)


# --- 2. GENERADOR DE CALENDARIO DE LIGA (IDA Y VUELTA) ---

def generar_calendario(equipos):
    l = list(equipos)  # copia: no modificamos la lista del llamador
    if len(l) % 2 != 0:
        # Equipo fantasma "DESCANSA" si el número es impar
        l.append(Equipo("DESCANSA"))
    n = len(l)

    calendario_ida = []
    for _ in range(n - 1):
        partidos = []
        for i in range(n // 2):
            eq1 = l[i]
            eq2 = l[n - 1 - i]
            if eq1.nombre != "DESCANSA" and eq2.nombre != "DESCANSA":
                partidos.append((eq1, eq2))
        calendario_ida.append(partidos)
        l = [l[0]] + [l[-1]] + l[1:-1]

    # La vuelta invierte local y visitante
    calendario_vuelta = [[(eq2, eq1) for eq1, eq2 in jornada] for jornada in calendario_ida]
    return calendario_ida + calendario_vuelta


# --- 3. MERCADO DE FICHAJES Y FINANZAS ---

def mostrar_mercado(equipo, mercado_disponible):
    while True:
        print("\n--- MERCADO DE FICHAJES ---")
        print(f"Presupuesto actual: {equipo.presupuesto:,} €")
        print(f"{'No.':<4} {'Nombre':<18} {'Pos':<5} {'Media':<7} {'Precio'}")
        print("-" * 45)
        for i, j in enumerate(mercado_disponible):
            print(f"{i+1:<4} {j.nombre:<18} {j.posicion:<5} {j.media:<7} {j.precio:,} €")

        print("\nOpciones:")
        print("1. Fichar un jugador (indica número)")
        print("2. Volver al menú principal")

        op = input("Elige una opción: ")
        if op == "1":
            try:
                idx = int(input("Número del jugador a fichar: ")) - 1
                if 0 <= idx < len(mercado_disponible):
                    jugador = mercado_disponible[idx]
                    if equipo.presupuesto >= jugador.precio:
                        equipo.presupuesto -= jugador.precio
                        equipo.agregar_jugador(jugador)
                        mercado_disponible.pop(idx)
                        print(f"¡Fichaje completado! {jugador.nombre} ya forma parte de tu plantilla.")
                    else:
                        print("❌ No tienes suficiente presupuesto.")
                else:
                    print("Número no válido.")
            except ValueError:
                print("Por favor, introduce un número válido.")
        elif op == "2":
            break
        else:
            print("Opción no válida.")


# --- 4. ENTRENAMIENTO Y RECUPERACIÓN (FATIGA) ---

def centro_tecnico(equipo):
    while True:
        print("\n--- CENTRO TÉCNICO Y FASE FÍSICA ---")
        print("1. Descansar plantilla (Reduce cansancio, sube moral)")
        print("2. Entrenamiento táctico/físico (Sube media/rendimiento, aumenta cansancio)")
        print("3. Volver al menú principal")

        op = input("Elige una opción: ")
        if op == "1":
            for j in equipo.plantilla:
                j.cansancio = max(0, j.cansancio - 30)
                j.moral = min(100, j.moral + 10)
            print("💤 El equipo ha descansado. Los jugadores han recuperado energía y moral.")
            input("Presiona Enter para continuar...")
            break
        elif op == "2":
            for j in equipo.plantilla:
                j.cansancio = min(100, j.cansancio + 15)
                # Pequeña probabilidad de mejora de media si se esfuerzan
                if random.random() < 0.15 and j.media < 90:
                    j.media += 1
                    print(f"⭐ ¡{j.nombre} ha mejorado su media entrenando duro y sube a {j.media}!")
            print("💪 Entrenamiento completado. El equipo está a punto, pero ha acumulado algo de fatiga.")
            input("Presiona Enter para continuar...")
            break
        elif op == "3":
            break
        else:
            print("Opción no válida.")


# --- 5. GESTIÓN DE PLANTILLA ---

def gestionar_plantilla(equipo):
    while True:
        print(f"\n--- PLANTILLA DE {equipo.nombre.upper()} ---")
        print(f"{'No.':<4} {'Nombre':<18} {'Pos':<5} {'Media':<7} {'Moral':<7} {'Cansancio'}")
        print("-" * 55)
        for i, j in enumerate(equipo.plantilla):
            print(f"{i+1:<4} {j.nombre:<18} {j.posicion:<5} {j.media:<7} {j.moral:<7} {j.cansancio}%")

        print("\nOpciones:")
        print("1. Ver once titular actual")
        print("2. Auto-convocar mejor once")
        print("3. Volver")

        opcion = input("Elige una opción: ")
        if opcion == "1":
            equipo.convocar_once_automatico()
            print("\n--- ONCE TITULAR ---")
            for j in equipo.alineacion_titular:
                print(f"- {j.nombre} ({j.posicion}) | Media: {j.media} | Rendimiento Real: {j.rendimiento_real()}")
            input("\nPresiona Enter para continuar...")
        elif opcion == "2":
            equipo.convocar_once_automatico()
            print("¡Once titular actualizado!")
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")


# --- 6. MOTOR DE SIMULACIÓN DE PARTIDOS ---

def simular_partido(equipo_local, equipo_visitante):
    print(f"\n⚽ ¡PARTIDO: {equipo_local.nombre} vs {equipo_visitante.nombre}!")

    fuerza_local = equipo_local.calcular_fuerza_equipo() + 3  # Factor campo
    fuerza_visitante = equipo_visitante.calcular_fuerza_equipo()

    goles_local = 0
    goles_visitante = 0

    for minuto in [15, 30, 45, 60, 75, 90]:
        if random.random() < fuerza_local / (fuerza_local + fuerza_visitante):
            if random.random() < 0.35:
                goles_local += 1
                print(f"[{minuto}'] ¡GOOOOOOL de {equipo_local.nombre}! ⚽")
        else:
            if random.random() < 0.35:
                goles_visitante += 1
                print(f"[{minuto}'] ¡GOOOOOOL de {equipo_visitante.nombre}! ⚽")
        time.sleep(0.3)

    equipo_local.partidos_jugados += 1
    equipo_visitante.partidos_jugados += 1
    equipo_local.goles_a_favor += goles_local
    equipo_local.goles_en_contra += goles_visitante
    equipo_visitante.goles_a_favor += goles_visitante
    equipo_visitante.goles_en_contra += goles_local

    if goles_local > goles_visitante:
        equipo_local.puntos += 3
        res = f"Victoria de {equipo_local.nombre} ({goles_local} - {goles_visitante})"
    elif goles_local < goles_visitante:
        equipo_visitante.puntos += 3
        res = f"Victoria de {equipo_visitante.nombre} ({goles_visitante} - {goles_local})"
    else:
        equipo_local.puntos += 1
        equipo_visitante.puntos += 1
        res = f"Empate ({goles_local} - {goles_visitante})"

    print(f"\n🏁 FINAL: {res}\n")

    # Desgaste físico post-partido
    for j in equipo_local.alineacion_titular + equipo_visitante.alineacion_titular:
        j.cansancio = min(100, j.cansancio + random.randint(20, 35))


def mostrar_clasificacion(equipos):
    print("\n" + "=" * 50)
    print(f"{'CLASIFICACIÓN GENERAL':^50}")
    print("=" * 50)
    print(f"{'Pos':<4} {'Equipo':<18} {'PTS':<5} {'PJ':<5} {'GF':<5} {'GC':<5} {'DG'}")
    print("-" * 50)

    ordenados = sorted(equipos, key=lambda e: (e.puntos, e.goles_a_favor - e.goles_en_contra), reverse=True)
    for i, eq in enumerate(ordenados):
        dg = eq.goles_a_favor - eq.goles_en_contra
        print(f"{i+1:<4} {eq.nombre:<18} {eq.puntos:<5} {eq.partidos_jugados:<5} {eq.goles_a_favor:<5} {eq.goles_en_contra:<5} {dg:+d}")
    print("=" * 50)


# --- 7. FLUJO PRINCIPAL DEL JUEGO ---
if __name__ == "__main__":
    mi_equipo = Equipo("Real Zaragoza", presupuesto=15000000)
    rival_1 = Equipo("SD Huesca")
    rival_2 = Equipo("SD Eibar")
    rival_3 = Equipo("Real Valladolid")

    lista_equipos = [mi_equipo, rival_1, rival_2, rival_3]

    mi_equipo.agregar_jugador(Jugador("Poussin", "POR", 72, precio=1000000))
    mi_equipo.agregar_jugador(Jugador("A. Francés", "DEF", 75, precio=3500000))
    mi_equipo.agregar_jugador(Jugador("Gisain", "DEF", 73, precio=2000000))
    mi_equipo.agregar_jugador(Jugador("Maikel Mesa", "CEN", 76, precio=4000000))
    mi_equipo.agregar_jugador(Jugador("Francho", "CEN", 77, precio=5000000))
    mi_equipo.agregar_jugador(Jugador("Valera", "DEL", 74, precio=3000000))
    for i in range(1, 6):
        mi_equipo.agregar_jugador(Jugador(f"Canterano {i}", "CEN", 68, precio=800000))

    for eq in [rival_1, rival_2, rival_3]:
        eq.agregar_jugador(Jugador("Portero Rival", "POR", 72))
        for i in range(1, 11):
            eq.agregar_jugador(Jugador(f"Jugador {i}", "CEN", 71))

    mercado = [
        Jugador("Sinan Bakis", "DEL", 75, precio=3200000),
        Jugador("Mollejo", "DEL", 74, precio=2800000),
        Jugador("Jair Amador", "DEF", 73, precio=1900000),
        Jugador("Marc Aguado", "CEN", 76, precio=3500000),
    ]

    calendario = generar_calendario(lista_equipos)
    jornada_actual = 0

    print("🏆 ¡BIENVENIDO A TU MÁNAGER DE FÚTBOL EN PYTHON!")

    while jornada_actual < len(calendario):
        mi_equipo.convocar_once_automatico()
        print(f"\n--- JORNADA {jornada_actual + 1} de {len(calendario)} ---")
        print("Partidos de esta jornada:")

        partidos_de_la_jornada = calendario[jornada_actual]
        for eq1, eq2 in partidos_de_la_jornada:
            marca = "  ← TU PARTIDO" if mi_equipo in (eq1, eq2) else ""
            print(f"  • {eq1.nombre} vs {eq2.nombre}{marca}")

        print("\nMenú de Gestión:")
        print("1. Jugar partidos de la jornada")
        print("2. Ver Clasificación")
        print("3. Gestionar Plantilla y Once Titular")
        print("4. Mercado de Fichajes")
        print("5. Centro Técnico (Entrenamiento / Descanso)")
        print("6. Salir del juego")

        op = input("Selecciona una opción: ")

        if op == "1":
            print(f"\n--- SIMULANDO JORNADA {jornada_actual + 1} ---")
            for eq1, eq2 in partidos_de_la_jornada:
                simular_partido(eq1, eq2)
            jornada_actual += 1
            input("\nJornada finalizada. Presiona Enter para continuar...")
        elif op == "2":
            mostrar_clasificacion(lista_equipos)
            input("\nPresiona Enter para continuar...")
        elif op == "3":
            gestionar_plantilla(mi_equipo)
        elif op == "4":
            mostrar_mercado(mi_equipo, mercado)
        elif op == "5":
            centro_tecnico(mi_equipo)
        elif op == "6":
            print("¡Gracias por jugar! Hasta pronto.")
            break
        else:
            print("Opción no válida.")

    if jornada_actual >= len(calendario):
        print("\n🎉 ¡La temporada ha finalizado! Clasificación final:")
        mostrar_clasificacion(lista_equipos)
