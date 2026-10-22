"""Versión de consola del juego de gestión de fútbol (sin Pygame)."""
import random
import time
import json
import os

# --- 1. CONFIGURACIÓN TÁCTICA Y CLASES ---

FORMACIONES = {
    "4-4-2": {"POR": 1, "DEF": 4, "CEN": 4, "DEL": 2},
    "4-3-3": {"POR": 1, "DEF": 4, "CEN": 3, "DEL": 3},
    "5-3-2": {"POR": 1, "DEF": 5, "CEN": 3, "DEL": 2},
}

ESTILOS = {
    "Ofensivo": {"ataque": 1.15, "defensa": 0.90, "desgaste": 1.2},
    "Equilibrado": {"ataque": 1.00, "defensa": 1.00, "desgaste": 1.0},
    "Defensivo": {"ataque": 0.85, "defensa": 1.15, "desgaste": 0.9},
}


class Jugador:
    def __init__(self, nombre, posicion, media, moral=80, cansancio=0, precio=2000000, goles=0, lesionado=0):
        self.nombre = nombre
        self.posicion = posicion  # POR, DEF, CEN, DEL
        self.media = media
        self.moral = moral
        self.cansancio = cansancio
        self.precio = precio
        self.goles = goles
        self.lesionado = lesionado  # Jornadas de baja (0 = sano)

    def rendimiento_real(self):
        if self.lesionado > 0:
            return 0
        factor_cansancio = 1 - (self.cansancio / 200)
        factor_moral = self.moral / 100
        return int(self.media * factor_cansancio * factor_moral)

    def to_dict(self):
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class Equipo:
    def __init__(self, nombre, presupuesto=12000000, formacion="4-4-2", estilo="Equilibrado"):
        self.nombre = nombre
        self.presupuesto = presupuesto
        self.plantilla = []
        self.alineacion_titular = []
        self.formacion = formacion
        self.estilo = estilo
        self.puntos = 0
        self.goles_a_favor = 0
        self.goles_en_contra = 0
        self.partidos_jugados = 0

    def agregar_jugador(self, jugador):
        self.plantilla.append(jugador)

    def convocar_once_automatico(self):
        """Selecciona el mejor once respetando la formación táctica actual y las lesiones."""
        esquema = FORMACIONES[self.formacion]
        disponibles = [j for j in self.plantilla if j.lesionado == 0]
        titulares = []

        # 1. Intentar cubrir cada posición según el esquema
        for pos, cantidad in esquema.items():
            candidatos = [j for j in disponibles if j.posicion == pos]
            candidatos.sort(key=lambda j: j.rendimiento_real(), reverse=True)
            seleccionados = candidatos[:cantidad]
            titulares.extend(seleccionados)
            for s in seleccionados:
                disponibles.remove(s)

        # 2. Si faltan efectivos en alguna línea, rellenar con los mejores disponibles (fuera de puesto)
        while len(titulares) < 11 and disponibles:
            disponibles.sort(key=lambda j: j.rendimiento_real(), reverse=True)
            titulares.append(disponibles.pop(0))

        self.alineacion_titular = titulares

    def calcular_fuerzas(self):
        """Devuelve una tupla (fuerza_ataque, fuerza_defensa) según jugadores y táctica."""
        if not self.alineacion_titular or any(j.lesionado > 0 for j in self.alineacion_titular):
            self.convocar_once_automatico()
        if not self.alineacion_titular:
            return 50, 50

        media_base = sum(j.rendimiento_real() for j in self.alineacion_titular) / len(self.alineacion_titular)
        mod = ESTILOS[self.estilo]
        return media_base * mod["ataque"], media_base * mod["defensa"]

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "presupuesto": self.presupuesto,
            "formacion": self.formacion,
            "estilo": self.estilo,
            "puntos": self.puntos,
            "goles_a_favor": self.goles_a_favor,
            "goles_en_contra": self.goles_en_contra,
            "partidos_jugados": self.partidos_jugados,
            "plantilla": [j.to_dict() for j in self.plantilla],
        }

    @classmethod
    def from_dict(cls, data):
        eq = cls(data["nombre"], data["presupuesto"], data["formacion"], data["estilo"])
        eq.puntos = data["puntos"]
        eq.goles_a_favor = data["goles_a_favor"]
        eq.goles_en_contra = data["goles_en_contra"]
        eq.partidos_jugados = data["partidos_jugados"]
        eq.plantilla = [Jugador.from_dict(j) for j in data["plantilla"]]
        eq.convocar_once_automatico()
        return eq


# --- 2. MOTOR DE SIMULACIÓN CON GOLEADORES Y LESIONES ---

def elegir_goleador(alineacion):
    """Elige quién marca ponderando la posición en el campo."""
    pesos = {"DEL": 50, "CEN": 30, "DEF": 10}
    return random.choices(alineacion, weights=[pesos.get(j.posicion, 1) for j in alineacion], k=1)[0]


def simular_partido(local, visitante):
    print(f"\n⚽ ¡PARTIDO: {local.nombre} ({local.formacion}, {local.estilo}) vs {visitante.nombre} ({visitante.formacion}, {visitante.estilo})!")

    atq_local, def_local = local.calcular_fuerzas()
    atq_vis, def_vis = visitante.calcular_fuerzas()

    # Factor campo (+3 en ataque y defensa local)
    atq_local += 3
    def_local += 3

    goles_local = 0
    goles_visitante = 0

    for minuto in [15, 30, 45, 60, 75, 90]:
        # Quién lleva la iniciativa en este tramo
        prob_iniciativa_local = atq_local / (atq_local + atq_vis)

        if random.random() < prob_iniciativa_local:
            exito = (atq_local / (atq_local + def_vis)) * 0.65
            if random.random() < exito:
                goles_local += 1
                autor = elegir_goleador(local.alineacion_titular)
                autor.goles += 1
                print(f"[{minuto}'] ¡GOOOOL de {autor.nombre} ({local.nombre})! ⚽")
        else:
            exito = (atq_vis / (atq_vis + def_local)) * 0.65
            if random.random() < exito:
                goles_visitante += 1
                autor = elegir_goleador(visitante.alineacion_titular)
                autor.goles += 1
                print(f"[{minuto}'] ¡GOOOOL de {autor.nombre} ({visitante.nombre})! ⚽")
        time.sleep(0.2)

    # Actualizar tabla
    local.partidos_jugados += 1
    visitante.partidos_jugados += 1
    local.goles_a_favor += goles_local
    local.goles_en_contra += goles_visitante
    visitante.goles_a_favor += goles_visitante
    visitante.goles_en_contra += goles_local

    if goles_local > goles_visitante:
        local.puntos += 3
        res = f"Victoria de {local.nombre} ({goles_local} - {goles_visitante})"
    elif goles_local < goles_visitante:
        visitante.puntos += 3
        res = f"Victoria de {visitante.nombre} ({goles_local} - {goles_visitante})"
    else:
        local.puntos += 1
        visitante.puntos += 1
        res = f"Empate ({goles_local} - {goles_visitante})"

    print(f"🏁 FINAL: {res}")

    # Desgaste físico, recuperación de lesionados previos y riesgo de nuevas lesiones
    for eq in [local, visitante]:
        # Los que estaban en la enfermería descuentan 1 jornada
        for j in eq.plantilla:
            if j not in eq.alineacion_titular and j.lesionado > 0:
                j.lesionado -= 1
                if j.lesionado == 0:
                    print(f"🟢 {j.nombre} ({eq.nombre}) ha recibido el alta médica.")

        # Desgaste y riesgo de lesión para los titulares
        mult_desgaste = ESTILOS[eq.estilo]["desgaste"]
        for j in eq.alineacion_titular:
            desgaste = int(random.randint(15, 25) * mult_desgaste)
            j.cansancio = min(100, j.cansancio + desgaste)

            # Si el cansancio supera el 75%, hay un 12% de riesgo de lesión
            prob_lesion = 0.12 if j.cansancio > 75 else 0.02
            if random.random() < prob_lesion:
                j.lesionado = random.randint(1, 3)
                print(f"🚑 ¡Lesión! {j.nombre} ({eq.nombre}) sufre molestias y será baja {j.lesionado} jornada(s).")


# --- 3. MENÚS DE GESTIÓN, TÁCTICA Y GOLEADORES ---

def menu_tactica_y_plantilla(equipo):
    while True:
        equipo.convocar_once_automatico()
        print(f"\n--- GESTIÓN DE {equipo.nombre.upper()} ---")
        print(f"Esquema actual: {equipo.formacion} | Estilo: {equipo.estilo}")
        print(f"{'No.':<3} {'Nombre':<16} {'Pos':<4} {'Med':<4} {'Rend':<5} {'Mor':<4} {'Cans':<5} {'Goles':<5} {'Estado'}")
        print("-" * 68)
        for i, j in enumerate(equipo.plantilla):
            titular_mark = "*" if j in equipo.alineacion_titular else " "
            estado = f"Baja ({j.lesionado}j)" if j.lesionado > 0 else ("Titular" if titular_mark == "*" else "Suplente")
            print(f"{i+1:<2}{titular_mark} {j.nombre:<16} {j.posicion:<4} {j.media:<4} {j.rendimiento_real():<5} {j.moral:<4} {j.cansancio:<4}% {j.goles:<5} {estado}")

        print("\nOpciones:")
        print("1. Cambiar Formación (4-4-2, 4-3-3, 5-3-2)")
        print("2. Cambiar Estilo (Ofensivo, Equilibrado, Defensivo)")
        print("3. Volver al menú principal")

        op = input("Elige una opción: ")
        if op == "1":
            f = input("Introduce formación (4-4-2 / 4-3-3 / 5-3-2): ").strip()
            if f in FORMACIONES:
                equipo.formacion = f
                equipo.convocar_once_automatico()
                print(f"✅ Formación cambiada a {f}.")
            else:
                print("❌ Formación no reconocida.")
        elif op == "2":
            e = input("Introduce estilo (Ofensivo / Equilibrado / Defensivo): ").strip().capitalize()
            if e in ESTILOS:
                equipo.estilo = e
                print(f"✅ Estilo cambiado a {e}.")
            else:
                print("❌ Estilo no reconocido.")
        elif op == "3":
            break
        else:
            print("Opción no válida.")


def mostrar_goleadores(equipos):
    print("\n" + "=" * 45)
    print(f"{'TABLA DE GOLEADORES (PICHICHI)':^45}")
    print("=" * 45)
    todos_jugadores = [(j, eq.nombre) for eq in equipos for j in eq.plantilla if j.goles > 0]
    todos_jugadores.sort(key=lambda x: x[0].goles, reverse=True)

    if not todos_jugadores:
        print("Todavía no se han marcado goles en la liga.")
    else:
        print(f"{'Pos':<4} {'Jugador':<18} {'Equipo':<16} {'Goles'}")
        print("-" * 45)
        for i, (jug, eq_nom) in enumerate(todos_jugadores[:10]):
            print(f"{i+1:<4} {jug.nombre:<18} {eq_nom:<16} {jug.goles}")
    print("=" * 45)


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


def mostrar_mercado(equipo, mercado_disponible):
    while True:
        print(f"\n--- MERCADO DE FICHAJES (Presupuesto: {equipo.presupuesto:,} €) ---")
        for i, j in enumerate(mercado_disponible):
            print(f"{i+1}. {j.nombre:<16} | Pos: {j.posicion} | Media: {j.media} | Precio: {j.precio:,} €")
        print("0. Volver")
        try:
            op = int(input("Número de jugador a fichar (0 para salir): "))
        except ValueError:
            print("Entrada no válida.")
            continue
        if op == 0:
            break
        if 1 <= op <= len(mercado_disponible):
            jug = mercado_disponible[op - 1]
            if equipo.presupuesto >= jug.precio:
                equipo.presupuesto -= jug.precio
                equipo.agregar_jugador(jug)
                mercado_disponible.pop(op - 1)
                print(f"✅ ¡Has fichado a {jug.nombre}!")
            else:
                print("❌ Presupuesto insuficiente.")
        else:
            print("Número no válido.")


def centro_tecnico(equipo):
    print("\n--- CENTRO TÉCNICO ---")
    print("1. Descansar plantilla (-30% cansancio, +10 moral)")
    print("2. Entrenamiento intensivo (+15% cansancio, opción de subir media)")
    op = input("Elige una opción (Enter para cancelar): ")
    if op == "1":
        for j in equipo.plantilla:
            j.cansancio = max(0, j.cansancio - 30)
            j.moral = min(100, j.moral + 10)
        print("💤 La plantilla ha descansado y recupera frescura.")
    elif op == "2":
        for j in equipo.plantilla:
            if j.lesionado == 0:
                j.cansancio = min(100, j.cansancio + 15)
                if random.random() < 0.15 and j.media < 90:
                    j.media += 1
                    print(f"⭐ ¡{j.nombre} sube su media a {j.media}!")
        print("💪 Sesión de entrenamiento completada.")


# --- 4. CALENDARIO Y PERSISTENCIA (GUARDAR / CARGAR JSON) ---

def generar_calendario_nombres(nombres_equipos):
    n = len(nombres_equipos)  # se asume número par de equipos
    l = nombres_equipos[:]
    calendario_ida = []
    for _ in range(n - 1):
        jornada = [(l[i], l[n - 1 - i]) for i in range(n // 2)]
        calendario_ida.append(jornada)
        l = [l[0]] + [l[-1]] + l[1:-1]
    calendario_vuelta = [[(vis, loc) for loc, vis in j] for j in calendario_ida]
    return calendario_ida + calendario_vuelta


def guardar_partida(archivo, jornada_actual, equipos, mercado, calendario_nombres):
    datos = {
        "jornada_actual": jornada_actual,
        "equipos": [e.to_dict() for e in equipos],
        "mercado": [j.to_dict() for j in mercado],
        "calendario": calendario_nombres,
    }
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"💾 Partida guardada correctamente en '{archivo}'.")


def cargar_partida(archivo):
    if not os.path.exists(archivo):
        print("❌ No existe ningún archivo de guardado previo.")
        return None
    with open(archivo, "r", encoding="utf-8") as f:
        datos = json.load(f)
    equipos = [Equipo.from_dict(e) for e in datos["equipos"]]
    mercado = [Jugador.from_dict(j) for j in datos["mercado"]]
    # JSON convierte las tuplas en listas; el desempaquetado del bucle principal sigue funcionando
    print(f"📂 Partida cargada desde la jornada {datos['jornada_actual'] + 1}.")
    return datos["jornada_actual"], equipos, mercado, datos["calendario"]


# --- 5. INICIALIZACIÓN Y BUCLE PRINCIPAL ---

def crear_plantilla_base(equipo, es_usuario=False):
    if es_usuario:
        base = [
            ("Poussin", "POR", 72), ("A. Francés", "DEF", 75), ("Jair Amador", "DEF", 73),
            ("Lluís López", "DEF", 71), ("Tasende", "DEF", 72), ("Borge", "DEF", 70),
            ("Francho", "CEN", 77), ("Marc Aguado", "CEN", 75), ("Maikel Mesa", "CEN", 76),
            ("Toni Moya", "CEN", 74), ("Gori", "CEN", 70), ("Iván Azón", "DEL", 74),
            ("Soberón", "DEL", 75), ("Bazdar", "DEL", 73),
        ]
        for nom, pos, med in base:
            equipo.agregar_jugador(Jugador(nom, pos, med, precio=med * 40000))
    else:
        # Plantilla compensada para rivales (1 POR, 5 DEF, 5 CEN, 3 DEL)
        posiciones = ["POR"] + ["DEF"] * 5 + ["CEN"] * 5 + ["DEL"] * 3
        for i, pos in enumerate(posiciones):
            equipo.agregar_jugador(Jugador(f"{pos}_{equipo.nombre[:3]}_{i+1}", pos, random.randint(70, 75)))


if __name__ == "__main__":
    ARCHIVO_SAVE = "partida_guardada.json"

    mi_equipo = Equipo("Real Zaragoza", presupuesto=10000000)
    crear_plantilla_base(mi_equipo, es_usuario=True)

    rivales = [Equipo("SD Huesca"), Equipo("Racing Santander"), Equipo("Sporting Gijón")]
    for r in rivales:
        crear_plantilla_base(r, es_usuario=False)

    lista_equipos = [mi_equipo] + rivales

    mercado = [
        Jugador("Aketxe", "CEN", 76, precio=3200000),
        Jugador("Keidi Bare", "CEN", 76, precio=3500000),
        Jugador("Alberto Marí", "DEL", 74, precio=2500000),
        Jugador("Bernardo Vital", "DEF", 74, precio=2400000),
    ]

    calendario = generar_calendario_nombres([e.nombre for e in lista_equipos])
    jornada_actual = 0

    while jornada_actual < len(calendario):
        mapa_equipos = {e.nombre: e for e in lista_equipos}
        mi_equipo = mapa_equipos["Real Zaragoza"]

        print(f"\n================ JORNADA {jornada_actual + 1} de {len(calendario)} ================")
        for loc_nom, vis_nom in calendario[jornada_actual]:
            print(f"  • {loc_nom} vs {vis_nom}")

        print("\nMenú de Mánager:")
        print("1. Jugar Jornada")
        print("2. Clasificación y Goleadores (Pichichi)")
        print("3. Plantilla y Táctica (Formación / Estilo)")
        print("4. Mercado de Fichajes")
        print("5. Centro Técnico (Entrenar / Descansar)")
        print("6. Guardar Partida")
        print("7. Cargar Partida")
        print("8. Salir")

        op = input("Selecciona una opción: ")

        if op == "1":
            for loc_nom, vis_nom in calendario[jornada_actual]:
                simular_partido(mapa_equipos[loc_nom], mapa_equipos[vis_nom])
            jornada_actual += 1
        elif op == "2":
            mostrar_clasificacion(lista_equipos)
            mostrar_goleadores(lista_equipos)
        elif op == "3":
            menu_tactica_y_plantilla(mi_equipo)
        elif op == "4":
            mostrar_mercado(mi_equipo, mercado)
        elif op == "5":
            centro_tecnico(mi_equipo)
        elif op == "6":
            guardar_partida(ARCHIVO_SAVE, jornada_actual, lista_equipos, mercado, calendario)
        elif op == "7":
            cargado = cargar_partida(ARCHIVO_SAVE)
            if cargado:
                jornada_actual, lista_equipos, mercado, calendario = cargado
        elif op == "8":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida.")

    if jornada_actual >= len(calendario):
        print("\n🎉 ¡La temporada ha finalizado! Clasificación final:")
        mostrar_clasificacion(lista_equipos)
        mostrar_goleadores(lista_equipos)
