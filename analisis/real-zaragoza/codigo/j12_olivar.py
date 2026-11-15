"""
Portada de la J12 (Real Jaén 0-4 Real Zaragoza), dibujada entera por código:
noche estrellada sobre la sierra, el castillo de Santa Catalina sobre su risco con Jaén a los pies,
un olivar en hileras y, sobre el camino que sube hacia el castillo, cuatro luces: una por gol,
cada una con su minuto.

Se hace todo aquí (cielo incluido) para que la imagen tenga un único estilo y no dependa del
modelo anónimo de Pollinations, que no sabe dibujar olivos ni castillos.
Necesita Pillow, numpy, fontTools y brotli (para leer las fuentes woff2 de recursos/fuentes).

Uso (desde la raíz del repositorio):
    python analisis/real-zaragoza/codigo/j12_olivar.py vertical   salida.jpg
    python analisis/real-zaragoza/codigo/j12_olivar.py panoramica salida.jpg
"""
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

FUENTES = Path(__file__).resolve().parent / "recursos" / "fuentes"
MINUTOS = ["45+3'", "54'", "78'", "80'"]          # goles.csv, partido 12, de menor a mayor minuto

CONF = {
    "vertical": dict(W=1080, H=1350, gy=800, vp=640, hb=1560, camino=250, r0=88, sep=250, curva=-150,
                     luces=[1118, 1012, 932, 872], etq_px=[56, 50, 44, 40],
                     castillo=(640, 7.5), estrellas=900, nube=0),
    "panoramica": dict(W=1672, H=941, gy=520, vp=1290, hb=1130, camino=175, r0=62, sep=178, curva=-95,
                       luces=[752, 688, 636, 597], etq_px=[38, 34, 30, 27],
                       castillo=(1290, 5.5), estrellas=1300, nube=0),
}


def fuente(nombre, px):
    ttf = Path("/tmp") / f"{nombre}.ttf"
    if not ttf.exists():
        from fontTools.ttLib import TTFont
        f = TTFont(FUENTES / f"{nombre}.woff2")
        f.flavor = None
        f.save(ttf)
    return ImageFont.truetype(str(ttf), px)


def mezcla(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def centro(c, u):
    """Eje del camino: curva suave que sube hacia el castillo."""
    return c["vp"] + c["curva"] * u * math.sin(2.4 * u + 0.5)


def vacia(c):
    return Image.new("RGBA", (c["W"], c["H"]), (0, 0, 0, 0))


# ------------------------------------------------------------------ cielo y sierra
def cielo(c, rnd):
    W, H, gy = c["W"], c["H"], c["gy"]
    y = np.linspace(0, 1, gy)[:, None]
    arriba, medio, horizonte, calido = (5, 10, 30), (14, 28, 68), (52, 72, 128), (150, 128, 168)
    img = np.zeros((H, W, 3), np.float32)
    for yy in range(gy):
        t = yy / gy
        col = mezcla(arriba, medio, t / .55) if t < .55 else mezcla(medio, horizonte, (t - .55) / .3)
        if t > .82:
            col = mezcla(horizonte, calido, ((t - .82) / .18) ** 1.4)
        img[yy, :, :] = col
    # resplandor de la ciudad tras el castillo
    cx = c["castillo"][0]
    yy, xx = np.mgrid[0:gy, 0:W]
    r = np.hypot((xx - cx) / (W * .55), (yy - gy) / (gy * .34))
    glow = np.clip(1 - r, 0, 1) ** 2.2
    img[:gy] += glow[..., None] * np.array([70, 62, 80], np.float32)
    base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
    # estrellas: más densas arriba, de brillo variable
    est = vacia(c)
    d = ImageDraw.Draw(est)
    for _ in range(c["estrellas"]):
        x = rnd.uniform(0, W)
        yv = gy * rnd.random() ** 1.7
        a = int(60 + 190 * rnd.random() ** 2.5)
        a = int(a * (1 - .8 * yv / gy))
        r_ = .55 + 1.1 * rnd.random() ** 6
        d.ellipse((x - r_, yv - r_, x + r_, yv + r_), fill=(215, 228, 255, a))
    for _ in range(14):
        x, yv = rnd.uniform(0, W), gy * rnd.random() ** 1.5 * .8
        d.ellipse((x - 2.4, yv - 2.4, x + 2.4, yv + 2.4), fill=(210, 225, 255, 90))
    est = est.filter(ImageFilter.GaussianBlur(.6))
    halo = vacia(c)
    dh = ImageDraw.Draw(halo)
    for _ in range(14):
        x, yv = rnd.uniform(0, W), gy * rnd.random() ** 1.5 * .8
        dh.ellipse((x - 5, yv - 5, x + 5, yv + 5), fill=(160, 190, 255, 38))
    base = Image.alpha_composite(base, halo.filter(ImageFilter.GaussianBlur(4)))
    return Image.alpha_composite(base, est)


def sierra(im, c):
    W, H, gy = c["W"], c["H"], c["gy"]
    for k, (alt, amp, col, fase) in enumerate([(gy - 96, 70, (70, 82, 132), 0.4), (gy - 52, 52, (46, 58, 104), 1.9),
                                               (gy - 18, 34, (28, 40, 80), 3.3)]):
        capa = vacia(c)
        d = ImageDraw.Draw(capa)
        pts = [(0, gy + 80)]
        for x in range(0, W + 6, 6):
            t = x / W
            y = alt - amp * (0.55 + 0.45 * math.sin(t * 4.3 + fase)) - amp * .3 * math.sin(t * 11 + fase * 2) \
                - amp * .12 * math.sin(t * 29 + fase)
            pts.append((x, y))
        pts.append((W, gy + 80))
        d.polygon(pts, fill=col + (255,))
        im = Image.alpha_composite(im, capa)
        niebla = vacia(c)
        dn = ImageDraw.Draw(niebla)
        for i in range(46):
            dn.line([(0, gy - 22 * (2 - k) - 46 + i + 28), (W, gy - 22 * (2 - k) - 46 + i + 28)],
                    fill=(150, 150, 195, int(34 * (1 - abs(i - 23) / 23))))
        im = Image.alpha_composite(im, niebla)
    return im


# ------------------------------------------------------------------ castillo, risco y ciudad
def castillo(im, c, rnd):
    cx, k = c["castillo"]
    gy = c["gy"]
    S = 3
    W, H = im.size
    capa = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    roca = (12, 17, 38, 255)
    u = k * 2.6                                          # módulo de construcción
    def P(x, y):
        return (x * S, y * S)
    # risco: perfil escarpado y asimétrico
    base_y = gy + 6
    ancho = 17 * u
    perfil = [(-1.55, 0), (-1.25, -.12), (-1.02, -.1), (-.88, -.38), (-.78, -.7), (-.7, -1.04), (-.4, -1.1), (.3, -1.12), (.66, -1.08), (.74, -.8), (.86, -.58), (1.0, -.34), (1.25, -.18), (1.6, 0)]
    alto = 10 * u
    pts = [P(cx + px * ancho, base_y + py * alto) for px, py in perfil]
    pts = [P(cx - 1.7 * ancho, base_y + 30)] + pts + [P(cx + 1.7 * ancho, base_y + 30)]
    d.polygon(pts, fill=roca)
    cima = base_y - 1.1 * alto + 6
    xl, xr = cx - .55 * ancho, cx + .55 * ancho

    def bloque(x0, x1, y0, y1, almenas=True):
        d.rectangle((*P(x0, y0), *P(x1, y1)), fill=roca)
        if almenas:
            n = max(2, int((x1 - x0) / (u * .6)))
            w = (x1 - x0) / (2 * n - 1)
            for j in range(n):
                d.rectangle((*P(x0 + 2 * j * w, y0 - u * .5), *P(x0 + 2 * j * w + w, y0 + 1)), fill=roca)

    # muralla continua y torres (Santa Catalina: recinto alargado con torre del homenaje a un lado)
    bloque(xl, xr, cima - 1.5 * u, cima + 4)
    bloque(xl - 1.2 * u, xl + 1.7 * u, cima - 5.2 * u, cima + 4)               # torre izquierda
    bloque(xl + 4.8 * u, xl + 6.5 * u, cima - 3.6 * u, cima + 4)
    bloque(xl + 8.5 * u, xl + 12.8 * u, cima - 3.0 * u, cima + 4)               # cuerpo central bajo
    bloque(xr - 6.5 * u, xr - 1.2 * u, cima - 8.4 * u, cima + 4)                # torre del homenaje
    bloque(xr - .2 * u, xr + 2.2 * u, cima - 4.2 * u, cima + 4)
    d.polygon([P(xl + 8.2 * u, cima - 3.0 * u - .5 * u), P(xl + 13.1 * u, cima - 3.0 * u - .5 * u), P(xl + 10.65 * u, cima - 5.4 * u)], fill=roca)  # capilla
    d.rectangle((*P(xr - 4.0 * u, cima - 10.6 * u), *P(xr - 3.8 * u, cima - 8.8 * u)), fill=roca)                  # asta
    d.rectangle((*P(xr - 4.6 * u, cima - 10.1 * u), *P(xr - 3.2 * u, cima - 10.0 * u)), fill=roca)
    # ciudad al pie: casas bajas apiñadas con tejados
    for i in range(70):
        t = i / 69
        x = cx + (t - .5) * 3.1 * ancho
        e = abs(t - .5) * 2
        h = (1.4 + rnd.random() * 2.6) * u * (1 - .45 * e) * .75
        w = (1.1 + rnd.random() * 1.6) * u * .75
        y_base = base_y + 18 - e ** 2 * 6 * u * .3
        d.rectangle((*P(x - w / 2, y_base - h), *P(x + w / 2, y_base + 30)), fill=(15, 21, 44, 255))
        if rnd.random() < .5:
            d.polygon([P(x - w / 2 - 1, y_base - h), P(x + w / 2 + 1, y_base - h), P(x, y_base - h - w * .35)], fill=(15, 21, 44, 255))
    capa = capa.resize((W, H), Image.LANCZOS)
    # luz cálida en ventanas del castillo y de la ciudad
    luz = vacia(c)
    dl = ImageDraw.Draw(luz)
    ventanas = [(xl + .2 * u, cima - 4.0 * u), (xl + .2 * u, cima - 2.4 * u), (xr - 5.2 * u, cima - 7.0 * u),
                (xr - 3.2 * u, cima - 7.0 * u), (xr - 5.2 * u, cima - 5.2 * u), (xr - 3.2 * u, cima - 5.2 * u),
                (xr - 4.2 * u, cima - 3.2 * u), (xr + .9 * u, cima - 2.8 * u), (xl + 10.4 * u, cima - 1.4 * u),
                (xl + 5.6 * u, cima - 2.0 * u), (xl + 14.3 * u, cima - .3 * u)]
    for x, y in ventanas:
        dl.rectangle((x - u * .16, y - u * .36, x + u * .16, y + u * .36), fill=(255, 196, 108, 255))
    for i in range(190):
        t = rnd.random()
        x = cx + (t - .5) * 3.0 * ancho
        e = abs(t - .5) * 2
        y = base_y + 18 - rnd.random() * (3.0 * u) * (1 - .5 * e) * .8
        if y > gy + 22:
            continue
        a = rnd.choice([(255, 190, 100, 255), (255, 214, 140, 255), (255, 170, 80, 255)])
        dl.rectangle((x, y, x + u * .2, y + u * .24), fill=a)
    # bruma cálida de la ciudad, contraluz del risco y brillo de ventanas
    cal = vacia(c)
    ImageDraw.Draw(cal).ellipse((cx - 1.5 * ancho, gy - 20 * u * .6, cx + 1.5 * ancho, gy + 10), fill=(255, 160, 90, 60))
    cal = cal.filter(ImageFilter.GaussianBlur(u * 3))
    brillo = luz.filter(ImageFilter.GaussianBlur(u * .9))
    im = Image.alpha_composite(im, cal)
    im = Image.alpha_composite(im, capa)
    im = Image.alpha_composite(im, brillo)
    im = Image.alpha_composite(im, brillo)
    return Image.alpha_composite(im, luz)


# ------------------------------------------------------------------ suelo, camino y olivos
def suelo(im, c):
    W, H, gy = c["W"], c["H"], c["gy"]
    vx = c["vp"]
    hb = c["hb"]
    arr = np.zeros((H - gy, W, 3), np.float32)
    for i in range(H - gy):
        u = min(1, i / (hb - gy))
        arr[i] = mezcla((46, 58, 100), (7, 12, 28), u ** .6)
    capa = Image.fromarray(arr.astype(np.uint8)).convert("RGBA")
    base = vacia(c)
    base.paste(capa, (0, gy))
    d = ImageDraw.Draw(base)
    # surcos entre hileras: franjas que convergen en el punto de fuga
    off = c["camino"] * 1.45
    i = 0
    while off < 5 * W:
        for sg in (-1, 1):
            pts = []
            for k in range(0, 41):
                u = .005 + k / 40 * 1.5
                y = gy + (hb - gy) * u
                pts.append((centro(c, u) + sg * off * u, y))
            ancho = c["sep"] * .34
            for k in range(40, -1, -1):
                u = .005 + k / 40 * 1.5
                y = gy + (hb - gy) * u
                pts.append((centro(c, u) + sg * (off + ancho) * u, y))
            d.polygon(pts, fill=(4, 9, 24, 28))
        off += c["sep"]
        i += 1
    im = Image.alpha_composite(im, base)
    # camino iluminado por la luna
    cam = vacia(c)
    dc = ImageDraw.Draw(cam)
    for y in range(gy, H):
        u = (y - gy) / (hb - gy)
        ancho = c["camino"] * u + 2
        xc = centro(c, u)
        col = mezcla((98, 116, 162), (30, 42, 74), u ** .75)
        dc.line([(xc - ancho, y), (xc + ancho, y)], fill=col + (255,))
        dc.line([(xc - ancho, y), (xc - ancho * .9, y)], fill=(12, 20, 44, 255))
        dc.line([(xc + ancho * .9, y), (xc + ancho, y)], fill=(12, 20, 44, 255))
        for sg in (-1, 1):
            xr = xc + sg * ancho * .36
            dc.line([(xr - 7 * u, y), (xr + 7 * u, y)], fill=mezcla(col, (10, 16, 36), .55) + (255,))
    return Image.alpha_composite(im, cam.filter(ImageFilter.GaussianBlur(.6)))


def olivos(im, c, rnd):
    W, H, gy = c["W"], c["H"], c["gy"]
    hb = c["hb"]
    arb = vacia(c)
    da = ImageDraw.Draw(arb)
    filas = []
    off = c["camino"] * 1.45
    while off < 5 * W:
        filas += [off, -off]
        off += c["sep"]
    arboles = []
    for fila in filas:
        u = .018
        while u < 1.5:
            arboles.append((u * rnd.uniform(.97, 1.03), fila))
            u *= 1.14
    arboles.sort()
    for u, fila in arboles:
        y = gy + (hb - gy) * u
        x = centro(c, u) + (fila + c["sep"] * .2) * u + rnd.uniform(-.14, .14) * c["sep"] * u
        r = c["r0"] * u * rnd.uniform(.8, 1.2)
        if x < -r * 2 or x > W + r * 2 or y - r * 1.7 > H or rnd.random() < .05:
            continue
        lejos = max(0, 1 - u * 1.9)
        bruma = mezcla((0, 0, 0), (0, 0, 0), 0)
        tono = rnd.uniform(-.12, .12)
        sombra = mezcla((3, 7, 18), (38, 50, 92), lejos)
        da.ellipse((x - r * .75, y - r * .12, x + r * 1.55, y + r * .26), fill=sombra + (255,))     # sombra hacia la derecha
        da.polygon([(x - r * .09, y + r * .02), (x + r * .09, y + r * .02), (x + r * .05, y - r * .6), (x - r * .12, y - r * .6)],
                   fill=mezcla((9, 12, 24), (38, 50, 92), lejos) + (255,))
        copa_oscura = mezcla((14, 34, 52), (52, 66, 116), lejos + tono)
        copa_media = mezcla((34, 66, 80), (66, 84, 134), lejos + tono)
        copa_clara = mezcla((104, 142, 150), (92, 112, 160), lejos)
        formas = []
        for _ in range(9):
            a = rnd.uniform(0, 2 * math.pi)
            rr = rnd.uniform(0, .62)
            formas.append((math.cos(a) * rr * .95, -1.05 + math.sin(a) * rr * .55, rnd.uniform(.38, .6), rnd.uniform(.28, .42)))
        for dx, dy, rx, ry in formas:
            da.ellipse((x + (dx - rx) * r, y + (dy - ry) * r * .8, x + (dx + rx) * r, y + (dy + ry) * r * .8), fill=copa_oscura + (255,))
        for dx, dy, rx, ry in formas:
            da.ellipse((x + (dx - rx * .78) * r - r * .06, y + (dy - ry * .75) * r * .8 - r * .05,
                        x + (dx + rx * .55) * r - r * .06, y + (dy + ry * .35) * r * .8 - r * .05), fill=copa_media + (255,))
        for dx, dy, rx, ry in formas[:5]:
            da.ellipse((x + (dx - rx * .5) * r - r * .1, y + (dy - ry * .55) * r * .8 - r * .1,
                        x + (dx + rx * .1) * r - r * .1, y + (dy - ry * .05) * r * .8 - r * .1), fill=copa_clara + (255,))
    im = Image.alpha_composite(im, arb.filter(ImageFilter.GaussianBlur(.55)))
    # bruma baja entre los olivos, más densa en la lejanía
    br = vacia(c)
    db = ImageDraw.Draw(br)
    for i in range(190):
        db.line([(0, gy + i), (W, gy + i)], fill=(120, 130, 190, int(78 * (1 - i / 190) ** 1.8)))
    return Image.alpha_composite(im, br)


# ------------------------------------------------------------------ luces y etiquetas
def luces(im, c):
    gy, hb = c["gy"], c["hb"]
    puntos = []
    for y in c["luces"]:
        u = (y - gy) / (hb - gy)
        puntos.append((centro(c, u), y, u))
    capa = vacia(c)
    for x, y, u in puntos:
        r = c["r0"] * u * .8
        # luz que cae sobre el camino y los olivos cercanos
        for rx, ry, a, col in [(7.0, 1.6, 34, (70, 130, 255)), (4.2, 1.0, 60, (130, 185, 255)), (2.2, .5, 110, (225, 238, 255))]:
            e = vacia(c)
            ImageDraw.Draw(e).ellipse((x - r * rx, y + r * 1.15 - r * ry, x + r * rx, y + r * 1.15 + r * ry), fill=col + (a,))
            capa = Image.alpha_composite(capa, e.filter(ImageFilter.GaussianBlur(r * .55)))
        haz = vacia(c)
        ImageDraw.Draw(haz).polygon([(x - r * .35, y), (x + r * .35, y), (x + r * 1.1, y - r * 8), (x - r * 1.1, y - r * 8)], fill=(130, 180, 255, 50))
        capa = Image.alpha_composite(capa, haz.filter(ImageFilter.GaussianBlur(r * .6)))
    for x, y, u in puntos:
        r = c["r0"] * u * .8
        halo = vacia(c)
        ImageDraw.Draw(halo).ellipse((x - r * 3.4, y - r * 3.4, x + r * 3.4, y + r * 3.4), fill=(70, 130, 255, 120))
        nucleo = vacia(c)
        dn = ImageDraw.Draw(nucleo)
        dn.ellipse((x - r * 1.3, y - r * 1.3, x + r * 1.3, y + r * 1.3), fill=(165, 202, 255, 255))
        dn.ellipse((x - r * .92, y - r * .92, x + r * .92, y + r * .92), fill=(248, 252, 255, 255))
        dest = vacia(c)
        dd = ImageDraw.Draw(dest)
        dd.polygon([(x - r * 5.6, y), (x, y - r * .2), (x + r * 5.6, y), (x, y + r * .2)], fill=(205, 228, 255, 150))
        dd.polygon([(x, y - r * 4), (x + r * .15, y), (x, y + r * 4), (x - r * .15, y)], fill=(205, 228, 255, 120))
        capa = Image.alpha_composite(capa, halo.filter(ImageFilter.GaussianBlur(r * 1.2)))
        capa = Image.alpha_composite(capa, dest.filter(ImageFilter.GaussianBlur(r * .12)))
        capa = Image.alpha_composite(capa, nucleo.filter(ImageFilter.GaussianBlur(r * .16)))
    im = Image.alpha_composite(im, capa)
    # etiquetas: a un lado de cada luz, con un trazo fino; alternan de lado para no amontonarse
    lados = [1, -1, 1, -1]
    for (x, y, u), minuto, lado, px in zip(puntos, MINUTOS, lados, c["etq_px"]):
        f = fuente("big-shoulders-display-latin-800-normal", px)
        r = c["r0"] * u * .8
        d = ImageDraw.Draw(im)
        ancho = d.textlength(minuto, font=f)
        tx = x + r * 2.2 + 16 if lado > 0 else x - r * 2.2 - 16 - ancho
        ty = y - px * .56
        sombra = vacia(c)
        ImageDraw.Draw(sombra).text((tx, ty), minuto, font=f, fill=(0, 0, 0, 230))
        im = Image.alpha_composite(im, sombra.filter(ImageFilter.GaussianBlur(6)))
        d = ImageDraw.Draw(im)
        d.text((tx, ty), minuto, font=f, fill=(232, 241, 255, 255))
        x0 = x + (r * 1.7 if lado > 0 else -r * 1.7)
        x1 = tx - 8 if lado > 0 else tx + ancho + 8
        d.line([(x0, y), (x1, y)], fill=(175, 208, 255, 160), width=2)
    return im


def acabado(im, rnd):
    """Viñeta, un toque de resplandor y grano fino para que todo parezca una sola imagen."""
    W, H = im.size
    rgb = im.convert("RGB")
    brillo = rgb.point(lambda v: max(0, v - 170) * 3)
    brillo = brillo.filter(ImageFilter.GaussianBlur(W / 90))
    rgb = ImageChops.screen(rgb, brillo.point(lambda v: int(v * .55)))
    vin = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vin).ellipse((-W * .2, -H * .08, W * 1.2, H * 1.08), fill=255)
    vin = vin.filter(ImageFilter.GaussianBlur(W / 5)).point(lambda v: 140 + v * 115 // 255)
    rgb = Image.composite(rgb, Image.new("RGB", (W, H), (3, 6, 16)), vin)
    ruido = np.random.default_rng(12).normal(0, 4.2, (H, W, 1)).astype(np.float32)
    arr = np.clip(np.asarray(rgb).astype(np.float32) + ruido, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def construir(formato, salida):
    c = CONF[formato]
    rnd = random.Random(12)
    im = cielo(c, rnd)
    im = sierra(im, c)
    im = castillo(im, c, rnd)
    im = suelo(im, c)
    im = olivos(im, c, rnd)
    im = luces(im, c)
    acabado(im, rnd).save(salida, quality=93)


if __name__ == "__main__":
    construir(sys.argv[1], sys.argv[2])
    print("guardado", sys.argv[2])
