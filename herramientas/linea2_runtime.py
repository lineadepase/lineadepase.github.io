"""Compone los scripts de compatibilidad desde módulos compartidos por las áreas."""


def build_runtime(root):
    assets = root / 'assets'
    if not assets.exists():
        return  # Los fixtures de HTML no necesitan generar JavaScript.
    bundles = {
        'linea2.js': ['lab', 'reto', 'studio', 'pasaporte'],
        'linea2-experiencias.js': ['laboratorios', 'temporada'],
        'linea2-cuaderno.js': ['escenarios', 'investigacion'],
    }
    for target, modules in bundles.items():
        text = '// Generado por herramientas/linea2_runtime.py; editar los módulos de área.\n'
        text += '\n'.join((assets / f'linea2-{name}.js').read_text(encoding='utf-8') for name in modules)
        (assets / target).write_text(text, encoding='utf-8')
