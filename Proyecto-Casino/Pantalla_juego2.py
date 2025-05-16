import pygame
import random
from config import VENTANA, ANCHO, fuente, pequena, BLANCO, DORADO, NEGRO
from estado_juego import EstadoJuego, dinero_j1, dinero_j2
from datos_juego import rojos, negros
from bd import guardar_resultado
from funciones_dibujo import (
    dibujar_ruleta, dibujar_bolita, dibujar_tablero,
    dibujar_apuestas_color, obtener_numero, dibujar_ficha_estilo_casino
)

def valor_ficha(valor):
    valores = {
        "50": 50, "500": 500, "2.5K": 2500, "10K": 10000,
        "25K": 25000, "50K": 50000, "100K": 100000, "250K": 250000
    }
    return valores.get(valor, 0)

def multiplicador_apuesta(apuesta):
    if isinstance(apuesta, int): return 35
    if apuesta in ["ROJO", "NEGRO", "PAR", "IMPAR", "1-18", "19-36"]: return 2
    return 0

class Pantalla_juego2:
    def __init__(self, cambiar_pantalla_callback):
        self.cambiar_pantalla = cambiar_pantalla_callback
        self.turno = 1
        self.apuestas_j1 = []
        self.apuestas_j2 = []
        self.resultado_final = None
        self.ganador = ""
        self.ficha_seleccionada = None

        # Fichas de cada jugador (color, valor)
        self.fichas_j1 = [
            ("gold", "50"), ("saddlebrown", "500"), ("pink", "2.5K"), ("skyblue", "10K"),
            ("orange", "25K"), ("gray", "50K"), ("violet", "100K"), ("purple", "250K")
        ]
        self.fichas_j2 = [
            ("red", "50"), ("blue", "500"), ("green", "2.5K"), ("cyan", "10K"),
            ("darkorange", "25K"), ("black", "50K"), ("indigo", "100K"), ("deeppink", "250K")
        ]

    def manejar_evento(self, evento):
        global dinero_j1, dinero_j2

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos

            # Botones de navegación
            if self.boton_casa.collidepoint(x, y):
                self.cambiar_pantalla("inicio")
            if self.boton_estadisticas.collidepoint(x, y):
                self.cambiar_pantalla("estadisticas")

            # Selección de fichas
            columnas = 4
            offset_x = 60
            offset_y = 530  # Posición más arriba
            for i, (color, valor) in enumerate(self.fichas_j1 if self.turno == 1 else self.fichas_j2):
                col = i % columnas
                row = i // columnas
                fx = offset_x + col * 50 if self.turno == 1 else ANCHO - offset_x - (3 - col) * 50
                fy = offset_y + row * 50
                if (x - fx)**2 + (y - fy)**2 < 25**2:
                    self.ficha_seleccionada = (color, valor)
                    return

            # Colocar ficha en el tablero
            for num, rect in EstadoJuego.casillas + EstadoJuego.casillas_extra:
                if self.ficha_seleccionada and rect.collidepoint(x, y):
                    valor = valor_ficha(self.ficha_seleccionada[1])
                    if self.turno == 1 and dinero_j1 >= valor:
                        self.apuestas_j1.append((num, self.ficha_seleccionada[0], valor))
                        dinero_j1 -= valor
                    elif self.turno == 2 and dinero_j2 >= valor:
                        self.apuestas_j2.append((num, self.ficha_seleccionada[0], valor))
                        dinero_j2 -= valor

            # Cambio de turno
            if self.boton_turno.collidepoint(x, y):
                self.turno = 2 if self.turno == 1 else 1
                self.ficha_seleccionada = None

            # Iniciar giro
            if self.boton_girar.collidepoint(x, y) and not EstadoJuego.girando:
                EstadoJuego.velocidad = random.uniform(10, 20)
                EstadoJuego.girando = True
                EstadoJuego.resultado_guardado = False
                self.resultado_final = None
                self.ganador = ""
                self.ficha_seleccionada = None

            # Borrar fichas y reembolsar
            if self.boton_borrar.collidepoint(x, y):
                if self.turno == 1:
                    for _, _, valor in self.apuestas_j1: dinero_j1 += valor
                    self.apuestas_j1.clear()
                else:
                    for _, _, valor in self.apuestas_j2: dinero_j2 += valor
                    self.apuestas_j2.clear()
                self.ficha_seleccionada = None

    def actualizar(self):
        global dinero_j1, dinero_j2

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
                        "rojo" if self.resultado_final in rojos else "negro"
                    )
                    guardar_resultado(self.resultado_final, color)
                    EstadoJuego.resultado_guardado = True

                    def gana(apuesta):
                        if isinstance(apuesta, int): return apuesta == self.resultado_final
                        if apuesta == "ROJO": return self.resultado_final in rojos
                        if apuesta == "NEGRO": return self.resultado_final in negros
                        if apuesta == "PAR": return self.resultado_final != 0 and self.resultado_final % 2 == 0
                        if apuesta == "IMPAR": return self.resultado_final % 2 == 1
                        if apuesta == "1-18": return 1 <= self.resultado_final <= 18
                        if apuesta == "19-36": return 19 <= self.resultado_final <= 36
                        return False

                    j1_total = sum(v * multiplicador_apuesta(a) for a, _, v in self.apuestas_j1 if gana(a))
                    j2_total = sum(v * multiplicador_apuesta(a) for a, _, v in self.apuestas_j2 if gana(a))
                    dinero_j1 += j1_total
                    dinero_j2 += j2_total

                    if j1_total and not j2_total:
                        self.ganador = "Jugador 1"
                    elif j2_total and not j1_total:
                        self.ganador = "Jugador 2"
                    elif j1_total and j2_total:
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

        # Dibujar apuestas en tablero
        EstadoJuego.apuestas.clear()
        EstadoJuego.apuestas.extend((a, c) for a, c, _ in self.apuestas_j1 + self.apuestas_j2)
        dibujar_apuestas_color(EstadoJuego.apuestas)

        # Billetes visuales
        pygame.draw.rect(ventana, (240, 255, 200), (10, 470, 200, 35), border_radius=10)
        pygame.draw.rect(ventana, (240, 255, 200), (ANCHO - 210, 470, 200, 35), border_radius=10)
        ventana.blit(pequena.render(f"Jugador 1: ₡{dinero_j1:,}", True, NEGRO), (20, 478))
        ventana.blit(pequena.render(f"Jugador 2: ₡{dinero_j2:,}", True, NEGRO), (ANCHO - 200, 478))

        if self.resultado_final is not None:
            texto = fuente.render(f"Número: {self.resultado_final}", True, BLANCO)
            ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 540))
            texto2 = pequena.render(f"Ganador: {self.ganador}", True, BLANCO)
            ventana.blit(texto2, (ANCHO//2 - texto2.get_width()//2, 570))

        # Dibujar fichas más arriba
        for i, (color, valor) in enumerate(self.fichas_j1):
            x = 60 + (i % 4) * 50
            y = 530 + (i // 4) * 50
            dibujar_ficha_estilo_casino(x, y, color, valor)

        for i, (color, valor) in enumerate(self.fichas_j2):
            x = ANCHO - 60 - (i % 4) * 50
            y = 530 + (i // 4) * 50
            dibujar_ficha_estilo_casino(x, y, color, valor)

        # Mostrar de quién es el turno
        texto_turno = fuente.render(f"Turno: Jugador {self.turno}", True, BLANCO)
        ventana.blit(texto_turno, (ANCHO // 2 - texto_turno.get_width() // 2, 510))

        # Botones
        self.boton_casa = pygame.Rect(10, 10, 100, 35)
        pygame.draw.rect(VENTANA, (255, 230, 100), self.boton_casa, border_radius=8)
        VENTANA.blit(pequena.render("Volver", True, NEGRO), (
            self.boton_casa.centerx - pequena.size("Volver")[0] // 2,
            self.boton_casa.centery - pequena.size("Volver")[1] // 2
        ))

        self.boton_estadisticas = pygame.Rect(ANCHO - 110, 10, 100, 35)
        pygame.draw.rect(VENTANA, (50, 150, 255), self.boton_estadisticas, border_radius=8)
        VENTANA.blit(pequena.render("Estadísticas", True, NEGRO), (
            self.boton_estadisticas.centerx - pequena.size("Estadísticas")[0] // 2,
            self.boton_estadisticas.centery - pequena.size("Estadísticas")[1] // 2
        ))

        self.boton_turno = pygame.Rect(30, 635, 100, 35)
        pygame.draw.rect(VENTANA, (255, 180, 0), self.boton_turno, border_radius=8)
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

        self.boton_borrar = pygame.Rect(770, 635, 100, 35)
        pygame.draw.rect(VENTANA, (180, 50, 50), self.boton_borrar, border_radius=8)
        VENTANA.blit(pequena.render("Limpiar", True, BLANCO), (
            self.boton_borrar.centerx - pequena.size("Limpiar")[0] // 2,
            self.boton_borrar.centery - pequena.size("Limpiar")[1] // 2
        ))
