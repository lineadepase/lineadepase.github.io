"""Notas consistentes sobre el corte de los datos publicados."""
from datetime import date

def _fecha(fecha):
    return date.fromisoformat(fecha).strftime('%d/%m/%Y')

def nota_corte_grupo(jornada_grupo, fecha_grupo, jornada_zaragoza, fecha_zaragoza):
    grupo = f"Grupo 2: jornada {jornada_grupo} ({_fecha(fecha_grupo)})"
    zaragoza = f"seguimiento individual del Real Zaragoza: jornada {jornada_zaragoza} ({_fecha(fecha_zaragoza)})"
    if jornada_grupo == jornada_zaragoza and fecha_grupo == fecha_zaragoza:
        return f"Datos del grupo y del Zaragoza actualizados hasta la jornada {jornada_grupo} ({_fecha(fecha_grupo)})."
    if jornada_zaragoza > jornada_grupo:
        return f"Datos comparativos del {grupo}. El {zaragoza}; esa jornada todavía no está incluida en la comparación."
    return f"Datos comparativos del {grupo}. El {zaragoza}; los cortes de ambas vistas son distintos."
