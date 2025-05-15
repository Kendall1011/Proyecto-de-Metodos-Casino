import pygame
import random
from config import VENTANA, ANCHO, fuente, grande, pequena, BLANCO, DORADO, NEGRO
from estado_juego import EstadoJuego
from datos_juego import rojos, negros
from bd import guardar_resultado
from funciones_dibujo import dibujar_ruleta, dibujar_bolita, dibujar_tablero, dibujar_apuestas_color, obtener_numero, dibujar_ficha_estilo_casino

class Pantalla_juego2:
    def __init__(self, cambiar_pantalla_callback):
        self.cambiar_pantalla = cambiar_pantalla_callback
        self.turno = 1
        self.apuestas_j1 = []
        self.apuestas_j2 = []
        self.resultado_final = None
        self.ganador = ""
        self.ficha_seleccionada = None

        self.fichas_j1 = [("gold", "50"), ("saddlebrown", "500"), ("pink", "2.5K"), ("skyblue", "10K"),
                          ("orange", "25K"), ("gray", "50K"), ("violet", "100K"), ("purple", "250K")]
        self.fichas_j2 = [("red", "50"), ("blue", "500"), ("green", "2.5K"), ("cyan", "10K"),
                          ("darkorange", "25K"), ("black", "50K"), ("indigo", "100K"), ("deeppink", "250K")]

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos

            if self.boton_casa.collidepoint(x, y):
                self.cambiar_pantalla("inicio")

            if self.boton_estadisticas.collidepoint(x, y):
                self.cambiar_pantalla("estadisticas")

            columnas = 4
            offset_x = 60
            offset_y = 550
            for i, (color, valor) in enumerate(self.fichas_j1 if self.turno == 1 else self.fichas_j2):
                col = i % columnas
                row = i // columnas
                fx = offset_x + col * 50 if self.turno == 1 else ANCHO - offset_x - col * 50
                fy = offset_y + row * 50
                if (x - fx)**2 + (y - fy)**2 < 25**2:
                    self.ficha_seleccionada = (color, valor)
                    return

            for num, rect in EstadoJuego.casillas + EstadoJuego.casillas_extra:
                if self.ficha_seleccionada and rect.collidepoint(x, y):
                    if self.turno == 1:
                        self.apuestas_j1.append((num, self.ficha_seleccionada[0]))
                    else:
                        self.apuestas_j2.append((num, self.ficha_seleccionada[0]))

            if self.boton_turno.collidepoint(x, y):
                self.turno = 2 if self.turno == 1 else 1
                self.ficha_seleccionada = None

            if self.boton_girar.collidepoint(x, y) and not EstadoJuego.girando:
                EstadoJuego.velocidad = random.uniform(10, 20)
                EstadoJuego.girando = True
                EstadoJuego.resultado_guardado = False
                EstadoJuego.resultado_final = None
                self.resultado_final = None
                self.ganador = ""
                self.ficha_seleccionada = None

            if self.boton_borrar.collidepoint(x, y):
                self.apuestas_j1.clear()
                self.apuestas_j2.clear()
                self.ficha_seleccionada = None
                self.ganador = ""
                self.resultado_final = None
                EstadoJuego.resultado_guardado = False
                EstadoJuego.resultado_final = None
                EstadoJuego.girando = False
    def actualizar(self):
        if EstadoJuego.girando:
            EstadoJuego.angulo_ruleta += EstadoJuego.velocidad
            EstadoJuego.bola_angulo -= EstadoJuego.velocidad * 1.5
            EstadoJuego.velocidad *= 0.98

            if EstadoJuego.velocidad < 0.1:
                EstadoJuego.girando = False

                if not EstadoJuego.resultado_guardado:
                    self.resultado_final = obtener_numero(EstadoJuego.bola_angulo - EstadoJuego.angulo_ruleta)

                    color = (
                        "verde" if self.resultado_final == 0 else
                        "rojo" if self.resultado_final in rojos else
                        "negro"
                    )

                    guardar_resultado(self.resultado_final, color)
                    EstadoJuego.resultado_guardado = True

            
    def _es_apuesta_ganadora(self, apuesta, resultado):
        if isinstance(apuesta, int):
            return apuesta == resultado
        if apuesta == "ROJO":
            return resultado in rojos
        if apuesta == "NEGRO":
            return resultado in negros
        if apuesta == "PAR":
            return resultado != 0 and resultado % 2 == 0
        if apuesta == "IMPAR":
            return resultado % 2 == 1
        if apuesta == "1-18":
            return 1 <= resultado <= 18
        if apuesta == "19-36":
            return 19 <= resultado <= 36
        return False

    def actualizar(self):
        if EstadoJuego.girando:
            EstadoJuego.angulo_ruleta += EstadoJuego.velocidad
            EstadoJuego.bola_angulo -= EstadoJuego.velocidad * 1.5
            EstadoJuego.velocidad *= 0.98

            if EstadoJuego.velocidad < 0.1:
                EstadoJuego.girando = False

                if not EstadoJuego.resultado_guardado:
                    self.resultado_final = obtener_numero(EstadoJuego.bola_angulo - EstadoJuego.angulo_ruleta)

                    color = (
                        "verde" if self.resultado_final == 0 else
                        "rojo" if self.resultado_final in rojos else
                        "negro"
                    )

                    guardar_resultado(self.resultado_final, color)
                    EstadoJuego.resultado_guardado = True

                # Validar apuestas
                j1_gano = any(self._es_apuesta_ganadora(n, self.resultado_final) for n, _ in self.apuestas_j1)
                j2_gano = any(self._es_apuesta_ganadora(n, self.resultado_final) for n, _ in self.apuestas_j2)

                if j1_gano and not j2_gano:
                    self.ganador = "Jugador 1"
                elif j2_gano and not j1_gano:
                    self.ganador = "Jugador 2"
                elif j1_gano and j2_gano:
                    self.ganador = "Empate"
                else:
                    self.ganador = "Ninguno"

                self.apuestas_j1.clear()
                self.apuestas_j2.clear()


    def dibujar(self, ventana):
        ventana.fill((18, 78, 22))
        dibujar_ruleta()
        dibujar_bolita()
        dibujar_tablero()
        dibujar_apuestas_color(self.apuestas_j1)
        dibujar_apuestas_color(self.apuestas_j2)

        if self.resultado_final is not None:
            texto = fuente.render(f"Número: {self.resultado_final}", True, BLANCO)
            ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 540))
            texto2 = pequena.render(f"Ganador: {self.ganador}", True, BLANCO)
            ventana.blit(texto2, (ANCHO//2 - texto2.get_width()//2, 570))



        columnas = 4
        offset_x = 60
        offset_y = 550

        for i, (color, valor) in enumerate(self.fichas_j1):
            col = i % columnas
            row = i // columnas
            x = offset_x + col * 50
            y = offset_y + row * 50
            dibujar_ficha_estilo_casino(x, y, color, valor)

        for i, (color, valor) in enumerate(self.fichas_j2):
            col = i % columnas
            row = i // columnas
            x = ANCHO - offset_x - col * 50
            y = offset_y + row * 50
            dibujar_ficha_estilo_casino(x, y, color, valor)

        texto_turno = fuente.render(f"Turno: Jugador {self.turno}", True, BLANCO)
        ventana.blit(texto_turno, (ANCHO // 2 - texto_turno.get_width() // 2, 510))
        # Botones
        boton_w, boton_h, radio = 100, 35, 8

        self.boton_casa = pygame.Rect(10, 10, boton_w, boton_h)
        pygame.draw.rect(VENTANA, (255, 230, 100), self.boton_casa, border_radius=radio)
        VENTANA.blit(pequena.render("Volver", True, NEGRO), (
            self.boton_casa.centerx - pequena.size("Volver")[0] // 2,
            self.boton_casa.centery - pequena.size("Volver")[1] // 2
        ))

        self.boton_estadisticas = pygame.Rect(ANCHO - 110, 10, boton_w, boton_h)
        pygame.draw.rect(VENTANA, (50, 150, 255), self.boton_estadisticas, border_radius=radio)
        VENTANA.blit(pequena.render("Estadísticas", True, NEGRO), (
            self.boton_estadisticas.centerx - pequena.size("Estadísticas")[0] // 2,
            self.boton_estadisticas.centery - pequena.size("Estadísticas")[1] // 2
        ))

        self.boton_turno = pygame.Rect(30, 635, boton_w, boton_h)
        pygame.draw.rect(VENTANA, (255, 180, 0), self.boton_turno, border_radius=radio)
        VENTANA.blit(pequena.render("Turno", True, NEGRO), (
            self.boton_turno.centerx - pequena.size("Turno")[0] // 2,
            self.boton_turno.centery - pequena.size("Turno")[1] // 2
        ))

        self.boton_girar = pygame.Rect(ANCHO//2 - 60, 620, 120, 35)
        pygame.draw.rect(VENTANA, DORADO, self.boton_girar)
        VENTANA.blit(fuente.render("GIRAR", True, NEGRO), (
            self.boton_girar.centerx - 30,
            self.boton_girar.centery - 12
        ))

        self.boton_borrar = pygame.Rect(770, 635, boton_w, boton_h)
        pygame.draw.rect(VENTANA, (180, 50, 50), self.boton_borrar, border_radius=radio)
        VENTANA.blit(pequena.render("Limpiar", True, BLANCO), (
            self.boton_borrar.centerx - pequena.size("Limpiar")[0] // 2,
            self.boton_borrar.centery - pequena.size("Limpiar")[1] // 2
        ))
