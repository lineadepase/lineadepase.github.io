"""
Portada de la J12 (Real Jaén 0-4 Real Zaragoza): olivar nocturno, castillo de Jaén en lo alto y
cuatro luces sobre el camino, una por gol, con el minuto de cada uno.

El modelo anónimo de Pollinations no sabe dibujar olivos, castillos ni objetos concretos, así que
solo se usa para el cielo estrellado; todo lo que hay por debajo del horizonte se dibuja aquí.
Necesita Pillow, fontTools y brotli (para leer las fuentes woff2 de recursos/fuentes).

Uso (desde la raíz del repositorio):
    python analisis/real-zaragoza/codigo/j12_olivar.py vertical   cielo.jpg salida.jpg
    python analisis/real-zaragoza/codigo/j12_olivar.py panoramica cielo.jpg salida.jpg
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FUENTES = Path(__file__).resolve().parent / "recursos" / "fuentes"
MINUTOS = ["45+3'", "54'", "78'", "80'"]          # goles.csv, partido 12, de menor a mayor minuto

CONF = {
    "vertical": dict(W=1080, H=1350, hy=722, vp=(600, 735), hb=1500, camino=235, r0=82, sep=235, curva=-120,
                     luces=[1112, 992, 893, 822], etq_lado=[1, -1, 1, -1], etq_px=[54, 48, 42, 38],
                     castillo=(600, 640, 1.55)),
    "panoramica": dict(W=1672, H=941, hy=495, vp=(1250, 505), hb=1110, camino=170, r0=60, sep=170, curva=-90,
                       luces=[748, 686, 636, 595], etq_lado=[1, -1, 1, -1], etq_px=[36, 32, 29, 26],
                       castillo=(1250, 428, 1.15)),
}


def fuente(nombre, px):
    ttf = Path("/tmp") / f"{nombre}.ttf"
    if not ttf.exists():
        from fontTools.ttLib import TTFont
        f = TTFont(FUENTES / f"{nombre}.woff2")
        f.flavor = None
        f.save(ttf)
    return ImageFont.truetype(str(ttf), px)


def centro(c, u):
    """Eje del camino: una curva suave que se acerca al castillo."""
    return c["vp"][0] + c["curva"] * u * math.sin(2.6 * u + 0.4)


def mezcla(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def colinas(im, c):
    W, H, hy = c["W"], c["H"], c["hy"]
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for base, amp, col, fase in [(hy - 40, 34, (31, 46, 84), 0.6), (hy - 12, 26, (21, 34, 66), 2.1)]:
        pts = [(0, H)]
        for x in range(0, W + 8, 8):
            y = base - amp * (0.5 + 0.5 * math.sin(x / W * 5.1 + fase)) - 12 * math.sin(x / W * 13 + fase)
            pts.append((x, y))
        pts.append((W, H))
        d.polygon(pts, fill=col + (255,))
    return Image.alpha_composite(im, capa)


def castillo(im, c):
    cx, cy, k = c["castillo"]
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    roca = (10, 16, 36, 255)
    ancho_colina = 430 * k / 1.4
    base = cy + 62 * k / 1.4
    pts = [(cx - ancho_colina, c["hy"] + 70)]
    for i in range(61):
        t = i / 60
        pts.append((cx + (t - 0.5) * 2 * ancho_colina, base + 92 * k / 1.4 * (abs(2 * t - 1) ** 1.7)))
    pts.append((cx + ancho_colina, c["hy"] + 70))
    d.polygon(pts, fill=roca)
    u = 11 * k

    def torre(x0, ancho, alto):
        d.rectangle((x0, base - alto, x0 + ancho, base + 4), fill=roca)
        n = max(2, int(ancho / (u * 0.55)))
        w = ancho / (2 * n - 1)
        for j in range(n):
            d.rectangle((x0 + 2 * j * w, base - alto - u * .45, x0 + 2 * j * w + w, base - alto + 1), fill=roca)

    torre(cx - 11.5 * u, 23 * u, 2.1 * u)
    torre(cx - 2.6 * u, 5.2 * u, 6.6 * u)
    torre(cx - 9.5 * u, 3.4 * u, 4.4 * u)
    torre(cx + 5.8 * u, 3.6 * u, 4.1 * u)
    torre(cx + 9.4 * u, 2.6 * u, 3.3 * u)
    torre(cx - 13.0 * u, 2.4 * u, 3.0 * u)
    fade = Image.new("L", im.size, 255)
    df = ImageDraw.Draw(fade)
    for y in range(int(c["hy"] - 4), int(c["hy"] + 70)):
        df.line([(0, y), (im.size[0], y)], fill=max(0, int(255 * (1 - (y - c["hy"] + 4) / 74))))
    df.rectangle((0, int(c["hy"] + 70), im.size[0], im.size[1]), fill=0)
    capa.putalpha(Image.composite(capa.getchannel("A"), Image.new("L", im.size, 0), fade))
    luz = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dl = ImageDraw.Draw(luz)
    for x, y in [(cx - 1.3 * u, base - 4.4 * u), (cx + .9 * u, base - 4.4 * u), (cx - 1.3 * u, base - 2.8 * u),
                 (cx - 8.3 * u, base - 2.7 * u), (cx + 7.0 * u, base - 2.6 * u), (cx + 3.2 * u, base - 1.2 * u),
                 (cx - 5.0 * u, base - 1.2 * u), (cx + 10.3 * u, base - 1.7 * u), (cx - 12.2 * u, base - 1.8 * u)]:
        dl.rectangle((x - u * .16, y - u * .36, x + u * .16, y + u * .36), fill=(255, 205, 120, 255))
    halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse((cx - 22 * u, base - 11 * u, cx + 22 * u, base + 3 * u), fill=(120, 150, 220, 70))
    halo = halo.filter(ImageFilter.GaussianBlur(u * 3))
    im = Image.alpha_composite(im, halo)
    im = Image.alpha_composite(im, capa)
    im = Image.alpha_composite(im, luz.filter(ImageFilter.GaussianBlur(u * .7)))
    return Image.alpha_composite(im, luz)


def suelo(im, c):
    W, H, hy = c["W"], c["H"], c["hy"]
    vx, vy = c["vp"]
    hb = c["hb"]
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for y in range(hy, H):
        u = min(1, (y - vy) / (hb - vy))
        d.line([(0, y), (W, y)], fill=mezcla((34, 50, 86), (6, 12, 26), max(0, u) ** 0.7) + (255,))
    for y in range(vy, H):
        u = (y - vy) / (hb - vy)
        ancho = c["camino"] * u
        col = mezcla((74, 92, 134), (22, 32, 58), u ** 0.8)
        xc = centro(c, u)
        d.line([(xc - ancho, y), (xc + ancho, y)], fill=col + (255,))
        for sgn in (-1, 1):
            xr = xc + sgn * ancho * 0.42
            d.line([(xr - 9 * u, y), (xr + 9 * u, y)], fill=mezcla(col, (8, 14, 30), .55) + (255,))
    return Image.alpha_composite(im, capa)


def olivos(im, c, rnd):
    W, H, hy = c["W"], c["H"], c["hy"]
    vx, vy = c["vp"]
    hb = c["hb"]
    arb = Image.new("RGBA", im.size, (0, 0, 0, 0))
    da = ImageDraw.Draw(arb)
    filas = []
    off = c["camino"] * 1.5
    while off < 5 * W:
        filas += [off, -off]
        off += c["sep"] * rnd.uniform(.9, 1.15)
    arboles = []
    for fila in filas:
        u = 0.02
        while u < 1.45:
            arboles.append((u * rnd.uniform(.96, 1.04), fila))
            u *= 1.13
    arboles.sort()
    for u, fila in arboles:
        y = vy + (hb - vy) * u
        x = centro(c, u) + fila * u + rnd.uniform(-.18, .18) * c["sep"] * u
        r = c["r0"] * u * rnd.uniform(.85, 1.15)
        if x < -r * 2 or x > W + r * 2 or y - r * 1.5 > H:
            continue
        niebla = max(0, 1 - u * 2.2) * .55
        da.ellipse((x - r * 1.15, y - r * .16, x + r * 1.15, y + r * .26), fill=mezcla((4, 8, 18), (30, 44, 76), niebla) + (255,))
        da.rectangle((x - r * .07, y - r * .55, x + r * .07, y + r * .03), fill=mezcla((10, 14, 26), (30, 44, 76), niebla) + (255,))
        copa = [(0.0, -0.95, 0.78, 0.55), (-.5, -.78, .55, .42), (.5, -.8, .55, .42), (-.28, -1.18, .5, .4),
                (.3, -1.15, .5, .4), (0.0, -1.38, .42, .34)]
        for dx, dy, rx, ry in copa:
            cx_, cy_ = x + dx * r, y + dy * r * .72
            da.ellipse((cx_ - rx * r, cy_ - ry * r, cx_ + rx * r, cy_ + ry * r), fill=mezcla((22, 42, 62), (46, 68, 104), niebla) + (255,))
        for dx, dy, rx, ry in copa[3:]:
            cx_, cy_ = x + (dx - .12) * r, y + (dy - .06) * r * .72
            da.ellipse((cx_ - rx * r * .62, cy_ - ry * r * .5, cx_ + rx * r * .62, cy_ + ry * r * .4),
                       fill=mezcla((92, 130, 140), (70, 96, 140), niebla) + (255,))
        for _ in range(int(2 + 3 * min(1, u))):
            px, py = x + rnd.uniform(-.9, .9) * r, y + rnd.uniform(-1.35, -.7) * r * .72
            da.ellipse((px - r * .07, py - r * .05, px + r * .07, py + r * .05), fill=mezcla((140, 170, 190), (80, 100, 150), niebla) + (255,))
    return Image.alpha_composite(im, arb.filter(ImageFilter.GaussianBlur(.7)))


def bruma(im, c):
    W, hy, vy = c["W"], c["hy"], c["vp"][1]
    bruma = Image.new("RGBA", im.size, (0, 0, 0, 0))
    db = ImageDraw.Draw(bruma)
    for i in range(70):
        db.line([(0, vy + i), (W, vy + i)], fill=(150, 165, 210, int(70 * (1 - i / 70) ** 2)))
    return Image.alpha_composite(im, bruma)


def luces(im, c):
    vx, vy = c["vp"]
    hb = c["hb"]
    puntos = [(centro(c, (y - vy) / (hb - vy)), y, (y - vy) / (hb - vy)) for y in c["luces"]]
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    for x, y, u in puntos:
        r = c["r0"] * u * 0.62
        for rx, ry, a, col in [(5.0, 1.1, 40, (80, 140, 255)), (3.2, .75, 70, (140, 190, 255)), (1.8, .4, 120, (220, 235, 255))]:
            e = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(e).ellipse((x - r * rx, y + r * .9 - r * ry, x + r * rx, y + r * .9 + r * ry), fill=col + (a,))
            capa = Image.alpha_composite(capa, e.filter(ImageFilter.GaussianBlur(r * .5)))
        haz = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(haz).polygon([(x - r * .3, y), (x + r * .3, y), (x + r * 1.0, y - r * 7), (x - r * 1.0, y - r * 7)], fill=(130, 180, 255, 55))
        capa = Image.alpha_composite(capa, haz.filter(ImageFilter.GaussianBlur(r * .5)))
    for x, y, u in puntos:
        r = c["r0"] * u * 0.62
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(halo).ellipse((x - r * 3.1, y - r * 3.1, x + r * 3.1, y + r * 3.1), fill=(70, 130, 255, 110))
        nucleo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dn = ImageDraw.Draw(nucleo)
        dn.ellipse((x - r * 1.25, y - r * 1.25, x + r * 1.25, y + r * 1.25), fill=(170, 205, 255, 255))
        dn.ellipse((x - r * .9, y - r * .9, x + r * .9, y + r * .9), fill=(245, 250, 255, 255))
        destello = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(destello)
        dd.polygon([(x - r * 5.2, y), (x, y - r * .22), (x + r * 5.2, y), (x, y + r * .22)], fill=(200, 225, 255, 150))
        dd.polygon([(x, y - r * 3.6), (x + r * .16, y), (x, y + r * 3.6), (x - r * .16, y)], fill=(200, 225, 255, 120))
        capa = Image.alpha_composite(capa, halo.filter(ImageFilter.GaussianBlur(r * 1.1)))
        capa = Image.alpha_composite(capa, destello.filter(ImageFilter.GaussianBlur(r * .12)))
        capa = Image.alpha_composite(capa, nucleo.filter(ImageFilter.GaussianBlur(r * .18)))
    im = Image.alpha_composite(im, capa)
    for (x, y, u), minuto, lado, px in zip(puntos, MINUTOS, c["etq_lado"], c["etq_px"]):
        f = fuente("big-shoulders-display-latin-800-normal", px)
        r = c["r0"] * u * 0.62
        d = ImageDraw.Draw(im)
        ancho = d.textlength(minuto, font=f)
        tx = x + r * 2.4 + 14 if lado > 0 else x - r * 2.4 - 14 - ancho
        ty = y - px * .55
        sombra = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sombra).text((tx, ty), minuto, font=f, fill=(0, 0, 0, 200))
        im = Image.alpha_composite(im, sombra.filter(ImageFilter.GaussianBlur(5)))
        d = ImageDraw.Draw(im)
        d.text((tx, ty), minuto, font=f, fill=(226, 238, 255, 255))
        x0 = x + (r * 1.9 if lado > 0 else -r * 1.9)
        x1 = tx - 7 if lado > 0 else tx + ancho + 7
        d.line([(x0, y), (x1, y)], fill=(170, 205, 255, 150), width=2)
    return im


def acabado(im, rnd):
    """Viñeta y un grano muy fino para que todo parezca una sola imagen."""
    W, H = im.size
    vin = Image.new("L", im.size, 0)
    ImageDraw.Draw(vin).ellipse((-W * .25, -H * .1, W * 1.25, H * 1.1), fill=255)
    vin = vin.filter(ImageFilter.GaussianBlur(W / 6))
    oscuro = Image.new("RGBA", im.size, (3, 6, 16, 255))
    im = Image.composite(im, oscuro, vin.point(lambda v: 150 + v * 105 // 255))
    ruido = Image.effect_noise(im.size, 14).convert("RGBA")
    return Image.blend(im, Image.alpha_composite(im, ruido), 0.05)


def construir(formato, cielo, salida):
    c = CONF[formato]
    rnd = random.Random(12)
    base = Image.open(cielo).convert("RGB")
    if base.size != (c["W"], c["H"]):
        base = base.resize((c["W"], c["H"]), Image.LANCZOS)
    im = base.convert("RGBA")
    im = colinas(im, c)
    im = suelo(im, c)
    im = castillo(im, c)
    im = olivos(im, c, rnd)
    im = bruma(im, c)
    im = luces(im, c)
    im = acabado(im, rnd)
    im.convert("RGB").save(salida, quality=93)


if __name__ == "__main__":
    construir(sys.argv[1], sys.argv[2], sys.argv[3])
    print("guardado", sys.argv[3])
