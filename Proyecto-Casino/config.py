import pygame
from estado_juego import EstadoJuego

# Inicializar Pygame y ventana
pygame.init()
ANCHO, ALTO = EstadoJuego.ANCHO, 700
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ruleta Casino Interactiva")

# Colores
ROJO = (200, 0, 0)
NEGRO = (20, 20, 20)
VERDE = (0, 150, 0)
BLANCO = (255, 255, 255)
DORADO = (218, 165, 32)
FONDO = (18, 78, 22)
MARRON_CLARO = (210, 180, 140)
MADERA = (120, 66, 18)
NARANJA = (255, 140, 0)
GRIS = (100, 100, 100)

# Fuentes
fuente = pygame.font.SysFont("Arial", 24)
pequena = pygame.font.SysFont("Arial", 14)
grande = pygame.font.SysFont("Arial", 32)
mini = pygame.font.SysFont("Arial", 10)  # Fuente más pequeña para el billete
