"""
Textos de las publicaciones de la simulación.

Como las probabilidades cambian cada jornada, los textos se escriben a partir
de los resultados en lugar de redactarse a mano. Uso, después de ejecutar.py:
    python analisis/grupo2-simulacion/codigo/textos.py
"""
import json
import subprocess
from pathlib import Path

import pandas as pd

ESTUDIO = Path(__file__).resolve().parents[1]
ENLACE = "https://lineadepase.com/proyectos/real-zaragoza/simulacion.html"


def enlace(red, campana="simulacion"):
    """Enlace a la página con la red de origen, para ver en la analítica de qué red llega cada visita."""
    return f"{ENLACE}?utm_source={red}&utm_medium=social&utm_campaign={campana}"


def anterior(jornada):
    """Probabilidades publicadas tras la jornada anterior, leídas del último validacion.json con un corte previo."""
    ruta = "analisis/grupo2-simulacion/documentacion/validacion.json"
    raiz = ESTUDIO.parents[1]
    try:
        commits = subprocess.run(["git", "log", "--format=%H", "--", ruta], cwd=raiz, capture_output=True,
                                 text=True, check=True).stdout.split()
        for commit in commits:
            datos = json.loads(subprocess.run(["git", "show", f"{commit}:{ruta}"], cwd=raiz, capture_output=True,
                                              text=True, check=True).stdout)
            if datos["tras_jornada"] < jornada:
                return datos
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError, KeyError):
        pass
    return None


def cambio(actual, previo):
    """Diferencia en puntos porcentuales, con signo, o cadena vacía si no hay dato anterior."""
    if previo is None:
        return ""
    diferencia = round((actual - previo) * 100)
    return f"{diferencia:+d}" if diferencia else "sin cambios"


def pct(valor):
    return f"{valor * 100:.0f} %"


def main():
    salida = ESTUDIO / "datos" / "salida"
    tabla = pd.read_csv(salida / "probabilidades.csv")
    evolucion = pd.read_csv(salida / "evolucion_zaragoza.csv")
    validacion = json.loads((ESTUDIO / "documentacion" / "validacion.json").read_text(encoding="utf-8"))
    j = validacion["tras_jornada"]
    z = tabla[tabla.equipo == "Real Zaragoza"].iloc[0]
    rivales = tabla[tabla.equipo != "Real Zaragoza"].sort_values("ascenso_o_playoff", ascending=False).head(2)
    inicio = evolucion.iloc[0]
    favorito = z.ascenso_o_playoff >= tabla.ascenso_o_playoff.max()
    lectura = "Es el equipo con más opciones, pero lejos de tenerlo hecho" if favorito else "No es el que más opciones tiene"
    lectura_fb = "Es el equipo con más opciones del grupo, pero" if favorito else "Aun así,"
    if validacion["penalizacion"] >= 16:
        leccion = (f"Con {j} jornadas, la mejor opción es una penalización fuerte: el modelo con fuerzas de equipo "
                   "apenas predice mejor que uno en el que todos son iguales.")
    else:
        leccion = f"Con {j} jornadas, los resultados ya separan a los equipos: la penalización elegida es {validacion['penalizacion']}."
    carpeta = ESTUDIO / "publicaciones"
    carpeta.mkdir(parents=True, exist_ok=True)

    # Cambio respecto a lo publicado tras la jornada anterior (no respecto a la serie recalculada).
    previo = anterior(j)
    previo_z = previo["zaragoza"] if previo else None
    c_directo = cambio(z.ascenso_directo, previo_z["ascenso_directo"] if previo_z else None)
    c_cinco = cambio(z.ascenso_o_playoff, previo_z["ascenso_directo"] + previo_z["playoff"] if previo_z else None)
    if previo_z:
        resumen = (f"El Real Zaragoza asciende directamente en el {pct(z.ascenso_directo)} de las 10.000 temporadas "
                   f"simuladas por Línea de pase ({c_directo} puntos respecto a la jornada anterior) y acaba entre los "
                   f"cinco primeros en el {pct(z.ascenso_o_playoff)} ({c_cinco}).")
    else:
        resumen = (f"El Real Zaragoza asciende directamente en el {pct(z.ascenso_directo)} de las 10.000 temporadas "
                   f"simuladas por Línea de pase y acaba entre los cinco primeros en el {pct(z.ascenso_o_playoff)}.")
    # Carrusel de Instagram y Facebook: la portada es una ilustración creada con IA.
    (carpeta / "instagram.txt").write_text(f"""Simulación del grupo 2 · Tras la jornada {j}

{resumen}

{lectura}: le siguen {rivales.iloc[0].equipo} ({pct(rivales.iloc[0].ascenso_o_playoff)}) y {rivales.iloc[1].equipo} ({pct(rivales.iloc[1].ascenso_o_playoff)}) en opciones de acabar entre los cinco primeros.

Quedan {38 - j} jornadas. Una probabilidad no es un pronóstico: resume lo que puede pasar con los resultados disponibles, no lo que va a pasar.

Desliza para ver cada puesto posible y cómo se ha hecho la simulación.

Método, código y todos los equipos: enlace en la bio.

#RealZaragoza #PrimeraFederacion #AnaliticaDeportiva #LineaDePase

Ilustración creada con IA.
""", encoding="utf-8")

    (carpeta / "facebook.txt").write_text(f"""Simulación del grupo 2 · Tras la jornada {j}

{resumen}

· Primero (ascenso directo): {pct(z.ascenso_directo)}
· Del segundo al quinto (playoff): {pct(z.playoff)}
· Descenso: {pct(z.descenso)}

{lectura_fb} en el {pct(1 - z.ascenso_o_playoff)} de las temporadas simuladas se queda fuera de los cinco primeros. Quedan {38 - j} jornadas. Una probabilidad no es un pronóstico.

Todos los equipos, el método y el código:
{enlace("facebook", "simulacion-semanal")}

Ilustración creada con IA.
""", encoding="utf-8")

    (carpeta / "linkedin.txt").write_text(f"""Con {j} jornadas jugadas, la clasificación dice menos de lo que parece. Línea de pase lo ha medido con una simulación Monte Carlo del grupo 2 de Primera Federación, programada en Python:

· Modelo de Poisson con ataque, defensa y ventaja local (Maher, 1982), ajustado solo con los resultados de los partidos.
· Penalización de las fuerzas hacia la media, elegida con validación cruzada dejando fuera una jornada cada vez. {leccion}
· 10.000 temporadas, con incertidumbre en los parámetros y desempates según el reglamento de la RFEF (puntos y diferencia particular entre empatados, diferencia general, goles a favor).
· Comprobación previa: los resultados tienen que reproducir la clasificación publicada, o el programa se detiene.

Tras la jornada {j}, el Real Zaragoza asciende directamente en el {pct(z.ascenso_directo)} de las simulaciones y acaba entre los cinco primeros en el {pct(z.ascenso_o_playoff)}.

La simulación se actualiza después de cada jornada:
{enlace("linkedin")}

#AnaliticaDeportiva #Python #MonteCarlo #Estadistica #RealZaragoza
""", encoding="utf-8")
    print("Textos escritos en", carpeta.relative_to(ESTUDIO.parents[1]))


if __name__ == "__main__":
    main()
