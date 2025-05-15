import pygame
import sys
from config import VENTANA
from pantalla_inicio import PantallaInicio
from pantalla_juego import PantallaJuego
from pantalla_estadisticas import PantallaEstadisticas
from pantalla_juego2 import Pantalla_juego2



# Variable global para la pantalla actual
pantalla_actual = None

# Función para cambiar de pantalla
def cambiar_pantalla(nombre):
    global pantalla_actual
    if nombre == "inicio":
        pantalla_actual = PantallaInicio(cambiar_pantalla)
    elif nombre == "juego":
        pantalla_actual = PantallaJuego(cambiar_pantalla)
    elif nombre == "juego2":
        pantalla_actual = Pantalla_juego2(cambiar_pantalla)
    elif nombre == "estadisticas":
        pantalla_actual = PantallaEstadisticas(lambda: cambiar_pantalla("juego"))



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
