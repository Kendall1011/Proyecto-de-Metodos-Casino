import pygame
from funciones_dibujo import dibujar_ficha_estilo_casino
from datos_juego import fichas
from config import ANCHO, ALTO, VENTANA, FONDO, NARANJA, NEGRO, BLANCO, ROJO, DORADO, fuente, pequena, grande

class PantallaInicio:
    def __init__(self, cambiar_pantalla):
        self.cambiar_pantalla = cambiar_pantalla

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.boton_jugar.collidepoint(x, y):
                self.cambiar_pantalla("juego")

    def actualizar(self):
        pass

    def dibujar(self, ventana):
        ventana.fill(FONDO)

        # Medidas del cartel
        cartel_ancho = 500
        cartel_alto = 100
        cartel_x = ANCHO // 2 - cartel_ancho // 2
        cartel_y = 100

        # Cartel "CASINO UCR" centrado
        pygame.draw.rect(VENTANA, NARANJA, (cartel_x, cartel_y, cartel_ancho, cartel_alto), border_radius=20)
        pygame.draw.rect(VENTANA, NEGRO, (cartel_x, cartel_y, cartel_ancho, cartel_alto), 4, border_radius=20)

        for i in range(18):
            espacio = cartel_ancho // 18
            pygame.draw.circle(VENTANA, BLANCO, (cartel_x + 10 + i * espacio, cartel_y + 10), 5)
            pygame.draw.circle(VENTANA, BLANCO, (cartel_x + 10 + i * espacio, cartel_y + cartel_alto - 10), 5)

        titulo = grande.render("CASINO UCR", True, ROJO)
        ventana.blit(titulo, (
            cartel_x + cartel_ancho // 2 - titulo.get_width() // 2,
            cartel_y + cartel_alto // 2 - titulo.get_height() // 2
        ))

        # Fichas decorativas centradas debajo del cartel
        y_ficha = cartel_y + cartel_alto + 30
        espacio = 50
        total_ancho = len(fichas) * espacio
        start_x = ANCHO // 2 - total_ancho // 2

        for i, (color, valor) in enumerate(fichas):
            x = start_x + i * espacio
            dibujar_ficha_estilo_casino(x, y_ficha, color, valor)

        # Información del proyecto
        linea1 = fuente.render("Proyecto Métodos Cuantitativos 2025", True, BLANCO)
        linea2 = fuente.render("- Kendall Leon", True, BLANCO)
        linea3 = fuente.render("- Nombre 2", True, BLANCO)
        linea4 = fuente.render("- Nombre 3", True, BLANCO)

        ventana.blit(linea1, (ANCHO // 2 - linea1.get_width() // 2, y_ficha + 60))
        ventana.blit(linea2, (ANCHO // 2 - linea2.get_width() // 2, y_ficha + 90))
        ventana.blit(linea3, (ANCHO // 2 - linea3.get_width() // 2, y_ficha + 120))
        ventana.blit(linea4, (ANCHO // 2 - linea4.get_width() // 2, y_ficha + 150))

        # Botón de inicio (centrado)
        boton_ancho = 140
        boton_alto = 50
        boton_x = ANCHO // 2 - boton_ancho // 2
        boton_y = y_ficha + 200

        self.boton_jugar = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)
        pygame.draw.rect(VENTANA, DORADO, self.boton_jugar, border_radius=12)
        texto_boton = fuente.render("1 Jugador", True, NEGRO)
        ventana.blit(texto_boton, (
            self.boton_jugar.centerx - texto_boton.get_width() // 2,
            self.boton_jugar.centery - texto_boton.get_height() // 2
        ))
