"""Esqueleto de juego de gestión y táctica de fútbol (Pygame).

Arquitectura: máquina de estados. Cada pantalla es una clase con
handle_event / update / draw. El Juego guarda el estado actual y cambia
de pantalla con cambiar_estado("NOMBRE").

Ejecutar:  pip install pygame && python main.py
"""
import random
import sys

import pygame

ANCHO, ALTO = 400, 700
FPS = 60

# Paleta oscura tipo analista deportivo
FONDO = (13, 17, 23)
PANEL = (22, 30, 42)
TEXTO = (230, 237, 243)
TEXTO_SUAVE = (139, 148, 158)
ACENTO = (46, 204, 113)
ACENTO_HOVER = (88, 230, 150)
AVISO = (241, 196, 15)


class Boton:
    """Botón rectangular con efecto hover."""

    def __init__(self, texto, rect, destino=None):
        self.texto = texto
        self.rect = pygame.Rect(rect)
        self.destino = destino  # nombre del estado al que navega (opcional)

    def draw(self, pantalla, fuente):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        color = ACENTO_HOVER if hover else ACENTO
        pygame.draw.rect(pantalla, color, self.rect, border_radius=12)
        img = fuente.render(self.texto, True, FONDO)
        pantalla.blit(img, img.get_rect(center=self.rect.center))

    def clicado(self, evento):
        return (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
                and self.rect.collidepoint(evento.pos))


def texto_centrado(pantalla, texto, fuente, color, y):
    img = fuente.render(texto, True, color)
    pantalla.blit(img, img.get_rect(center=(ANCHO // 2, y)))


class Estado:
    """Clase base de pantalla."""

    def __init__(self, juego):
        self.juego = juego
        self.botones = []

    def al_entrar(self):
        """Se llama cada vez que se activa la pantalla."""

    def handle_event(self, evento):
        for b in self.botones:
            if b.clicado(evento):
                self.al_pulsar(b)

    def al_pulsar(self, boton):
        if boton.destino:
            self.juego.cambiar_estado(boton.destino)

    def update(self, dt):
        pass

    def draw(self, pantalla):
        for b in self.botones:
            b.draw(pantalla, self.juego.f_media)


class Menu(Estado):
    def __init__(self, juego):
        super().__init__(juego)
        self.botones = [Boton("EMPEZAR", (50, 520, 300, 60), "MERCADO")]

    def draw(self, pantalla):
        texto_centrado(pantalla, "LÍNEA DE PASE", self.juego.f_titulo, TEXTO, 250)
        texto_centrado(pantalla, "Gestión y táctica de fútbol",
                       self.juego.f_pequena, TEXTO_SUAVE, 300)
        super().draw(pantalla)


class Mercado(Estado):
    """Fichajes estilo Tinder: aceptar / descartar jugadores."""

    NOMBRES = ["Iker Soto", "Marc Vidal", "Pablo Ruiz", "Dani Ortega", "Hugo Lara"]
    POSICIONES = ["POR", "DEF", "MED", "DEL"]

    def __init__(self, juego):
        super().__init__(juego)
        self.botones = [
            Boton("✗ Pasar", (30, 520, 160, 55)),
            Boton("✓ Fichar", (210, 520, 160, 55)),
            Boton("IR A PLANTILLA", (50, 610, 300, 55), "PLANTILLA"),
        ]
        self.candidato = self.nuevo()

    def nuevo(self):
        return {"nombre": random.choice(self.NOMBRES),
                "pos": random.choice(self.POSICIONES),
                "media": random.randint(55, 90)}

    def al_pulsar(self, boton):
        if boton.texto.startswith("✓"):
            self.juego.plantilla.append(self.candidato)
            self.candidato = self.nuevo()
        elif boton.texto.startswith("✗"):
            self.candidato = self.nuevo()
        else:
            super().al_pulsar(boton)

    def draw(self, pantalla):
        texto_centrado(pantalla, "MERCADO", self.juego.f_grande, TEXTO, 50)
        tarjeta = pygame.Rect(40, 100, 320, 380)
        pygame.draw.rect(pantalla, PANEL, tarjeta, border_radius=20)
        c = self.candidato
        texto_centrado(pantalla, c["nombre"], self.juego.f_grande, TEXTO, 300)
        texto_centrado(pantalla, c["pos"], self.juego.f_media, TEXTO_SUAVE, 345)
        texto_centrado(pantalla, f"Media {c['media']}", self.juego.f_media, AVISO, 390)
        super().draw(pantalla)


class Plantilla(Estado):
    def __init__(self, juego):
        super().__init__(juego)
        self.botones = [
            Boton("ENTRENAR", (50, 540, 300, 55)),
            Boton("JUGAR PARTIDO", (50, 610, 300, 55), "PARTIDO"),
        ]

    def al_pulsar(self, boton):
        if boton.texto == "ENTRENAR":
            for j in self.juego.plantilla:
                j["media"] = min(99, j["media"] + random.randint(0, 2))
        else:
            super().al_pulsar(boton)

    def draw(self, pantalla):
        texto_centrado(pantalla, "PLANTILLA", self.juego.f_grande, TEXTO, 50)
        y = 100
        for j in self.juego.plantilla[-10:]:
            fila = pygame.Rect(30, y, 340, 40)
            pygame.draw.rect(pantalla, PANEL, fila, border_radius=8)
            pantalla.blit(self.juego.f_pequena.render(
                f"{j['pos']}  {j['nombre']}", True, TEXTO), (42, y + 10))
            m = self.juego.f_pequena.render(str(j["media"]), True, AVISO)
            pantalla.blit(m, (350 - m.get_width(), y + 10))
            y += 46
        if not self.juego.plantilla:
            texto_centrado(pantalla, "Aún no has fichado a nadie",
                           self.juego.f_pequena, TEXTO_SUAVE, 300)
        super().draw(pantalla)


class Partido(Estado):
    def __init__(self, juego):
        super().__init__(juego)
        self.botones = [
            Boton("TOMAR DECISIÓN", (50, 540, 300, 55)),
            Boton("VOLVER AL MENÚ", (50, 610, 300, 55), "MENU"),
        ]
        self.log = []

    def al_entrar(self):
        self.log = ["Comienza el partido"]

    def al_pulsar(self, boton):
        if boton.texto == "TOMAR DECISIÓN":
            self.log.append(random.choice([
                "Cambio táctico: línea defensiva adelantada",
                "Sustitución: entra un delantero fresco",
                "Presión alta tras pérdida",
                "Juego por bandas"]))
            self.log = self.log[-8:]
        else:
            super().al_pulsar(boton)

    def draw(self, pantalla):
        texto_centrado(pantalla, "DÍA DE PARTIDO", self.juego.f_grande, TEXTO, 50)
        pygame.draw.rect(pantalla, PANEL, (30, 100, 340, 400), border_radius=16)
        for i, linea in enumerate(self.log):
            pantalla.blit(self.juego.f_pequena.render(linea, True, TEXTO),
                          (42, 115 + i * 36))
        super().draw(pantalla)


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Línea de Pase")
        self.reloj = pygame.time.Clock()
        self.f_titulo = pygame.font.SysFont("arial", 44, bold=True)
        self.f_grande = pygame.font.SysFont("arial", 30, bold=True)
        self.f_media = pygame.font.SysFont("arial", 22, bold=True)
        self.f_pequena = pygame.font.SysFont("arial", 16)
        self.plantilla = []  # datos compartidos entre pantallas
        self.estados = {
            "MENU": Menu(self), "MERCADO": Mercado(self),
            "PLANTILLA": Plantilla(self), "PARTIDO": Partido(self),
        }
        self.estado = self.estados["MENU"]
        self.ejecutando = True

    def cambiar_estado(self, nombre):
        self.estado = self.estados[nombre]
        self.estado.al_entrar()

    def run(self):
        """Bucle principal: eventos -> actualizar -> dibujar."""
        while self.ejecutando:
            dt = self.reloj.tick(FPS) / 1000
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.ejecutando = False
                else:
                    self.estado.handle_event(evento)
            self.estado.update(dt)
            self.pantalla.fill(FONDO)
            self.estado.draw(self.pantalla)
            pygame.display.flip()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Juego().run()
