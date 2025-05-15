import pygame
import random
from config import VENTANA, ANCHO, fuente, grande, pequena, BLANCO, DORADO, NEGRO
from estado_juego import EstadoJuego
from datos_juego import fichas, rojos, negros
from bd import guardar_resultado
from funciones_dibujo import dibujar_ruleta, dibujar_bolita, dibujar_tablero, dibujar_fichas, dibujar_apuestas, obtener_numero

class PantallaJuego:
    def __init__(self, cambiar_pantalla_callback):
        self.cambiar_pantalla = cambiar_pantalla_callback

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos

            # Selección de fichas
            for i in range(len(fichas)):
                fx = ANCHO // 2 - (len(fichas) * 40) // 2 + i * 50
                if (x - fx)**2 + (y - 580)**2 < 400:
                    EstadoJuego.ficha_seleccionada = i
                    return

            # Selección de casillas
            for num, rect in EstadoJuego.casillas + EstadoJuego.casillas_extra:
                if EstadoJuego.ficha_seleccionada is not None and rect.collidepoint(x, y):
                    EstadoJuego.apuestas.append((num, EstadoJuego.ficha_seleccionada))

            # Botón girar
            if self.boton_girar.collidepoint(x, y) and not EstadoJuego.girando:
                EstadoJuego.velocidad = random.uniform(10, 20)
                EstadoJuego.girando = True
                EstadoJuego.resultado_final = None
                EstadoJuego.mensaje_resultado = ""
                EstadoJuego.resultado_guardado = False

            # Botón borrar
            elif self.boton_borrar.collidepoint(x, y):
                EstadoJuego.apuestas.clear()

            # Botón repetir
            elif self.boton_repetir.collidepoint(x, y):
                EstadoJuego.apuestas.clear()
                EstadoJuego.apuestas.extend(EstadoJuego.apuesta_anterior)

            # Botón estadísticas
            elif self.boton_estadisticas.collidepoint(x, y):
                self.cambiar_pantalla("estadisticas")

    def actualizar(self):
        if EstadoJuego.girando:
            EstadoJuego.angulo_ruleta += EstadoJuego.velocidad
            EstadoJuego.bola_angulo -= EstadoJuego.velocidad * 1.5
            EstadoJuego.velocidad *= 0.98

            if EstadoJuego.velocidad < 0.1:
                EstadoJuego.girando = False

                if not EstadoJuego.resultado_guardado:
                    EstadoJuego.resultado_final = obtener_numero(EstadoJuego.bola_angulo - EstadoJuego.angulo_ruleta)
                    EstadoJuego.mensaje_resultado = "Perdiste"

                    if EstadoJuego.resultado_final is not None:
                        if EstadoJuego.resultado_final == 0:
                            color = "verde"
                        elif EstadoJuego.resultado_final in rojos:
                            color = "rojo"
                        else:
                            color = "negro"

                        guardar_resultado(EstadoJuego.resultado_final, color)
                        EstadoJuego.resultado_guardado = True

                    for apuesta, _ in EstadoJuego.apuestas:
                        if (
                            (isinstance(apuesta, int) and apuesta == EstadoJuego.resultado_final) or
                            (apuesta == "ROJO" and EstadoJuego.resultado_final in rojos) or
                            (apuesta == "NEGRO" and EstadoJuego.resultado_final in negros) or
                            (apuesta == "PAR" and EstadoJuego.resultado_final % 2 == 0 and EstadoJuego.resultado_final != 0) or
                            (apuesta == "IMPAR" and EstadoJuego.resultado_final % 2 == 1) or
                            (apuesta == "1-18" and 1 <= EstadoJuego.resultado_final <= 18) or
                            (apuesta == "19-36" and 19 <= EstadoJuego.resultado_final <= 36)
                        ):
                            EstadoJuego.mensaje_resultado = "¡Ganaste!"
                            break

                    EstadoJuego.apuesta_anterior = EstadoJuego.apuestas[:]
                    EstadoJuego.apuestas.clear()

    def dibujar(self, ventana):
        ventana.fill((18, 78, 22))
        dibujar_ruleta()
        dibujar_bolita()
        dibujar_tablero()
        dibujar_apuestas()
        dibujar_fichas()

        if EstadoJuego.resultado_final is not None:
            texto_num = grande.render(f"Número: {EstadoJuego.resultado_final}", True, BLANCO)
            ventana.blit(texto_num, (ANCHO//2 - texto_num.get_width()//2, 290))
            texto_msg = fuente.render(
                EstadoJuego.mensaje_resultado, True,
                (0, 255, 0) if EstadoJuego.mensaje_resultado == "¡Ganaste!" else (255, 50, 50)
            )
            ventana.blit(texto_msg, (ANCHO//2 - texto_msg.get_width()//2, 320))

        # Botón GIRAR
        self.boton_girar = pygame.Rect(ANCHO // 2 - 60, 620, 120, 35)
        pygame.draw.rect(VENTANA, DORADO, self.boton_girar)
        texto_girar = fuente.render("GIRAR", True, NEGRO)
        ventana.blit(texto_girar, (self.boton_girar.centerx - texto_girar.get_width() // 2, self.boton_girar.centery - 12))

        # Botón ELIMINAR
        self.boton_borrar = pygame.Rect(30, 620, 100, 30)
        pygame.draw.rect(VENTANA, (180, 50, 50), self.boton_borrar)
        ventana.blit(pequena.render("Eliminar", True, BLANCO), (self.boton_borrar.centerx - 25, self.boton_borrar.centery - 7))

        # Botón REPETIR
        self.boton_repetir = pygame.Rect(770, 620, 100, 30)
        pygame.draw.rect(VENTANA, (50, 120, 200), self.boton_repetir)
        ventana.blit(pequena.render("Repetir", True, BLANCO), (self.boton_repetir.centerx - 25, self.boton_repetir.centery - 7))

       # Botón ESTADÍSTICAS (pequeño, esquina superior derecha)
        self.boton_estadisticas = pygame.Rect(ANCHO - 140, 10, 120, 30)
        pygame.draw.rect(VENTANA, (50, 150, 255), self.boton_estadisticas)
        texto_est = pequena.render("Estadísticas", True, (0, 0, 0))
        VENTANA.blit(texto_est, (self.boton_estadisticas.centerx - texto_est.get_width() // 2,
                         self.boton_estadisticas.centery - 8))
