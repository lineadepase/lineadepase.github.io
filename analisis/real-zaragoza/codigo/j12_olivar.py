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
                     castillo=(640, 8.6), estrellas=900, nube=0),
    "panoramica": dict(W=1672, H=941, gy=520, vp=1290, hb=1130, camino=175, r0=62, sep=178, curva=-95,
                       luces=[752, 688, 636, 597], etq_px=[38, 34, 30, 27],
                       castillo=(1290, 6.2), estrellas=1300, nube=0),
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
    """Castillo de Santa Catalina: recinto alargado sobre una cresta que baja hacia un lado, iluminado
    desde abajo con focos cálidos, y Jaén extendida al pie, con sus calles y ventanas encendidas."""
    cx, k = c["castillo"]
    f = k / 7.5
    gy = c["gy"]
    S = 3
    W, H = im.size
    base_y = gy + 6

    def PX(dx, h):
        return ((cx + dx * f) * S, (base_y - h * f) * S)

    cresta = [(-700, -30), (-600, 6), (-500, 22), (-430, 58), (-370, 96), (-310, 130), (-250, 160), (-215, 184),
              (-120, 190), (0, 190), (115, 188), (160, 168), (215, 140), (280, 118), (350, 100), (430, 84),
              (500, 58), (580, 30), (650, 6), (700, -30)]
    suave = []
    for (x0, h0), (x1, h1) in zip(cresta, cresta[1:]):
        for t in (0, .33, .66):
            suave.append((x0 + (x1 - x0) * t + rnd.uniform(-5, 5), h0 + (h1 - h0) * t + rnd.uniform(-4, 4)))
    suave.append(cresta[-1])

    def alto_cresta(dx):
        for (x0, h0), (x1, h1) in zip(cresta, cresta[1:]):
            if x0 <= dx <= x1:
                return h0 + (h1 - h0) * (dx - x0) / (x1 - x0)
        return 0

    roca = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ImageDraw.Draw(roca).polygon([PX(x, h) for x, h in suave], fill=(13, 18, 40, 255))
    # luz de luna en el filo de la cresta
    filo = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ImageDraw.Draw(filo).line([PX(x, h) for x, h in suave if -330 < x < 330], fill=(70, 88, 140, 150), width=3 * S // 2)
    # recinto
    cast = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(cast)
    pared = (34, 28, 46, 255)
    P0 = 188

    def bloque(x0, x1, h, almenas=True, base=P0):
        d.rectangle((*PX(x0, base + h), *PX(x1, base - 40)), fill=pared)
        if almenas:
            n = max(2, int((x1 - x0) / 9))
            w = (x1 - x0) / (2 * n - 1)
            for j in range(n):
                d.rectangle((*PX(x0 + 2 * j * w, base + h + 6), *PX(x0 + 2 * j * w + w, base + h + 1)), fill=pared)

    bloque(-215, 115, 24)                          # muralla
    bloque(-236, -192, 58)                         # torre izquierda
    bloque(-172, -128, 36, False)                  # capilla
    d.polygon([PX(-176, P0 + 36), PX(-124, P0 + 36), PX(-150, P0 + 62)], fill=pared)
    bloque(-118, -92, 44)
    bloque(-72, -18, 112)                          # torre del homenaje
    bloque(22, 56, 48)
    bloque(92, 130, 56)
    # lienzo de muralla que baja por la cresta
    xs = list(range(115, 230, 6))
    arriba = [PX(x, alto_cresta(x) + 17) for x in xs]
    abajo = [PX(x, alto_cresta(x) - 6) for x in reversed(xs)]
    d.polygon(arriba + abajo, fill=pared)
    for x in range(121, 225, 14):
        d.rectangle((*PX(x, alto_cresta(x) + 22), *PX(x + 6, alto_cresta(x) + 16)), fill=pared)
    bloque(196, 222, 30, True, base=alto_cresta(209))
    # ciudad al pie: casas, algunas con tejado, siguiendo la base de la cresta
    ciudad = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    dc = ImageDraw.Draw(ciudad)
    casas = []
    dx = -690
    while dx < 690:
        w = rnd.uniform(9, 20)
        e = abs(dx) / 690
        h = rnd.uniform(10, 34) * (1 - .5 * e) + 4
        casas.append((dx, w, h))
        dx += w * rnd.uniform(.8, 1.05)
    for dx, w, h in casas:
        yb = -4
        dc.rectangle((*PX(dx, yb + h), *PX(dx + w, yb - 34)), fill=(16, 21, 44, 255))
        if rnd.random() < .45:
            dc.polygon([PX(dx - 1, yb + h), PX(dx + w + 1, yb + h), PX(dx + w / 2, yb + h + w * .35)], fill=(16, 21, 44, 255))
    roca = roca.resize((W, H), Image.LANCZOS)
    filo = filo.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1))
    cast = cast.resize((W, H), Image.LANCZOS)
    ciudad = ciudad.resize((W, H), Image.LANCZOS)
    # focos: la muralla se ilumina desde abajo con luz cálida y se pierde hacia arriba
    ytop = base_y - (P0 + 120) * f
    yfin = base_y - (P0 - 10) * f
    rampa = np.clip((np.arange(H) - ytop) / (yfin - ytop), 0, 1) ** 1.6 * .5
    alfa = np.asarray(cast.getchannel("A")).astype(np.float32) / 255 * rampa[:, None]
    cal = np.zeros((H, W, 4), np.uint8)
    cal[..., 0], cal[..., 1], cal[..., 2] = 238, 150, 92
    cal[..., 3] = (alfa * 255).astype(np.uint8)
    cal = Image.fromarray(cal, "RGBA")
    # ventanas (ranuras) y luces de la ciudad
    luz = vacia(c)
    dl = ImageDraw.Draw(luz)
    ranuras = [(-58, 270), (-44, 270), (-58, 244), (-44, 244), (-51, 218), (-205, 228), (-110, 214), (40, 222),
               (112, 226), (-150, 205), (205, 150)]
    for dx, h in ranuras:
        x, y = cx + dx * f, base_y - h * f
        dl.rectangle((x - 1.5 * f, y - 4.5 * f, x + 1.5 * f, y + 4.5 * f), fill=(255, 205, 120, 255))
    for dx, w, h in casas:
        for _ in range(int(w / 6)):
            if rnd.random() < .5:
                x = cx + (dx + rnd.uniform(1, w - 1)) * f
                y = base_y - rnd.uniform(-2, h) * f
                dl.rectangle((x, y, x + 1.8, y + 2.2), fill=rnd.choice([(255, 190, 100, 255), (255, 214, 140, 255), (255, 168, 80, 255)]))
    calles = vacia(c)
    dcl = ImageDraw.Draw(calles)
    for fila in range(6):
        yy = base_y + 10 - fila * 6.5 * f
        dx = -700
        while dx < 700:
            p_ = max(.08, .9 - abs(dx) / 760)
            if rnd.random() < p_:
                dcl.ellipse((cx + dx * f, yy, cx + dx * f + 2.3, yy + 2.3), fill=rnd.choice([(255, 196, 110, 255), (255, 176, 84, 255), (255, 220, 150, 255)]))
            dx += rnd.uniform(5, 9)
    glow = vacia(c)
    ImageDraw.Draw(glow).ellipse((cx - 720 * f, gy - 48, cx + 720 * f, gy + 16), fill=(255, 150, 80, 82))
    glow = glow.filter(ImageFilter.GaussianBlur(26))
    im = Image.alpha_composite(im, glow)
    im = Image.alpha_composite(im, cast)
    im = Image.alpha_composite(im, cal)
    im = Image.alpha_composite(im, roca)
    # luz de luna en las laderas: más clara arriba y a la izquierda, con algo de textura de roca
    yy = np.arange(H)[:, None].astype(np.float32)
    xx = np.arange(W)[None, :].astype(np.float32)
    cima_y = base_y - 190 * f
    vert = np.clip(1 - (yy - cima_y) / (base_y - cima_y), 0, 1) ** 1.3
    horiz = np.clip(1.1 - (xx - (cx - 500 * f)) / (1000 * f), .15, 1)
    ruido = np.random.default_rng(7).random((H // 6 + 1, W // 6 + 1)).astype(np.float32)
    ruido = np.asarray(Image.fromarray((ruido * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) / 255
    luna = np.zeros((H, W, 4), np.uint8)
    luna[..., 0], luna[..., 1], luna[..., 2] = 74, 96, 156
    a_roca = np.asarray(roca.getchannel("A")).astype(np.float32) / 255
    luna[..., 3] = (a_roca * vert * horiz * (.16 + .26 * ruido) * 255).astype(np.uint8)
    im = Image.alpha_composite(im, Image.fromarray(luna, "RGBA"))
    im = Image.alpha_composite(im, filo)
    im = Image.alpha_composite(im, ciudad)
    brillo = luz.filter(ImageFilter.GaussianBlur(2.2))
    im = Image.alpha_composite(im, calles.filter(ImageFilter.GaussianBlur(1.6)))
    im = Image.alpha_composite(im, calles)
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
    surcos = vacia(c)
    d = ImageDraw.Draw(surcos)
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
            d.polygon(pts, fill=(4, 9, 24, 20))
        off += c["sep"]
        i += 1
    # el campo nace del pie de la ciudad: sin línea de horizonte dura
    al = np.asarray(base.getchannel('A')).copy()
    for i in range(70):
        al[gy + i] = (al[gy + i] * (i / 70) ** 1.4).astype(np.uint8)
    base.putalpha(Image.fromarray(al))
    im = Image.alpha_composite(im, base)
    im = Image.alpha_composite(im, surcos.filter(ImageFilter.GaussianBlur(1.6)))
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
        r = c["r0"] * u * rnd.uniform(.72, 1.28)
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
        db.line([(0, gy + i), (W, gy + i)], fill=(165, 150, 200, int(92 * (1 - i / 190) ** 1.7)))
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
