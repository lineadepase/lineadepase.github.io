"""Prototipo de escritorio con Tkinter. Mantengo en este archivo el modelo de datos de esta interfaz, la construcción de pestañas, el mapa de tiros y los eventos de usuario. No es una aplicación móvil."""
import tkinter as tk
from tkinter import ttk, messagebox
import random
import os

# --- 1. CONFIGURACIÓN TÁCTICA Y COORDENADAS EN EL CAMPO (PIZARRA 2D) ---

# Cada formación indica cuántos jugadores necesito por línea; todas suman once.
FORMACIONES = {
    "4-4-2": {"POR": 1, "DEF": 4, "CEN": 4, "DEL": 2},
    "4-3-3": {"POR": 1, "DEF": 4, "CEN": 3, "DEL": 3},
    "5-3-2": {"POR": 1, "DEF": 5, "CEN": 3, "DEL": 2},
}

# Coordenadas normalizadas (x, y de 0.0 a 1.0) para dibujar a los jugadores en el campo
COORDENADAS_FORMACION = {
    "4-4-2": [
        (0.08, 0.50),  # POR
        (0.25, 0.18), (0.25, 0.38), (0.25, 0.62), (0.25, 0.82),  # 4 DEF
        (0.50, 0.18), (0.50, 0.38), (0.50, 0.62), (0.50, 0.82),  # 4 CEN
        (0.76, 0.35), (0.76, 0.65),  # 2 DEL
    ],
    "4-3-3": [
        (0.08, 0.50),  # POR
        (0.25, 0.18), (0.25, 0.38), (0.25, 0.62), (0.25, 0.82),  # 4 DEF
        (0.50, 0.25), (0.50, 0.50), (0.50, 0.75),  # 3 CEN
        (0.76, 0.22), (0.76, 0.50), (0.76, 0.78),  # 3 DEL
    ],
    "5-3-2": [
        (0.08, 0.50),  # POR
        (0.25, 0.12), (0.25, 0.31), (0.25, 0.50), (0.25, 0.69), (0.25, 0.88),  # 5 DEF
        (0.50, 0.25), (0.50, 0.50), (0.50, 0.75),  # 3 CEN
        (0.76, 0.35), (0.76, 0.65),  # 2 DEL
    ],
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


# --- 2. MODELO DE DATOS ---

class Jugador:
    """Modelo reducido de futbolista que utiliza la interfaz Tkinter."""
    def __init__(self, nombre, posicion, media, precio=2000000, salario=15000):
        """Guardo los datos básicos del jugador y preparo sus estadísticas para una temporada nueva."""
        self.nombre = nombre
        self.posicion = posicion
        self.media = media
        self.moral = 85
        self.cansancio = 0
        self.precio = precio
        self.salario = salario
        self.goles = 0
        self.xg_acumulado = 0.0
        self.lesionado = 0

    def rendimiento_real(self):
        """Ajusto la media por fatiga y moral; mientras haya lesión, el jugador no aporta rendimiento."""
        if self.lesionado > 0:
            return 0
        factor_cansancio = 1 - (self.cansancio / 200)
        factor_moral = self.moral / 100
        return int(self.media * factor_cansancio * factor_moral)


class Equipo:
    """Modelo de club para la versión gráfica; mantiene su once y estadísticas junto a la plantilla."""
    def __init__(self, nombre, presupuesto=10000000, aforo=28000):
        """Inicializo el club, la táctica por defecto y los contadores de liga."""
        self.nombre = nombre
        self.presupuesto = presupuesto
        self.aforo = aforo
        self.plantilla = []
        self.alineacion_titular = []
        self.formacion = "4-4-2"
        self.estilo = "Equilibrado"
        self.puntos = 0
        self.pj = 0
        self.gf = 0
        self.gc = 0
        self.xg_f = 0.0
        self.xg_c = 0.0

    def agregar_jugador(self, j):
        """Incorporo el jugador al listado de la plantilla."""
        self.plantilla.append(j)

    def masa_salarial(self):
        """Calculo el coste salarial de una jornada sumando todos los contratos."""
        return sum(j.salario for j in self.plantilla)

    def convocar_once_automatico(self):
        """Formo el once respetando primero las posiciones previstas y cubriendo después los huecos con los mejores disponibles."""
        esquema = FORMACIONES[self.formacion]
        disponibles = [j for j in self.plantilla if j.lesionado == 0]
        titulares = []
        for pos, cant in esquema.items():
            cand = sorted([j for j in disponibles if j.posicion == pos], key=lambda x: x.rendimiento_real(), reverse=True)
            sel = cand[:cant]
            titulares.extend(sel)
            for s in sel:
                disponibles.remove(s)
        while len(titulares) < 11 and disponibles:
            disponibles.sort(key=lambda x: x.rendimiento_real(), reverse=True)
            titulares.append(disponibles.pop(0))
        self.alineacion_titular = titulares

    def calcular_fuerzas(self):
        """Calculo las fuerzas de ataque y defensa del once después de aplicar el estilo táctico."""
        if len(self.alineacion_titular) < 11 or any(j.lesionado > 0 for j in self.alineacion_titular):
            self.convocar_once_automatico()
        media_base = sum(j.rendimiento_real() for j in self.alineacion_titular) / max(1, len(self.alineacion_titular))
        mod = ESTILOS[self.estilo]
        return media_base * mod["ataque"], media_base * mod["defensa"]


# --- 3. INTERFAZ GRÁFICA (TKINTER GUI) ---

class FootballManagerGUI:
    """Coordina los datos de la versión de escritorio, construye las pestañas y conecta botones con la simulación."""
    def __init__(self, root):
        """Preparo la ventana principal y construyo los datos, estilos y controles en ese orden."""
        self.root = root
        self.root.title("Línea de Pase - Football Manager & xG Lab")
        self.root.geometry("1120x720")
        self.root.configure(bg="#0f172a")

        self.imagenes_cache = {}
        self.inicializar_datos()
        self.configurar_estilos()
        self.crear_interfaz()
        self.actualizar_todo()

    def cargar_imagen_segura(self, ruta, ancho=None, alto=None):
        """Carga un archivo PNG/GIF desde la carpeta assets/ si existe."""
        if os.path.exists(ruta):
            try:
                img = tk.PhotoImage(file=ruta)
                self.imagenes_cache[ruta] = img
                return img
            except Exception:
                return None
        return None

    def inicializar_datos(self):
        """Creo el club, los rivales ficticios, el mercado y el calendario de ida y vuelta inicial."""
        self.mi_equipo = Equipo("FC Pase y Pifia", presupuesto=9500000, aforo=30000)
        base_rz = [
            ("Paco Manoplas", "POR", 72), ("Rafa Rechaces", "DEF", 75), ("Tino Tobillo", "DEF", 73),
            ("Blas Banderín", "DEF", 71), ("Lola Cerrojazo", "DEF", 73), ("Nico Nopuedo", "DEF", 70),
            ("Pili Pasecorto", "CEN", 77), ("Rolo Rondo", "CEN", 75), ("Mauri MediaVuelta", "CEN", 76),
            ("Cris Cañito", "CEN", 74), ("Fede FueraJuego", "CEN", 70), ("Golo Goloso", "DEL", 74),
            ("Rita Remates", "DEL", 75), ("Charly Trallazo", "DEL", 73),
        ]
        for nom, pos, med in base_rz:
            self.mi_equipo.agregar_jugador(Jugador(nom, pos, med, precio=med * 35000, salario=med * 220))
        self.mi_equipo.convocar_once_automatico()

        self.rivales = [Equipo("Atlético Siestense", aforo=9000), Equipo("Unión Deportiva Patapalo", aforo=22000), Equipo("Deportivo Balón Perdido", aforo=29000)]
        for r in self.rivales:
            posiciones = ["POR"] + ["DEF"] * 5 + ["CEN"] * 5 + ["DEL"] * 3
            contadores = {pos: 0 for pos in NOMBRES_RIVALES}
            apodo = r.nombre.split()[0]
            for pos in posiciones:
                med = random.randint(70, 75)
                nombres = NOMBRES_RIVALES[pos]
                nombre = f"{nombres[contadores[pos] % len(nombres)]} ({apodo})"
                contadores[pos] += 1
                r.agregar_jugador(Jugador(nombre, pos, med, precio=med * 35000, salario=med * 200))
            r.convocar_once_automatico()

        self.equipos = [self.mi_equipo] + self.rivales
        self.mercado = [
            Jugador("Crispín Chutapiedras", "CEN", 76, precio=2800000, salario=18000),
            Jugador("Pipo Puntería", "CEN", 76, precio=3000000, salario=19000),
            Jugador("Tere Taconazo", "DEL", 74, precio=2200000, salario=15000),
            Jugador("Benito Banderazo", "DEF", 74, precio=2100000, salario=14500),
            Jugador("Marga Parapenaltis", "CEN", 75, precio=2400000, salario=16000),
        ]

        # Generar calendario ida y vuelta
        nombres = [e.nombre for e in self.equipos]
        l = nombres[:]
        ida = []
        for _ in range(len(nombres) - 1):
            ida.append([(l[i], l[len(nombres) - 1 - i]) for i in range(len(nombres) // 2)])
            l = [l[0]] + [l[-1]] + l[1:-1]
        vuelta = [[(vis, loc) for loc, vis in j] for j in ida]
        self.calendario = ida + vuelta
        self.jornada_actual = 0

    def configurar_estilos(self):
        """Defino los colores, tamaños y estados visuales de los controles ttk."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#0f172a", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1e293b", foreground="#cbd5e1", padding=[16, 8], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#2563eb")], foreground=[("selected", "white")])
        style.configure("Treeview", background="#1e293b", foreground="white", fieldbackground="#1e293b", rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#334155", foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#2563eb")])

    def crear_interfaz(self):
        # Cabecera superior
        """Monto la cabecera, las pestañas principales y sus paneles de trabajo."""
        self.header = tk.Frame(self.root, bg="#1e293b", height=65, padx=20, pady=10)
        self.header.pack(fill="x")

        self.lbl_club = tk.Label(self.header, text="⚽ FC PASE Y PIFIA", fg="white", bg="#1e293b", font=("Segoe UI", 16, "bold"))
        self.lbl_club.pack(side="left")

        self.lbl_info_top = tk.Label(self.header, text="", fg="#38bdf8", bg="#1e293b", font=("Segoe UI", 12, "bold"))
        self.lbl_info_top.pack(side="right")

        # Contenedor de pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        self.tab_tactica = tk.Frame(self.notebook, bg="#0f172a")
        self.tab_partido = tk.Frame(self.notebook, bg="#0f172a")
        self.tab_liga = tk.Frame(self.notebook, bg="#0f172a")
        self.tab_mercado = tk.Frame(self.notebook, bg="#0f172a")

        self.notebook.add(self.tab_tactica, text="📋 Pizarra Táctica y Plantilla")
        self.notebook.add(self.tab_partido, text="⚽ Día de Partido y Mapa xG")
        self.notebook.add(self.tab_liga, text="📊 Clasificación y Métricas")
        self.notebook.add(self.tab_mercado, text="💶 Mercado y Centro Técnico")

        self.construir_tab_tactica()
        self.construir_tab_partido()
        self.construir_tab_liga()
        self.construir_tab_mercado()

    # --- PESTAÑA 1: PIZARRA TÁCTICA Y PLANTILLA ---
    def construir_tab_tactica(self):
        """Construyo los selectores de formación y estilo, la tabla de plantilla y la pizarra táctica."""
        panel_izq = tk.Frame(self.tab_tactica, bg="#0f172a")
        panel_izq.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        controles = tk.Frame(panel_izq, bg="#1e293b", padx=10, pady=8)
        controles.pack(fill="x", pady=(0, 10))

        tk.Label(controles, text="Formación:", fg="white", bg="#1e293b", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        self.combo_form = ttk.Combobox(controles, values=list(FORMACIONES.keys()), state="readonly", width=8)
        self.combo_form.set(self.mi_equipo.formacion)
        self.combo_form.pack(side="left", padx=5)
        self.combo_form.bind("<<ComboboxSelected>>", self.cambiar_tactica)

        tk.Label(controles, text="Estilo:", fg="white", bg="#1e293b", font=("Segoe UI", 10, "bold")).pack(side="left", padx=10)
        self.combo_estilo = ttk.Combobox(controles, values=list(ESTILOS.keys()), state="readonly", width=12)
        self.combo_estilo.set(self.mi_equipo.estilo)
        self.combo_estilo.pack(side="left", padx=5)
        self.combo_estilo.bind("<<ComboboxSelected>>", self.cambiar_tactica)

        btn_auto = tk.Button(controles, text="🔄 Auto-Convocar Mejor 11", bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, command=self.autoconvocar)
        btn_auto.pack(side="right", padx=5)

        # Tabla de jugadores
        cols = ("Pos", "Nombre", "Media", "Rend", "Cansancio", "Goles", "xG", "Estado")
        self.tree_plantilla = ttk.Treeview(panel_izq, columns=cols, show="headings", height=18)
        anchos = [45, 130, 50, 50, 75, 50, 55, 80]
        for col, w in zip(cols, anchos):
            self.tree_plantilla.heading(col, text=col)
            self.tree_plantilla.column(col, width=w, anchor="center" if col != "Nombre" else "w")
        self.tree_plantilla.pack(fill="both", expand=True)

        # Panel derecho: campo 2D (pizarra)
        panel_der = tk.Frame(self.tab_tactica, bg="#0f172a")
        panel_der.pack(side="right", fill="both", padx=10, pady=10)

        tk.Label(panel_der, text="Pizarra Táctica Titular (En Tiempo Real)", fg="#38bdf8", bg="#0f172a", font=("Segoe UI", 11, "bold")).pack(pady=(0, 5))
        self.canvas_pizarra = tk.Canvas(panel_der, width=460, height=520, bg="#15803d", highlightthickness=2, highlightbackground="white")
        self.canvas_pizarra.pack()

    def dibujar_campo_base(self, canvas, w, h):
        """Limpio el lienzo y pinto un campo con líneas, áreas y franjas de césped."""
        canvas.delete("all")
        # Franjas de césped
        for i in range(0, w, 46):
            color = "#166534" if (i // 46) % 2 == 0 else "#15803d"
            canvas.create_rectangle(i, 0, i + 46, h, fill=color, outline="")
        # Líneas de cal
        canvas.create_rectangle(15, 15, w - 15, h - 15, outline="white", width=2)
        canvas.create_line(w // 2, 15, w // 2, h - 15, fill="white", width=2)
        canvas.create_oval(w // 2 - 50, h // 2 - 50, w // 2 + 50, h // 2 + 50, outline="white", width=2)
        # Áreas
        canvas.create_rectangle(15, h // 2 - 95, 85, h // 2 + 95, outline="white", width=2)
        canvas.create_rectangle(w - 85, h // 2 - 95, w - 15, h // 2 + 95, outline="white", width=2)

    def dibujar_pizarra_tactica(self):
        """Coloco en el campo a los titulares según su posición y las coordenadas de la formación elegida."""
        w, h = 460, 520
        self.dibujar_campo_base(self.canvas_pizarra, w, h)
        coords = COORDENADAS_FORMACION.get(self.mi_equipo.formacion, COORDENADAS_FORMACION["4-4-2"])

        # Ordenar titulares por línea para colocarlos en su coordenada correspondiente
        orden_pos = {"POR": 0, "DEF": 1, "CEN": 2, "DEL": 3}
        titulares_ord = sorted(self.mi_equipo.alineacion_titular, key=lambda j: orden_pos.get(j.posicion, 99))

        for idx, jug in enumerate(titulares_ord[:len(coords)]):
            cx = int(coords[idx][0] * w)
            cy = int(coords[idx][1] * h)
            color_ficha = "#f59e0b" if jug.posicion == "POR" else "#2563eb"
            self.canvas_pizarra.create_oval(cx - 18, cy - 18, cx + 18, cy + 18, fill=color_ficha, outline="white", width=2)
            self.canvas_pizarra.create_text(cx, cy, text=str(jug.rendimiento_real()), fill="white", font=("Segoe UI", 9, "bold"))
            # Etiqueta con el nombre
            self.canvas_pizarra.create_rectangle(cx - 42, cy + 20, cx + 42, cy + 36, fill="#0f172a", outline="")
            self.canvas_pizarra.create_text(cx, cy + 28, text=jug.nombre[:11], fill="white", font=("Segoe UI", 8, "bold"))

    # --- PESTAÑA 2: DÍA DE PARTIDO Y MAPA DE TIROS (xG SHOT MAP) ---
    def construir_tab_partido(self):
        """Preparo la crónica del partido y el lienzo del mapa de remates."""
        top_partido = tk.Frame(self.tab_partido, bg="#1e293b", pady=12, padx=20)
        top_partido.pack(fill="x", padx=10, pady=10)

        self.lbl_cartel_partido = tk.Label(top_partido, text="PRÓXIMO PARTIDO", fg="white", bg="#1e293b", font=("Segoe UI", 15, "bold"))
        self.lbl_cartel_partido.pack(side="left")

        self.btn_jugar = tk.Button(top_partido, text="▶️ SIMULAR JORNADA EN VIVO", bg="#16a34a", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=18, pady=6, command=self.jugar_jornada_gui)
        self.btn_jugar.pack(side="right")

        cuerpo = tk.Frame(self.tab_partido, bg="#0f172a")
        cuerpo.pack(fill="both", expand=True, padx=10)

        # Izquierda: crónica
        frame_cronica = tk.Frame(cuerpo, bg="#0f172a")
        frame_cronica.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(frame_cronica, text="Crónica y Eventos en Directo", fg="#38bdf8", bg="#0f172a", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 5))

        self.txt_cronica = tk.Text(frame_cronica, bg="#1e293b", fg="white", font=("Consolas", 10), height=22, padx=10, pady=10)
        self.txt_cronica.pack(fill="both", expand=True)

        # Derecha: shot map
        frame_shotmap = tk.Frame(cuerpo, bg="#0f172a")
        frame_shotmap.pack(side="right", fill="both")
        tk.Label(frame_shotmap, text="Mapa de Tiros xG (Tamaño = Valor xG | Dorado = Gol)", fg="#facc15", bg="#0f172a", font=("Segoe UI", 10, "bold")).pack(pady=(0, 5))

        self.canvas_shotmap = tk.Canvas(frame_shotmap, width=480, height=440, bg="#15803d", highlightthickness=2, highlightbackground="white")
        self.canvas_shotmap.pack()
        self.dibujar_campo_base(self.canvas_shotmap, 480, 440)

    # --- PESTAÑA 3: CLASIFICACIÓN Y MÉTRICAS xG ---
    def construir_tab_liga(self):
        """Creo las tablas de clasificación y de goleadores con las columnas analíticas."""
        tk.Label(self.tab_liga, text="Clasificación General y Rendimiento Esperado (xG)", fg="#38bdf8", bg="#0f172a", font=("Segoe UI", 13, "bold")).pack(pady=10)
        cols = ("Pos", "Equipo", "PTS", "PJ", "GF", "GC", "DG", "xG Favor", "xG Contra", "Diferencial (G - xG)")
        self.tree_liga = ttk.Treeview(self.tab_liga, columns=cols, show="headings", height=8)
        for col in cols:
            self.tree_liga.heading(col, text=col)
            self.tree_liga.column(col, width=100 if col != "Equipo" else 160, anchor="center")
        self.tree_liga.pack(fill="x", padx=20, pady=5)

        tk.Label(self.tab_liga, text="Tabla de Goleadores (Pichichi vs xG Individual)", fg="#facc15", bg="#0f172a", font=("Segoe UI", 13, "bold")).pack(pady=(20, 10))
        cols_gol = ("Jugador", "Equipo", "Pos", "Goles", "xG Acumulado", "Efectividad (G - xG)")
        self.tree_goleadores = ttk.Treeview(self.tab_liga, columns=cols_gol, show="headings", height=9)
        for col in cols_gol:
            self.tree_goleadores.heading(col, text=col)
            self.tree_goleadores.column(col, width=140, anchor="center")
        self.tree_goleadores.pack(fill="x", padx=20, pady=5)

    # --- PESTAÑA 4: MERCADO Y CENTRO TÉCNICO ---
    def construir_tab_mercado(self):
        """Construyo los controles de entrenamiento y la tabla de jugadores disponibles."""
        frame_sup = tk.Frame(self.tab_mercado, bg="#1e293b", padx=15, pady=12)
        frame_sup.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_sup, text="Centro Técnico:", fg="white", bg="#1e293b", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        tk.Button(frame_sup, text="💤 Descansar Plantilla (-30% Cansancio)", bg="#0284c7", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=12, pady=4, command=self.accion_descansar).pack(side="left", padx=10)
        tk.Button(frame_sup, text="💪 Entrenamiento Intensivo (+Media / +15% Cansancio)", bg="#7c3aed", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=12, pady=4, command=self.accion_entrenar).pack(side="left", padx=10)

        tk.Label(self.tab_mercado, text="Jugadores Disponibles en el Mercado de Fichajes", fg="#38bdf8", bg="#0f172a", font=("Segoe UI", 12, "bold")).pack(pady=5)
        cols_merc = ("Nombre", "Pos", "Media", "Precio", "Salario/Jornada")
        self.tree_mercado = ttk.Treeview(self.tab_mercado, columns=cols_merc, show="headings", height=10)
        for col in cols_merc:
            self.tree_mercado.heading(col, text=col)
            self.tree_mercado.column(col, width=160, anchor="center")
        self.tree_mercado.pack(fill="x", padx=20, pady=5)

        btn_fichar = tk.Button(self.tab_mercado, text="✍️ Fichar Jugador Seleccionado", bg="#16a34a", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=16, pady=8, command=self.fichar_jugador)
        btn_fichar.pack(pady=10)

    # --- LÓGICA DE EVENTOS Y SIMULACIÓN ---
    def cambiar_tactica(self, event=None):
        """Leo las opciones seleccionadas, rehago el once y refresco lo que ve el usuario."""
        self.mi_equipo.formacion = self.combo_form.get()
        self.mi_equipo.estilo = self.combo_estilo.get()
        self.mi_equipo.convocar_once_automatico()
        self.actualizar_todo()

    def autoconvocar(self):
        """Vuelvo a elegir automáticamente el once y actualizo las tablas y la pizarra."""
        self.mi_equipo.convocar_once_automatico()
        self.actualizar_todo()

    def accion_descansar(self):
        """Reduce el cansancio, mejora la moral y comunica el resultado antes de refrescar la pantalla."""
        for j in self.mi_equipo.plantilla:
            j.cansancio = max(0, j.cansancio - 30)
            j.moral = min(100, j.moral + 10)
        messagebox.showinfo("Centro Técnico", "La plantilla ha descansado y recupera frescura física.")
        self.actualizar_todo()

    def accion_entrenar(self):
        """Entreno a los jugadores aptos, aplico fatiga y muestro qué medias han mejorado."""
        mejorados = []
        for j in self.mi_equipo.plantilla:
            if j.lesionado == 0:
                j.cansancio = min(100, j.cansancio + 15)
                if random.random() < 0.18 and j.media < 92:
                    j.media += 1
                    mejorados.append(f"{j.nombre} ({j.media})")
        msg = "Entrenamiento completado."
        if mejorados:
            msg += "\n¡Han subido su media!: " + ", ".join(mejorados)
        messagebox.showinfo("Centro Técnico", msg)
        self.actualizar_todo()

    def fichar_jugador(self):
        """Compruebo que haya selección y presupuesto suficiente antes de transferir jugador y dinero."""
        sel = self.tree_mercado.selection()
        if not sel:
            messagebox.showwarning("Mercado", "Selecciona primero un jugador de la tabla.")
            return
        idx = self.tree_mercado.index(sel[0])
        jug = self.mercado[idx]
        if self.mi_equipo.presupuesto >= jug.precio:
            self.mi_equipo.presupuesto -= jug.precio
            self.mi_equipo.agregar_jugador(jug)
            self.mercado.pop(idx)
            self.mi_equipo.convocar_once_automatico()
            messagebox.showinfo("Fichaje Cerrado", f"¡{jug.nombre} se incorpora al {self.mi_equipo.nombre}!")
            self.actualizar_todo()
        else:
            messagebox.showerror("Presupuesto Insuficiente", "No tienes fondos suficientes para esta operación.")

    def jugar_jornada_gui(self):
        """Simulo todos los encuentros de la jornada una vez y actualizo el marcador, la crónica y las tablas."""
        if self.jornada_actual >= len(self.calendario):
            messagebox.showinfo("Fin de Temporada", "¡La temporada ha concluido! Revisa la clasificación final.")
            return

        self.txt_cronica.delete("1.0", tk.END)
        self.dibujar_campo_base(self.canvas_shotmap, 480, 440)

        mapa_eq = {e.nombre: e for e in self.equipos}
        partidos = self.calendario[self.jornada_actual]

        self.txt_cronica.insert(tk.END, f"=== JORNADA {self.jornada_actual + 1} ===\n\n")

        for loc_nom, vis_nom in partidos:
            loc, vis = mapa_eq[loc_nom], mapa_eq[vis_nom]
            es_nuestro = (loc == self.mi_equipo or vis == self.mi_equipo)
            self.simular_partido_motor(loc, vis, dibujar_mapa=es_nuestro)

        self.jornada_actual += 1
        self.actualizar_todo()

    def simular_partido_motor(self, local, vis, dibujar_mapa=False):
        """Resuelvo un partido y aplico sus consecuencias deportivas, financieras y físicas; dibujo los remates del partido del usuario."""
        atq_l, def_l = local.calcular_fuerzas()
        atq_v, def_v = vis.calcular_fuerzas()
        atq_l += 3
        def_l += 3

        g_l, g_v = 0, 0
        xg_l, xg_v = 0.0, 0.0

        if dibujar_mapa:
            self.txt_cronica.insert(tk.END, f"⚽ {local.nombre} vs {vis.nombre}\n" + "-" * 42 + "\n")

        for minuto in [12, 24, 37, 45, 56, 68, 79, 89]:
            if random.random() < 0.82:
                ataca_local = random.random() < (atq_l / (atq_l + atq_v))
                eq_atq = local if ataca_local else vis
                rematador = random.choice(eq_atq.alineacion_titular)

                # Generar xG y resultado del tiro
                es_clara = random.random() < 0.25
                xg_tiro = round(random.uniform(0.30, 0.55) if es_clara else random.uniform(0.04, 0.22), 2)
                prob_gol = min(0.85, xg_tiro * (rematador.rendimiento_real() / 72))
                es_gol = random.random() < prob_gol

                rematador.xg_acumulado = round(rematador.xg_acumulado + xg_tiro, 2)
                if ataca_local:
                    xg_l += xg_tiro
                    if es_gol:
                        g_l += 1
                else:
                    xg_v += xg_tiro
                    if es_gol:
                        g_v += 1

                if es_gol:
                    rematador.goles += 1

                if dibujar_mapa:
                    # Shot map (local ataca a la derecha, visitante a la izquierda)
                    radio = int(5 + xg_tiro * 22)
                    if ataca_local:
                        sx = random.randint(340, 445) if es_clara else random.randint(280, 380)
                    else:
                        sx = random.randint(35, 140) if es_clara else random.randint(100, 200)
                    sy = random.randint(135, 305) if es_clara else random.randint(75, 365)

                    color_tiro = "#facc15" if es_gol else ("#38bdf8" if ataca_local else "#f87171")
                    self.canvas_shotmap.create_oval(sx - radio, sy - radio, sx + radio, sy + radio, fill=color_tiro, outline="white", width=2)

                    if es_gol:
                        self.txt_cronica.insert(tk.END, f"[{minuto}'] ¡GOOOL de {rematador.nombre} ({eq_atq.nombre})! (xG: {xg_tiro:.2f})\n")
                    elif xg_tiro >= 0.28:
                        self.txt_cronica.insert(tk.END, f"[{minuto}'] ¡Ocasión clara fallada por {rematador.nombre}! (xG: {xg_tiro:.2f})\n")

        # Actualizar clasificación y economía
        local.pj += 1
        vis.pj += 1
        local.gf += g_l
        local.gc += g_v
        vis.gf += g_v
        vis.gc += g_l
        local.xg_f = round(local.xg_f + xg_l, 2)
        local.xg_c = round(local.xg_c + xg_v, 2)
        vis.xg_f = round(vis.xg_f + xg_v, 2)
        vis.xg_c = round(vis.xg_c + xg_l, 2)

        if g_l > g_v:
            local.puntos += 3
        elif g_l < g_v:
            vis.puntos += 3
        else:
            local.puntos += 1
            vis.puntos += 1

        recaudacion = int(local.aforo * random.uniform(0.75, 0.95)) * 20
        local.presupuesto += recaudacion - local.masa_salarial()
        vis.presupuesto -= vis.masa_salarial()

        for eq in [local, vis]:
            for j in eq.alineacion_titular:
                j.cansancio = min(100, j.cansancio + random.randint(12, 22))

        if dibujar_mapa:
            self.txt_cronica.insert(tk.END, f"\n🏁 FINAL: {local.nombre} {g_l} - {g_v} {vis.nombre}\n")
            self.txt_cronica.insert(tk.END, f"📊 xG Partido: {local.nombre} {xg_l:.2f} vs {xg_v:.2f} {vis.nombre}\n")
            self.txt_cronica.insert(tk.END, "💶 Balance Jornada (Taquilla - Salarios)\n\n")
        else:
            self.txt_cronica.insert(tk.END, f"• Otro resultado: {local.nombre} {g_l} - {g_v} {vis.nombre} (xG: {xg_l:.2f}-{xg_v:.2f})\n")

    def actualizar_todo(self):
        # Cabecera
        """Sincronizo cabecera, próximo rival, plantilla, pizarra, clasificación, goleadores y mercado con el estado actual."""
        j_txt = f"Jornada {self.jornada_actual + 1}/{len(self.calendario)}" if self.jornada_actual < len(self.calendario) else "Fin de Liga"
        self.lbl_info_top.config(text=f"📅 {j_txt}   |   💶 Presupuesto: {self.mi_equipo.presupuesto:,} €   |   Salarios: {self.mi_equipo.masa_salarial():,} €/j")

        # Próximo rival en pestaña Partido
        if self.jornada_actual < len(self.calendario):
            for loc, vis in self.calendario[self.jornada_actual]:
                if self.mi_equipo.nombre in (loc, vis):
                    self.lbl_cartel_partido.config(text=f"Jornada {self.jornada_actual + 1}:  {loc}  vs  {vis}")
        else:
            self.lbl_cartel_partido.config(text="🏆 TEMPORADA FINALIZADA")

        # Tabla plantilla
        for row in self.tree_plantilla.get_children():
            self.tree_plantilla.delete(row)
        for j in self.mi_equipo.plantilla:
            est = "Titular ⭐" if j in self.mi_equipo.alineacion_titular else "Suplente"
            self.tree_plantilla.insert("", tk.END, values=(j.posicion, j.nombre, j.media, j.rendimiento_real(), f"{j.cansancio}%", j.goles, f"{j.xg_acumulado:.2f}", est))

        # Pizarra 2D
        self.dibujar_pizarra_tactica()

        # Tabla clasificación
        for row in self.tree_liga.get_children():
            self.tree_liga.delete(row)
        ord_eq = sorted(self.equipos, key=lambda e: (e.puntos, e.gf - e.gc), reverse=True)
        for idx, eq in enumerate(ord_eq):
            dg = eq.gf - eq.gc
            dif_xg = eq.gf - eq.xg_f
            self.tree_liga.insert("", tk.END, values=(idx + 1, eq.nombre, eq.puntos, eq.pj, eq.gf, eq.gc, f"{dg:+d}", f"{eq.xg_f:.2f}", f"{eq.xg_c:.2f}", f"{dif_xg:+.2f}"))

        # Tabla goleadores
        for row in self.tree_goleadores.get_children():
            self.tree_goleadores.delete(row)
        todos_j = [(j, e.nombre) for e in self.equipos for j in e.plantilla if j.goles > 0 or j.xg_acumulado >= 0.3]
        todos_j.sort(key=lambda x: (x[0].goles, x[0].xg_acumulado), reverse=True)
        for j, eq_nom in todos_j[:10]:
            self.tree_goleadores.insert("", tk.END, values=(j.nombre, eq_nom, j.posicion, j.goles, f"{j.xg_acumulado:.2f}", f"{j.goles - j.xg_acumulado:+.2f}"))

        # Tabla mercado
        for row in self.tree_mercado.get_children():
            self.tree_mercado.delete(row)
        for j in self.mercado:
            self.tree_mercado.insert("", tk.END, values=(j.nombre, j.posicion, j.media, f"{j.precio:,} €", f"{j.salario:,} €"))


if __name__ == "__main__":
    root = tk.Tk()
    app = FootballManagerGUI(root)
    root.mainloop()
