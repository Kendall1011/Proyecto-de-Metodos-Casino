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
    if isinstance(apuesta, int):
        return 35
    if apuesta in ["ROJO", "NEGRO", "PAR", "IMPAR", "1-18", "19-36"]:
        return 2
    if apuesta in ["1st 12", "2nd 12", "3rd 12", "2to1_0", "2to1_1", "2to1_2"]:
        return 3
    return 0

def es_apuesta_valida(apuestas, nueva_apuesta):
    tipos = [a[0] if isinstance(a, tuple) else a for a in apuestas]

    # No permitir ROJO y NEGRO juntos
    if (("ROJO" in tipos and nueva_apuesta == "NEGRO") or
        ("NEGRO" in tipos and nueva_apuesta == "ROJO")):
        return False

    # No permitir PAR e IMPAR juntos
    if (("PAR" in tipos and nueva_apuesta == "IMPAR") or
        ("IMPAR" in tipos and nueva_apuesta == "PAR")):
        return False

    return True

    docenas = {
        "1st 12": range(1, 13),
        "2nd 12": range(13, 25),
        "3rd 12": range(25, 37)
    }
    if nueva_apuesta in docenas:
        for t in tipos:
            if isinstance(t, int) and t not in docenas[nueva_apuesta]:
                return False
    if isinstance(nueva_apuesta, int):
        for d, nums in docenas.items():
            if d in tipos and nueva_apuesta not in nums:
                return False

    return True


class Pantalla_juego2:
    def __init__(self, cambiar_pantalla_callback):
        self.cambiar_pantalla = cambiar_pantalla_callback
        self.turno = 1
        self.apuestas_j1 = []
        self.apuestas_j2 = []
        self.resultado_final = None
        self.ganador = ""
        self.ficha_seleccionada = None
        self.flash_j1 = None
        self.flash_j2 = None
        self.flash_tiempo = 0

        self.fichas_j1 = [
            ("darkgoldenrod", "50"), ("saddlebrown", "500"), ("pink", "2.5K"), ("skyblue", "10K"),
            ("orange", "25K"), ("gray", "50K"), ("violet", "100K"), ("purple", "250K")
        ]
        self.fichas_j2 = [
            ("red", "50"), ("blue", "500"), ("green", "2.5K"), ("cyan", "10K"),
            ("darkorange", "25K"), ("black", "50K"), ("indigo", "100K"), ("deeppink", "250K")
        ]

        # Cargar el sonido de la ruleta
        self.sonido_ruleta = pygame.mixer.Sound("sonidos/roulette-spin.mp3")
        self.sonido_ruleta.set_volume(0.7)
        self.sonido_ruleta_canal = None  # Para controlar el canal de reproducción

        # Cargar el sonido de victoria
        self.sonido_player_wins = pygame.mixer.Sound("sonidos/player-wins.mp3")
        self.sonido_player_wins.set_volume(0.7)
        self.sonido_player_wins_canal = None  # Para controlar el canal de reproducción

        self.banca_rota_j1 = False
        self.banca_rota_j2 = False
        self.banca_rota_tiempo_j1 = 0
        self.banca_rota_tiempo_j2 = 0

    def manejar_evento(self, evento):
        global dinero_j1, dinero_j2

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos

            if self.boton_casa.collidepoint(x, y):
                self.cambiar_pantalla("inicio")
            elif self.boton_estadisticas.collidepoint(x, y):
                self.cambiar_pantalla("estadisticas")

            columnas = 4
            offset_x = 60
            offset_y = 550
            fichas_actuales = self.fichas_j1 if self.turno == 1 else self.fichas_j2

            for i, (color, valor) in enumerate(fichas_actuales):
                col = i % columnas
                row = i // columnas
                if self.turno == 1:
                    fx = offset_x + col * 50
                else:
                    fx = ANCHO - offset_x - (col * 50)
                fy = offset_y + row * 50
                if (x - fx)**2 + (y - fy)**2 < 25**2:
                    self.ficha_seleccionada = (color, valor)
                    return

            for num, rect in EstadoJuego.casillas + EstadoJuego.casillas_extra:
                if self.ficha_seleccionada and rect.collidepoint(x, y):
                    valor = valor_ficha(self.ficha_seleccionada[1])
                    if self.turno == 1 and dinero_j1 >= valor:
                        if es_apuesta_valida([a for a, _, _ in self.apuestas_j1], num):
                            self.apuestas_j1.append((num, self.ficha_seleccionada[0], valor))
                            dinero_j1 -= valor
                    elif self.turno == 2 and dinero_j2 >= valor:
                        if es_apuesta_valida([a for a, _, _ in self.apuestas_j2], num):
                            self.apuestas_j2.append((num, self.ficha_seleccionada[0], valor))
                            dinero_j2 -= valor

            if self.boton_turno.collidepoint(x, y):
                self.turno = 2 if self.turno == 1 else 1
                self.ficha_seleccionada = None

            if self.boton_girar.collidepoint(x, y) and not EstadoJuego.girando:
                EstadoJuego.velocidad = random.uniform(10, 20)
                EstadoJuego.girando = True
                EstadoJuego.resultado_guardado = False
                self.resultado_final = None
                self.ganador = ""
                self.ficha_seleccionada = None

                # Reproducir sonido de ruleta solo cuando empieza a girar
                if self.sonido_ruleta_canal is None or not self.sonido_ruleta_canal.get_busy():
                    self.sonido_ruleta_canal = self.sonido_ruleta.play()

            if self.boton_borrar.collidepoint(x, y):
                if self.turno == 1:
                    for _, _, valor in self.apuestas_j1:
                        dinero_j1 += valor
                    self.apuestas_j1.clear()
                else:
                    for _, _, valor in self.apuestas_j2:
                        dinero_j2 += valor
                    self.apuestas_j2.clear()
                self.ficha_seleccionada = None

    def actualizar(self):
        global dinero_j1, dinero_j2

        if EstadoJuego.girando:
            EstadoJuego.angulo_ruleta += EstadoJuego.velocidad
            EstadoJuego.bola_angulo -= EstadoJuego.velocidad * 1.5
            EstadoJuego.velocidad *= 0.98

            # Si el sonido no está sonando, reprodúcelo (por si acaso)
            if self.sonido_ruleta_canal is None or not self.sonido_ruleta_canal.get_busy():
                self.sonido_ruleta_canal = self.sonido_ruleta.play()

            if EstadoJuego.velocidad < 0.1:
                EstadoJuego.girando = False

                # Detener el sonido cuando termina de girar
                if self.sonido_ruleta_canal is not None:
                    self.sonido_ruleta_canal.stop()

                if not EstadoJuego.resultado_guardado:
                    self.resultado_final = obtener_numero(EstadoJuego.bola_angulo - EstadoJuego.angulo_ruleta)
                    color = (
                        "verde" if self.resultado_final == 0 else
                        "rojo" if self.resultado_final in rojos else "negro"
                    )
                    guardar_resultado(self.resultado_final, color)
                    EstadoJuego.resultado_guardado = True

                    def gana(apuesta):
                        if isinstance(apuesta, int):
                            return apuesta == self.resultado_final
                        if apuesta == "ROJO":
                            return self.resultado_final in rojos
                        if apuesta == "NEGRO":
                            return self.resultado_final in negros
                        if apuesta == "PAR":
                            return self.resultado_final != 0 and self.resultado_final % 2 == 0
                        if apuesta == "IMPAR":
                            return self.resultado_final % 2 == 1
                        if apuesta == "1-18":
                            return 1 <= self.resultado_final <= 18
                        if apuesta == "19-36":
                            return 19 <= self.resultado_final <= 36
                        if apuesta == "1st 12":
                            return 1 <= self.resultado_final <= 12
                        if apuesta == "2nd 12":
                            return 13 <= self.resultado_final <= 24
                        if apuesta == "3rd 12":
                            return 25 <= self.resultado_final <= 36
                        if apuesta == "2to1_0":
                            return self.resultado_final in [3,6,9,12,15,18,21,24,27,30,33,36]
                        if apuesta == "2to1_1":
                            return self.resultado_final in [2,5,8,11,14,17,20,23,26,29,32,35]
                        if apuesta == "2to1_2":
                            return self.resultado_final in [1,4,7,10,13,16,19,22,25,28,31,34]
                        return False

                    j1_total = sum(v * multiplicador_apuesta(a) for a, _, v in self.apuestas_j1 if gana(a))
                    j2_total = sum(v * multiplicador_apuesta(a) for a, _, v in self.apuestas_j2 if gana(a))
                    dinero_j1 += j1_total
                    dinero_j2 += j2_total

                    if j1_total and not j2_total:
                        self.ganador = "Jugador 1"
                        # Sonido de victoria para Jugador 1
                        if self.sonido_player_wins_canal is None or not self.sonido_player_wins_canal.get_busy():
                            self.sonido_player_wins_canal = self.sonido_player_wins.play()
                    elif j2_total and not j1_total:
                        self.ganador = "Jugador 2"
                        # Sonido de victoria para Jugador 2
                        if self.sonido_player_wins_canal is None or not self.sonido_player_wins_canal.get_busy():
                            self.sonido_player_wins_canal = self.sonido_player_wins.play()
                    elif j1_total and j2_total:
                        self.ganador = "Empate"
                        # Sonido de victoria para ambos
                        if self.sonido_player_wins_canal is None or not self.sonido_player_wins_canal.get_busy():
                            self.sonido_player_wins_canal = self.sonido_player_wins.play()
                    else:
                        self.ganador = "Ninguno"

                    if j1_total > 0:
                        self.flash_j1 = "verde"
                    elif self.apuestas_j1:
                        self.flash_j1 = "rojo"

                    if j2_total > 0:
                        self.flash_j2 = "verde"
                    elif self.apuestas_j2:
                        self.flash_j2 = "rojo"

                    self.flash_tiempo = pygame.time.get_ticks()

                    self.apuestas_j1.clear()
                    self.apuestas_j2.clear()

                    if dinero_j1 == 0:
                        self.banca_rota_j1 = True
                        self.banca_rota_tiempo_j1 = pygame.time.get_ticks()
                    if dinero_j2 == 0:
                        self.banca_rota_j2 = True
                        self.banca_rota_tiempo_j2 = pygame.time.get_ticks()

        # Ocultar mensajes de banca rota después de 3 segundos
        if self.banca_rota_j1 and pygame.time.get_ticks() - self.banca_rota_tiempo_j1 > 3000:
            self.banca_rota_j1 = False
        if self.banca_rota_j2 and pygame.time.get_ticks() - self.banca_rota_tiempo_j2 > 3000:
            self.banca_rota_j2 = False

    def dibujar(self, ventana):
        ventana.fill((18, 78, 22))
        dibujar_ruleta()
        dibujar_bolita()
        dibujar_tablero()

        EstadoJuego.apuestas.clear()
        EstadoJuego.apuestas.extend((a, c) for a, c, _ in self.apuestas_j1 + self.apuestas_j2)
        dibujar_apuestas_color(EstadoJuego.apuestas)

        billete_x1 = 45
        billete_y = 475
        billete_w = 65
        billete_h = 28
        centro_x1 = billete_x1 + billete_w // 2
        billete_x2 = ANCHO - 110
        centro_x2 = billete_x2 + billete_w // 2

        if self.flash_j1 and pygame.time.get_ticks() - self.flash_tiempo < 300:
            color_flash_j1 = (0, 255, 0) if self.flash_j1 == "verde" else (255, 60, 60)
        else:
            color_flash_j1 = (192, 255, 140)
            # NO borres self.flash_j1 aquí, así el mensaje se mantiene

        if self.flash_j2 and pygame.time.get_ticks() - self.flash_tiempo < 300:
            color_flash_j2 = (0, 255, 0) if self.flash_j2 == "verde" else (255, 60, 60)
        else:
            color_flash_j2 = (192, 255, 140)

        texto_j1 = pequena.render(f"Jugador 1 = {dinero_j1:,}", True, BLANCO)
        ventana.blit(texto_j1, texto_j1.get_rect(center=(centro_x1, billete_y - 12)))
        pygame.draw.rect(ventana, color_flash_j1, (billete_x1, billete_y, billete_w, billete_h), border_radius=4)
        pygame.draw.circle(ventana, (60, 160, 60), (billete_x1 + 10, billete_y + billete_h // 2), 3)
        pygame.draw.circle(ventana, (60, 160, 60), (billete_x1 + billete_w - 10, billete_y + billete_h // 2), 3)
        pygame.draw.circle(ventana, (60, 160, 60), (centro_x1, billete_y + billete_h // 2), 6)
        simbolo = pequena.render("$", True, BLANCO)
        simbolo_rect = simbolo.get_rect(center=(centro_x1, billete_y + billete_h // 2))
        ventana.blit(simbolo, simbolo_rect)

        texto_j2 = pequena.render(f"Jugador 2 = {dinero_j2:,}", True, BLANCO)
        ventana.blit(texto_j2, texto_j2.get_rect(center=(centro_x2, billete_y - 12)))
        pygame.draw.rect(ventana, color_flash_j2, (billete_x2, billete_y, billete_w, billete_h), border_radius=4)
        pygame.draw.circle(ventana, (60, 160, 60), (billete_x2 + 10, billete_y + billete_h // 2), 3)
        pygame.draw.circle(ventana, (60, 160, 60), (billete_x2 + billete_w - 10, billete_y + billete_h // 2), 3)
        pygame.draw.circle(ventana, (60, 160, 60), (centro_x2, billete_y + billete_h // 2), 6)
        simbolo2 = pequena.render("$", True, BLANCO)
        simbolo_rect2 = simbolo2.get_rect(center=(centro_x2, billete_y + billete_h // 2))
        ventana.blit(simbolo2, simbolo_rect2)


        if self.resultado_final is not None:
            texto = fuente.render(f"Número: {self.resultado_final}", True, BLANCO)
            ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 540))

            # Mensaje para Jugador 1 (esquina superior izquierda)
            if self.flash_j1 == "verde":
                msg_j1 = "¡Ganaste!"
                color_j1 = (0, 255, 0)
            elif self.flash_j1 == "rojo":
                msg_j1 = "Perdiste"
                color_j1 = (255, 50, 50)
            else:
                msg_j1 = ""
                color_j1 = BLANCO

            # Mensaje para Jugador 2 (esquina superior derecha)
            if self.flash_j2 == "verde":
                msg_j2 = "¡Ganaste!"
                color_j2 = (0, 255, 0)
            elif self.flash_j2 == "rojo":
                msg_j2 = "Perdiste"
                color_j2 = (255, 50, 50)
            else:
                msg_j2 = ""
                color_j2 = BLANCO

            # Mostrar mensajes solo si hubo apuestas
            if msg_j1:
                texto_j1 = fuente.render(msg_j1, True, color_j1)
                nombre_j1 = fuente.render("Jugador 1", True, BLANCO)
                ventana.blit(nombre_j1, (300, 300))
                ventana.blit(texto_j1, (300, 330))
            if msg_j2:
                texto_j2 = fuente.render(msg_j2, True, color_j2)
                nombre_j2 = fuente.render("Jugador 2", True, BLANCO)
                ventana.blit(nombre_j2, (ANCHO - nombre_j2.get_width() - 300, 300))
                ventana.blit(texto_j2, (ANCHO - texto_j2.get_width() - 300, 330))

        for i, (color, valor) in enumerate(self.fichas_j1):
            x = 60 + (i % 4) * 50
            y = 550 + (i // 4) * 50
            dibujar_ficha_estilo_casino(x, y, color, valor)

        for i, (color, valor) in enumerate(self.fichas_j2):
            x = ANCHO - 60 - (i % 4) * 50
            y = 550 + (i // 4) * 50
            dibujar_ficha_estilo_casino(x, y, color, valor)


        texto_turno = fuente.render(f"Turno: Jugador {self.turno}", True, BLANCO)
        ventana.blit(texto_turno, (ANCHO // 2 - texto_turno.get_width() // 2, 580))

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

        # Mensaje de banca rota para cada jugador (solo si corresponde y solo por 3 segundos)
        y_banca_rota = 80
        if self.banca_rota_j1:
            texto_banca_j1 = fuente.render("¡Jugador 1 está en banca rota y ya no puede jugar!", True, (255, 50, 50))
            x_centro = ANCHO // 2 - texto_banca_j1.get_width() // 2
            fondo_rect = pygame.Rect(x_centro - 16, y_banca_rota - 8, texto_banca_j1.get_width() + 32, texto_banca_j1.get_height() + 16)
            s = pygame.Surface((fondo_rect.width, fondo_rect.height), pygame.SRCALPHA)
            s.fill((0,0,0,180))
            ventana.blit(s, (fondo_rect.x, fondo_rect.y))
            ventana.blit(texto_banca_j1, (x_centro, y_banca_rota))
        if self.banca_rota_j2:
            texto_banca_j2 = fuente.render("¡Jugador 2 está en banca rota y ya no puede jugar!", True, (255, 50, 50))
            x_centro = ANCHO // 2 - texto_banca_j2.get_width() // 2
            fondo_rect = pygame.Rect(x_centro - 16, y_banca_rota + 40 - 8, texto_banca_j2.get_width() + 32, texto_banca_j2.get_height() + 16)
            s = pygame.Surface((fondo_rect.width, fondo_rect.height), pygame.SRCALPHA)
            s.fill((0,0,0,180))
            ventana.blit(s, (fondo_rect.x, fondo_rect.y))
            ventana.blit(texto_banca_j2, (x_centro, y_banca_rota + 40))
