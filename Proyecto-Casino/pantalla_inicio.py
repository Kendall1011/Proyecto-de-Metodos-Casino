import pygame 
from config import ANCHO, FONDO, NEGRO, BLANCO, fuente, grande
import estado_juego
from estado_juego import EstadoJuego
from funciones_dibujo import dibujar_ruleta_animada, dibujar_bolita_inicio, dibujar_ficha_estilo_casino
from datos_juego import fichas
import math

class PantallaInicio:
    def __init__(self, cambiar_pantalla, mensaje_banca_rota=False):
        self.cambiar_pantalla = cambiar_pantalla
        self.mensaje_banca_rota = mensaje_banca_rota
        self.angulo = 0
        self.tiempo = 0

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.boton_jugar.collidepoint(x, y):
                self.reiniciar_juego(modo_dos_jugadores=False)
                self.cambiar_pantalla("juego")
            elif self.boton_jugar2.collidepoint(x, y):
                self.reiniciar_juego(modo_dos_jugadores=True)
                self.cambiar_pantalla("juego2")

    def reiniciar_juego(self, modo_dos_jugadores):
        estado_juego.dinero_j1 = 100000
        estado_juego.dinero_j2 = 100000 if modo_dos_jugadores else 0
        EstadoJuego.apuestas.clear()
        EstadoJuego.apuesta_anterior.clear()
        EstadoJuego.resultado_final = None
        EstadoJuego.mensaje_resultado = ""
        EstadoJuego.girando = False
        EstadoJuego.velocidad = 0
        EstadoJuego.resultado_guardado = False

    def actualizar(self):
        self.angulo = (self.angulo + 1) % 360
        self.tiempo += 0.1

    def dibujar(self, ventana):
        ventana.fill(FONDO)
        centro_ruleta = (ANCHO // 2, 160)
        pygame.draw.circle(ventana, (255, 215, 0), centro_ruleta, 130)
        dibujar_ruleta_animada(ventana, centro_ruleta, 110, self.angulo)
        dibujar_bolita_inicio(ventana, centro_ruleta, 80, -self.angulo * 2)

        # Cartel "CASINO UCR"
        cartel_ancho = 600
        cartel_alto = 80
        cartel_x = ANCHO // 2 - cartel_ancho // 2
        cartel_y = 300
        pygame.draw.rect(ventana, (10, 10, 60), (cartel_x, cartel_y, cartel_ancho, cartel_alto), border_radius=20)
        pygame.draw.rect(ventana, BLANCO, (cartel_x, cartel_y, cartel_ancho, cartel_alto), 4, border_radius=20)

        # Luces del cartel
        num_puntos = 24
        espaciado = cartel_ancho // (num_puntos + 1)
        for i in range(1, num_puntos + 1):
            x = cartel_x + i * espaciado
            pulso = math.sin(self.tiempo + i * 0.3)
            intensidad = 200 + int(55 * pulso)
            color_luz = (intensidad, int(intensidad * 0.8), 100)
            for y in [cartel_y + 10, cartel_y + cartel_alto - 10]:
                glow = pygame.Surface((12, 12), pygame.SRCALPHA)
                pygame.draw.circle(glow, (255, 255, 255, 40), (6, 6), 6)
                ventana.blit(glow, (x - 6, y - 6))
                pygame.draw.circle(ventana, color_luz, (x, y), 4)

        brillo = 180 + int(75 * math.sin(self.tiempo))
        color_texto = (brillo, brillo, 0)
        texto = grande.render("MonteCarloBet", True, color_texto)
        ventana.blit(texto, (cartel_x + cartel_ancho // 2 - texto.get_width() // 2, cartel_y + cartel_alto // 2 - texto.get_height() // 2))

        # Fichas
        y_ficha = cartel_y + cartel_alto + 30
        espacio = 50
        total_ancho = len(fichas) * espacio
        start_x = ANCHO // 2 - total_ancho // 2
        for i, (color, valor) in enumerate(fichas):
            x = start_x + i * espacio
            dibujar_ficha_estilo_casino(x, y_ficha, color, valor)

        # Créditos del proyecto
        textos = [
            "Proyecto Métodos Cuantitativos 2025",
            "- Kendall León",
            "- Anderson Umaña",
            "- Dylan Bastos",
            "- Mario Saborio"
        ]
        altura_creditos = len(textos) * 30
        for i, txt in enumerate(textos):
            render = fuente.render(txt, True, BLANCO)
            ventana.blit(render, (ANCHO // 2 - render.get_width() // 2, y_ficha + 70 + i * 30))

        # Botones (ajustado dinámicamente para que no tapen los textos)
        boton_ancho = 140
        boton_alto = 50
        espacio_entre = 30
        total_ancho_botones = boton_ancho * 2 + espacio_entre
        boton_x1 = ANCHO // 2 - total_ancho_botones // 2
        boton_x2 = boton_x1 + boton_ancho + espacio_entre
        boton_y = y_ficha + 40 + altura_creditos + 30  # calculado dinámicamente

        self.boton_jugar = pygame.Rect(boton_x1, boton_y, boton_ancho, boton_alto)
        self.boton_jugar2 = pygame.Rect(boton_x2, boton_y, boton_ancho, boton_alto)
        pygame.draw.rect(ventana, (255, 204, 0), self.boton_jugar, border_radius=12)
        pygame.draw.rect(ventana, (255, 204, 0), self.boton_jugar2, border_radius=12)

        texto_b1 = fuente.render("1 Jugador", True, NEGRO)
        texto_b2 = fuente.render("2 Jugadores", True, NEGRO)
        ventana.blit(texto_b1, self.boton_jugar.move(30, 10))
        ventana.blit(texto_b2, self.boton_jugar2.move(15, 10))
