import pygame
import sys
from config import VENTANA
from pantalla_inicio import PantallaInicio
from pantalla_juego import PantallaJuego

# Variable global para la pantalla actual
pantalla_actual = None

# Función para cambiar de pantalla
def cambiar_pantalla(nombre):
    global pantalla_actual
    if nombre == "inicio":
        pantalla_actual = PantallaInicio(cambiar_pantalla)
    elif nombre == "juego":
        pantalla_actual = PantallaJuego()

# Bucle principal del juego
def main():
    global pantalla_actual
    cambiar_pantalla("inicio")
    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pantalla_actual.manejar_evento(evento)

        pantalla_actual.actualizar()
        pantalla_actual.dibujar(VENTANA)
        pygame.display.flip()
        reloj.tick(60)

# Ejecutar solo si se llama directamente
if __name__ == "__main__":
    main()
