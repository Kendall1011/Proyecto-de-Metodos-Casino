import pygame
from config import ANCHO, ALTO, fuente, pequena, BLANCO, NEGRO
from funciones_dibujo import dibujar_ficha_estilo_casino
from datos_juego import fichas

AZUL = (0, 70, 200)
VERDE = (0, 150, 0)
ROJO = (200, 0, 0)
GRIS = (60, 60, 60)

class PantallaRecomendaciones:
    def __init__(self, volver_callback, consejos_generales, recomendaciones_historial):
        self.volver_callback = volver_callback
        self.consejos_generales = consejos_generales
        self.recomendaciones_historial = recomendaciones_historial

        self.titulo_fuente = pygame.font.SysFont("arial", 38, bold=True)
        self.subtitulo_fuente = pygame.font.SysFont("arial", 26, bold=True)
        self.texto_fuente = pygame.font.SysFont("arial", 22)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            if self.boton_volver.collidepoint(x, y):
                self.volver_callback()

    def actualizar(self):
        pass

def render_texto_multilinea(texto, fuente, color, x, y, max_width, ventana):
    palabras = texto.split(' ')
    linea = ""
    for palabra in palabras:
        test_linea = linea + palabra + " "
        if fuente.size(test_linea)[0] > max_width:
            rendered = fuente.render(linea, True, color)
            ventana.blit(rendered, (x, y))
            y += fuente.get_height() + 2
            linea = palabra + " "
        else:
            linea = test_linea
    if linea:
        rendered = fuente.render(linea, True, color)
        ventana.blit(rendered, (x, y))
        y += fuente.get_height() + 2
    return y

def dibujar(self, ventana):
    ventana.fill(BLANCO)

    # Fichas amontonadas (minimalista, arriba y centradas)
    centro_x = ANCHO // 2
    y_fichas = 30  # Más arriba
    espacio = 36
    offset = -((len(fichas)-1) * espacio) // 2
    for i, (color, valor) in enumerate(fichas):
        x = centro_x + offset + i * espacio
        y = y_fichas + (i % 2) * 10  # Un poco desordenadas para efecto "amontonado"
        dibujar_ficha_estilo_casino(x, y, color, valor)

    # Inicia el texto justo debajo de las fichas
    y = y_fichas + 50

    # Consejos generales
    x_texto = 40  # Más a la izquierda
    max_width = ANCHO - x_texto - 40  # Más espacio para el texto
    subtitulo1 = self.subtitulo_fuente.render("Consejos generales:", True, NEGRO)
    ventana.blit(subtitulo1, (x_texto, y))
    y += 38
    for consejo in self.consejos_generales:
        color = VERDE if consejo.lower().startswith("se recomienda") else ROJO if consejo.lower().startswith("no") else GRIS
        y = render_texto_multilinea("• " + consejo, self.texto_fuente, color, x_texto + 20, y, max_width, ventana)

    # Recomendaciones del historial
    y += 15
    subtitulo2 = self.subtitulo_fuente.render("Recomendaciones para Jugar:", True, NEGRO)
    ventana.blit(subtitulo2, (x_texto, y))
    y += 38
    for reco in self.recomendaciones_historial:
        color = VERDE if reco.lower().startswith("se recomienda") else ROJO if reco.lower().startswith("no") else GRIS
        y = render_texto_multilinea("• " + reco, self.texto_fuente, color, x_texto + 20, y, max_width, ventana)

    # Botón volver pequeño, abajo a la derecha
    boton_ancho = 90
    boton_alto = 32
    margen_derecho = 30
    margen_inferior = 30
    y_boton = ALTO - boton_alto - margen_inferior
    self.boton_volver = pygame.Rect(ANCHO - boton_ancho - margen_derecho, y_boton, boton_ancho, boton_alto)
    pygame.draw.rect(ventana, (230, 230, 230), self.boton_volver, border_radius=12)
    pygame.draw.rect(ventana, (180, 180, 180), self.boton_volver, 2, border_radius=12)
    texto_btn = self.texto_fuente.render("Volver", True, (60, 60, 60))
    ventana.blit(
        texto_btn,
        (self.boton_volver.centerx - texto_btn.get_width() // 2, self.boton_volver.centery - texto_btn.get_height() // 2)
    )

# Agrega esta función fuera de la clase (arriba o abajo del archivo)
# y reemplaza el método dibujar de tu clase por el de arriba.
PantallaRecomendaciones.dibujar = dibujar
PantallaRecomendaciones.render_texto_multilinea = staticmethod(render_texto_multilinea)