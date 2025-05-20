import pygame
import math
from funciones_dibujo import dibujar_ficha_estilo_casino, dibujar_ruleta_animada, dibujar_bolita_inicio
from datos_juego import fichas
from config import ANCHO, FONDO, NEGRO, BLANCO, ROJO, fuente, grande

class PantallaInicio:
    def __init__(self, cambiar_pantalla):
        self.cambiar_pantalla = cambiar_pantalla
        self.angulo = 0
        self.tiempo = 0

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.boton_jugar.collidepoint(x, y):
                self.cambiar_pantalla("juego")
            elif self.boton_jugar2.collidepoint(x, y):
                self.cambiar_pantalla("juego2")

    def actualizar(self):
        self.angulo = (self.angulo + 1) % 360
        self.tiempo += 0.05

    def dibujar(self, ventana):
        ventana.fill(FONDO)

        # 🎯 Ruleta y bolita animadas
        centro_ruleta = (ANCHO // 2, 160)
        pygame.draw.circle(ventana, (255, 215, 0), centro_ruleta, 130)
        dibujar_ruleta_animada(ventana, centro_ruleta, 110, self.angulo)
        dibujar_bolita_inicio(ventana, centro_ruleta, 80, -self.angulo * 2)

        # 🎯 Cartel visual "CASINO UCR"
        cartel_ancho = 600
        cartel_alto = 80
        cartel_x = ANCHO // 2 - cartel_ancho // 2
        cartel_y = 300

        # Fondo y borde del cartel
        pygame.draw.rect(ventana, (10, 10, 60), (cartel_x, cartel_y, cartel_ancho, cartel_alto), border_radius=20)
        pygame.draw.rect(ventana, BLANCO, (cartel_x, cartel_y, cartel_ancho, cartel_alto), 4, border_radius=20)

        # 💡 Puntos decorativos tipo luces con simetría perfecta (24 puntos, sin esquinas)
        num_puntos = 24
        espaciado = cartel_ancho // (num_puntos + 1)
        for i in range(1, num_puntos + 1):
            x = cartel_x + i * espaciado
            for y in [cartel_y + 10, cartel_y + cartel_alto - 10]:
                # Resplandor suave
                glow = pygame.Surface((12, 12), pygame.SRCALPHA)
                pygame.draw.circle(glow, (255, 255, 255, 80), (6, 6), 6)
                ventana.blit(glow, (x - 6, y - 6))
                pygame.draw.circle(ventana, BLANCO, (int(x), int(y)), 4)

        # ✨ Texto con resplandor animado
        intensidad = 180 + int(75 * math.sin(self.tiempo))
        color_resplandor = (intensidad, intensidad, 0)
        texto = grande.render("CASINO UCR", True, color_resplandor)
        ventana.blit(texto, (
            cartel_x + cartel_ancho // 2 - texto.get_width() // 2,
            cartel_y + cartel_alto // 2 - texto.get_height() // 2
        ))

        # 🎲 Fichas decorativas
        y_ficha = cartel_y + cartel_alto + 30
        espacio_fichas = 50
        total_ancho_fichas = len(fichas) * espacio_fichas
        start_x = ANCHO // 2 - total_ancho_fichas // 2
        for i, (color, valor) in enumerate(fichas):
            x = start_x + i * espacio_fichas
            dibujar_ficha_estilo_casino(x, y_ficha, color, valor)

        # 📄 Créditos del proyecto
        textos = [
            "Proyecto Métodos Cuantitativos 2025",
            "- Kendall León",
            "- Anderson Umaña",
            "- Nombre 3"
        ]
        for i, txt in enumerate(textos):
            render = fuente.render(txt, True, BLANCO)
            ventana.blit(render, (ANCHO // 2 - render.get_width() // 2, y_ficha + 70 + i * 30))

        # 🎮 Botones
        boton_ancho = 140
        boton_alto = 50
        espacio_entre = 30
        total_ancho_botones = boton_ancho * 2 + espacio_entre
        boton_x1 = ANCHO // 2 - total_ancho_botones // 2
        boton_x2 = boton_x1 + boton_ancho + espacio_entre
        boton_y = y_ficha + 200

        self.boton_jugar = pygame.Rect(boton_x1, boton_y, boton_ancho, boton_alto)
        self.boton_jugar2 = pygame.Rect(boton_x2, boton_y, boton_ancho, boton_alto)

        pygame.draw.rect(ventana, (255, 204, 0), self.boton_jugar, border_radius=12)
        pygame.draw.rect(ventana, (255, 204, 0), self.boton_jugar2, border_radius=12)

        texto_b1 = fuente.render("1 Jugador", True, NEGRO)
        texto_b2 = fuente.render("2 Jugadores", True, NEGRO)

        ventana.blit(texto_b1, (
            self.boton_jugar.centerx - texto_b1.get_width() // 2,
            self.boton_jugar.centery - texto_b1.get_height() // 2
        ))
        ventana.blit(texto_b2, (
            self.boton_jugar2.centerx - texto_b2.get_width() // 2,
            self.boton_jugar2.centery - texto_b2.get_height() // 2
        ))
