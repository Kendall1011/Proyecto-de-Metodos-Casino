import pygame
import random
from config import VENTANA, ANCHO, fuente, grande, pequena, BLANCO, DORADO, NEGRO
from estado_juego import EstadoJuego, dinero_j1
from datos_juego import fichas, rojos, negros
from bd import guardar_resultado
from funciones_dibujo import dibujar_ruleta, dibujar_bolita, dibujar_tablero, dibujar_fichas, dibujar_apuestas, obtener_numero 

def valor_ficha(valor):
    valores = {
        "50": 50, "500": 500, "2.5K": 2500, "10K": 10000,
        "25K": 25000, "50K": 50000, "100K": 100000, "250K": 250000
    }
    return valores.get(str(valor), 0)


class PantallaJuego:
    def __init__(self, cambiar_pantalla_callback):
        self.cambiar_pantalla = cambiar_pantalla_callback
        self.flash_j1 = None
        self.flash_tiempo = 0


    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos

            # Botón casa (volver a inicio)
            if self.boton_casa.collidepoint(x, y):
                self.cambiar_pantalla("inicio")
            # Selección de fichas
            for i in range(len(fichas)):
                fx = ANCHO // 2 - (len(fichas) * 40) // 2 + i * 50
                if (x - fx)**2 + (y - 580)**2 < 400:
                    EstadoJuego.ficha_seleccionada = i
                    return

            # Selección de casillas
            for num, rect in EstadoJuego.casillas + EstadoJuego.casillas_extra:
                if EstadoJuego.ficha_seleccionada is not None and rect.collidepoint(x, y):
                    # ↓↓↓ Descontar dinero si tiene suficiente ↓↓↓
                    global dinero_j1
                    valor = valor_ficha(fichas[EstadoJuego.ficha_seleccionada][1])
                    if dinero_j1 >= valor:
                        EstadoJuego.apuestas.append((num, EstadoJuego.ficha_seleccionada))
                        dinero_j1 -= valor

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

                    
                    # → Calcular ganancia
                    global dinero_j1
                    for apuesta, idx in EstadoJuego.apuestas:
                        valor = valor_ficha(fichas[idx][1])
                        if (
                            (isinstance(apuesta, int) and apuesta == EstadoJuego.resultado_final) or
                            (apuesta == "ROJO" and EstadoJuego.resultado_final in rojos) or
                            (apuesta == "NEGRO" and EstadoJuego.resultado_final in negros) or
                            (apuesta == "PAR" and EstadoJuego.resultado_final % 2 == 0 and EstadoJuego.resultado_final != 0) or
                            (apuesta == "IMPAR" and EstadoJuego.resultado_final % 2 == 1) or
                            (apuesta == "1-18" and 1 <= EstadoJuego.resultado_final <= 18) or
                            (apuesta == "19-36" and 19 <= EstadoJuego.resultado_final <= 36)
                        ):
                            if isinstance(apuesta, int):
                                dinero_j1 += valor * 35
                            else:
                                dinero_j1 += valor * 2

                    EstadoJuego.apuesta_anterior = EstadoJuego.apuestas[:]
                    EstadoJuego.apuestas.clear()
                if EstadoJuego.mensaje_resultado == "¡Ganaste!":
                    self.flash_j1 = "verde"
                else:
                    self.flash_j1 = "rojo"
                self.flash_tiempo = pygame.time.get_ticks()




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
            

         # Tamaño y estilo unificado para todos los botones pequeños
        boton_w = 100
        boton_h = 35
        radio = 8

        # Botón ELIMINAR
        self.boton_borrar = pygame.Rect(30, 620, boton_w, boton_h)
        pygame.draw.rect(VENTANA, (180, 50, 50), self.boton_borrar, border_radius=radio)
        ventana.blit(pequena.render("Eliminar", True, BLANCO), (
            self.boton_borrar.centerx - pequena.size("Eliminar")[0] // 2,
            self.boton_borrar.centery - pequena.size("Eliminar")[1] // 2
        ))

        # Botón REPETIR
        self.boton_repetir = pygame.Rect(770, 620, boton_w, boton_h)
        pygame.draw.rect(VENTANA, (50, 120, 200), self.boton_repetir, border_radius=radio)
        ventana.blit(pequena.render("Repetir", True, BLANCO), (
            self.boton_repetir.centerx - pequena.size("Repetir")[0] // 2,
            self.boton_repetir.centery - pequena.size("Repetir")[1] // 2
        ))

        # Botón ESTADÍSTICAS (esquina superior derecha)
        self.boton_estadisticas = pygame.Rect(ANCHO - 110, 10, boton_w, boton_h)
        pygame.draw.rect(VENTANA, (50, 150, 255), self.boton_estadisticas, border_radius=radio)
        texto_est = pequena.render("Estadísticas", True, (0, 0, 0))
        VENTANA.blit(texto_est, (
            self.boton_estadisticas.centerx - texto_est.get_width() // 2,
            self.boton_estadisticas.centery - texto_est.get_height() // 2
        ))

        # Botón CASA (esquina superior izquierda)
        self.boton_casa = pygame.Rect(10, 10, boton_w, boton_h)
        pygame.draw.rect(VENTANA, (255, 230, 100), self.boton_casa, border_radius=radio)
        texto_casa = pequena.render("Volver", True, (0, 0, 0))
        VENTANA.blit(texto_casa, (
            self.boton_casa.centerx - texto_casa.get_width() // 2,
            self.boton_casa.centery - texto_casa.get_height() // 2
        ))

        # Color flash activo solo por 300 ms
        color_flash_j1 = (192, 255, 140)  # normal
        if self.flash_j1 and pygame.time.get_ticks() - self.flash_tiempo < 300:
            color_flash_j1 = (0, 255, 0) if self.flash_j1 == "verde" else (255, 60, 60)
        else:
            self.flash_j1 = None


       # Billete visual pequeño alineado a la izquierda (estilo limpio)
        billete_x = 30
        billete_y = 565
        billete_w = 65
        billete_h = 28
        centro_x = billete_x + billete_w // 2
        centro_y = billete_y + billete_h // 2

        # Texto centrado encima del billete
        texto_j1 = pequena.render(f"Dinero {dinero_j1:,}", True, BLANCO)
        ventana.blit(texto_j1, texto_j1.get_rect(center=(centro_x, billete_y - 12)))

        # Billete decorado
        pygame.draw.rect(VENTANA, color_flash_j1, (billete_x, billete_y, billete_w, billete_h), border_radius=4)
        pygame.draw.circle(VENTANA, (60, 160, 60), (billete_x + 10, centro_y), 3)
        pygame.draw.circle(VENTANA, (60, 160, 60), (billete_x + billete_w - 10, centro_y), 3)
        pygame.draw.circle(VENTANA, (60, 160, 60), (centro_x, centro_y), 6)

        # Símbolo $
        simbolo = pequena.render("$", True, BLANCO)
        simbolo_rect = simbolo.get_rect(center=(centro_x, centro_y))
        ventana.blit(simbolo, simbolo_rect)


        # Botón GIRAR (se mantiene igual)
        self.boton_girar = pygame.Rect(ANCHO // 2 - 60, 620, 120, 35)
        pygame.draw.rect(VENTANA, DORADO, self.boton_girar)
        texto_girar = fuente.render("GIRAR", True, NEGRO)
        ventana.blit(texto_girar, (
            self.boton_girar.centerx - texto_girar.get_width() // 2,
            self.boton_girar.centery - texto_girar.get_height() // 2
        ))