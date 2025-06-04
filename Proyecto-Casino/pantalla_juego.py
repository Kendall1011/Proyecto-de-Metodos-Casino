import pygame
import random
from config import VENTANA, ANCHO, fuente, grande, pequena, BLANCO, DORADO, NEGRO
import estado_juego
from estado_juego import EstadoJuego
from datos_juego import fichas, rojos, negros
from bd import guardar_resultado
from funciones_dibujo import dibujar_ruleta, dibujar_bolita, dibujar_tablero, dibujar_fichas, dibujar_apuestas, obtener_numero

def valor_ficha(valor):
    valores = {
        "50": 50, "500": 500, "2.5K": 2500, "10K": 10000,
        "25K": 25000, "50K": 50000, "100K": 100000, "250K": 250000
    }
    return valores.get(str(valor), 0)

def es_apuesta_valida(apuestas, nueva_apuesta):
    tipos = [a[0] if isinstance(a, tuple) else a for a in apuestas]
    if (("ROJO" in tipos and nueva_apuesta == "NEGRO") or
        ("NEGRO" in tipos and nueva_apuesta == "ROJO")):
        return False
    if (("PAR" in tipos and nueva_apuesta == "IMPAR") or
        ("IMPAR" in tipos and nueva_apuesta == "PAR")):
        return False
    return True

def reiniciar_estado_juego():
    EstadoJuego.apuestas = []
    EstadoJuego.apuesta_anterior = []
    EstadoJuego.ficha_seleccionada = None
    EstadoJuego.girando = False
    EstadoJuego.velocidad = 0
    EstadoJuego.angulo_ruleta = 0
    EstadoJuego.bola_angulo = 0
    EstadoJuego.resultado_final = None
    EstadoJuego.resultado_guardado = False
    EstadoJuego.mensaje_resultado = ""
    estado_juego.dinero_j1 = 100000
    estado_juego.dinero_j2 = 100000

class PantallaJuego:
    def __init__(self, cambiar_pantalla_callback):
        self.cambiar_pantalla = cambiar_pantalla_callback
        self.flash_j1 = None
        self.flash_tiempo = 0
        self.banca_rota = False
        self.mostrar_reiniciar = False  # <--- NUEVO
        reiniciar_estado_juego()

        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.sonido_player_wins = pygame.mixer.Sound("sonidos/player-wins.mp3")
        self.sonido_player_wins.set_volume(0.7)
        self.sonido_player_wins_canal = None
        self.sonido_ruleta = pygame.mixer.Sound("sonidos/roulette-spin.mp3")
        self.sonido_ruleta.set_volume(0.7)
        self.sonido_ruleta_canal = None

    def manejar_evento(self, evento):
        if evento.type == pygame.USEREVENT and hasattr(evento, 'banca_rota') and evento.banca_rota:
            self.banca_rota = True
            self.banca_rota_tiempo = pygame.time.get_ticks()
            return

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos

            if getattr(self, "mostrar_reiniciar", False):
                if hasattr(self, "boton_reiniciar") and self.boton_reiniciar.collidepoint(x, y):
                    estado_juego.dinero_j1 = 100000
                    EstadoJuego.apuestas.clear()
                    EstadoJuego.apuesta_anterior.clear()
                    self.mostrar_reiniciar = False
                    return

            if self.boton_casa.collidepoint(x, y):
                self.cambiar_pantalla("inicio")

            for i in range(len(fichas)):
                fx = ANCHO // 2 - (len(fichas) * 40) // 2 + i * 50
                if (x - fx)**2 + (y - 580)**2 < 400:
                    EstadoJuego.ficha_seleccionada = i
                    return

            for num, rect in EstadoJuego.casillas + EstadoJuego.casillas_extra:
                if EstadoJuego.ficha_seleccionada is not None and rect.collidepoint(x, y):
                    valor = valor_ficha(fichas[EstadoJuego.ficha_seleccionada][1])
                    if estado_juego.dinero_j1 >= valor:
                        if es_apuesta_valida(EstadoJuego.apuestas, num):
                            EstadoJuego.apuestas.append((num, EstadoJuego.ficha_seleccionada))
                            estado_juego.dinero_j1 -= valor

            if self.boton_girar.collidepoint(x, y) and not EstadoJuego.girando:
                EstadoJuego.velocidad = random.uniform(10, 20)
                EstadoJuego.girando = True
                EstadoJuego.resultado_final = None
                EstadoJuego.mensaje_resultado = ""
                EstadoJuego.resultado_guardado = False
                if self.sonido_ruleta_canal is None or not self.sonido_ruleta_canal.get_busy():
                    self.sonido_ruleta_canal = self.sonido_ruleta.play()

            elif self.boton_borrar.collidepoint(x, y):
                # Devolver el dinero de las apuestas antes de borrarlas
                for apuesta, idx in EstadoJuego.apuestas:
                    valor = valor_ficha(fichas[idx][1])
                    estado_juego.dinero_j1 += valor
                EstadoJuego.apuestas.clear()

            elif self.boton_repetir.collidepoint(x, y):
                EstadoJuego.apuestas.clear()
                EstadoJuego.apuestas.extend(EstadoJuego.apuesta_anterior)

            elif self.boton_estadisticas.collidepoint(x, y):
                self.cambiar_pantalla("estadisticas")

    def actualizar(self):
        if EstadoJuego.girando:
            EstadoJuego.angulo_ruleta += EstadoJuego.velocidad
            EstadoJuego.bola_angulo -= EstadoJuego.velocidad * 1.5
            EstadoJuego.velocidad *= 0.98

            if self.sonido_ruleta_canal is None or not self.sonido_ruleta_canal.get_busy():
                self.sonido_ruleta_canal = self.sonido_ruleta.play()

            if EstadoJuego.velocidad < 0.1:
                EstadoJuego.girando = False
                if self.sonido_ruleta_canal is not None:
                    self.sonido_ruleta_canal.stop()
                if not EstadoJuego.resultado_guardado:
                    EstadoJuego.resultado_final = obtener_numero(EstadoJuego.bola_angulo - EstadoJuego.angulo_ruleta)
                    EstadoJuego.mensaje_resultado = "Perdiste"
                    gano = False  # <--- NUEVO

                    if EstadoJuego.resultado_final is not None:
                        color = ("verde" if EstadoJuego.resultado_final == 0
                                 else "rojo" if EstadoJuego.resultado_final in rojos else "negro")
                        guardar_resultado(EstadoJuego.resultado_final, color)
                        EstadoJuego.resultado_guardado = True

                        for apuesta, idx in EstadoJuego.apuestas:
                            valor = valor_ficha(fichas[idx][1])
                            if (
                                (isinstance(apuesta, int) and apuesta == EstadoJuego.resultado_final) or
                                (apuesta == "ROJO" and EstadoJuego.resultado_final in rojos) or
                                (apuesta == "NEGRO" and EstadoJuego.resultado_final in negros) or
                                (apuesta == "PAR" and EstadoJuego.resultado_final % 2 == 0 and EstadoJuego.resultado_final != 0) or
                                (apuesta == "IMPAR" and EstadoJuego.resultado_final % 2 == 1) or
                                (apuesta == "1-18" and 1 <= EstadoJuego.resultado_final <= 18) or
                                (apuesta == "19-36" and 19 <= EstadoJuego.resultado_final <= 36) or
                                (apuesta == "1st 12" and 1 <= EstadoJuego.resultado_final <= 12) or
                                (apuesta == "2nd 12" and 13 <= EstadoJuego.resultado_final <= 24) or
                                (apuesta == "3rd 12" and 25 <= EstadoJuego.resultado_final <= 36) or
                                (apuesta == "2to1_0" and EstadoJuego.resultado_final in [3,6,9,12,15,18,21,24,27,30,33,36]) or
                                (apuesta == "2to1_1" and EstadoJuego.resultado_final in [2,5,8,11,14,17,20,23,26,29,32,35]) or
                                (apuesta == "2to1_2" and EstadoJuego.resultado_final in [1,4,7,10,13,16,19,22,25,28,31,34])
                            ):
                                estado_juego.dinero_j1 += valor * (35 if isinstance(apuesta, int) else 2)
                                gano = True  # <--- NUEVO
                            elif apuesta in ["1st 12", "2nd 12", "3rd 12", "2to1_0", "2to1_1", "2to1_2"]:
                                estado_juego.dinero_j1 += valor * 3
                                gano = True  # <--- NUEVO

                        if gano:
                            EstadoJuego.mensaje_resultado = "¡Ganaste!"

                    self.flash_j1 = "verde" if EstadoJuego.mensaje_resultado == "¡Ganaste!" else "rojo"
                    self.flash_tiempo = pygame.time.get_ticks()
                    if estado_juego.dinero_j1 == 0:
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'banca_rota': True}))
                        self.mostrar_reiniciar = True
                    else:
                        self.mostrar_reiniciar = False

        if self.banca_rota and pygame.time.get_ticks() - self.banca_rota_tiempo > 3000:
            self.banca_rota = False

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

        # Dibujar dinero
        billete_x = 30
        billete_y = 565
        billete_w = 65
        billete_h = 28
        centro_x = billete_x + billete_w // 2
        centro_y = billete_y + billete_h // 2
        color_flash_j1 = (192, 255, 140)
        if self.flash_j1 and pygame.time.get_ticks() - self.flash_tiempo < 300:
            color_flash_j1 = (0, 255, 0) if self.flash_j1 == "verde" else (255, 60, 60)
        else:
            self.flash_j1 = None

        texto_j1 = pequena.render(f"Dinero {estado_juego.dinero_j1:,}", True, BLANCO)
        ventana.blit(texto_j1, texto_j1.get_rect(center=(centro_x, billete_y - 12)))
        pygame.draw.rect(VENTANA, color_flash_j1, (billete_x, billete_y, billete_w, billete_h), border_radius=4)
        pygame.draw.circle(VENTANA, (60, 160, 60), (billete_x + 10, centro_y), 3)
        pygame.draw.circle(VENTANA, (60, 160, 60), (billete_x + billete_w - 10, centro_y), 3)
        pygame.draw.circle(VENTANA, (60, 160, 60), (centro_x, centro_y), 6)
        simbolo = pequena.render("$", True, BLANCO)
        simbolo_rect = simbolo.get_rect(center=(centro_x, centro_y))
        ventana.blit(simbolo, simbolo_rect)

        # Botones
        self.boton_borrar = pygame.Rect(30, 620, 100, 35)
        pygame.draw.rect(VENTANA, (180, 50, 50), self.boton_borrar, border_radius=8)
        ventana.blit(pequena.render("Eliminar", True, BLANCO), self.boton_borrar.move(10, 5))

        self.boton_repetir = pygame.Rect(770, 620, 100, 35)
        pygame.draw.rect(VENTANA, (50, 120, 200), self.boton_repetir, border_radius=8)
        ventana.blit(pequena.render("Repetir", True, BLANCO), self.boton_repetir.move(10, 5))

        self.boton_estadisticas = pygame.Rect(ANCHO - 110, 10, 100, 35)
        pygame.draw.rect(VENTANA, (50, 150, 255), self.boton_estadisticas, border_radius=8)
        texto_est = pequena.render("Estadísticas", True, NEGRO)
        VENTANA.blit(texto_est, texto_est.get_rect(center=self.boton_estadisticas.center))

        self.boton_casa = pygame.Rect(10, 10, 100, 35)
        pygame.draw.rect(VENTANA, (255, 230, 100), self.boton_casa, border_radius=8)
        texto_casa = pequena.render("Volver", True, NEGRO)
        VENTANA.blit(texto_casa, texto_casa.get_rect(center=self.boton_casa.center))

        self.boton_girar = pygame.Rect(ANCHO // 2 - 60, 620, 120, 35)
        pygame.draw.rect(VENTANA, DORADO, self.boton_girar)
        texto_girar = fuente.render("GIRAR", True, NEGRO)
        ventana.blit(texto_girar, texto_girar.get_rect(center=self.boton_girar.center))

        if self.banca_rota:
            texto_banca_rota = fuente.render("¡Estás en banca rota!", True, (255, 50, 50))
            x_centro = ANCHO // 2 - texto_banca_rota.get_width() // 2
            y_pos = 30
            fondo_rect = pygame.Rect(x_centro - 16, y_pos - 8, texto_banca_rota.get_width() + 32, texto_banca_rota.get_height() + 16)
            s = pygame.Surface((fondo_rect.width, fondo_rect.height), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            ventana.blit(s, fondo_rect.topleft)
            ventana.blit(texto_banca_rota, (x_centro, y_pos))

        if self.mostrar_reiniciar:
            ancho_btn = 260
            alto_btn = 90
            x_btn = ANCHO // 2 - ancho_btn // 2
            y_btn = 180
            self.boton_reiniciar = pygame.Rect(x_btn, y_btn, ancho_btn, alto_btn)

            # Efecto de parpadeo (luces)
            tiempo = pygame.time.get_ticks() // 300 % 2
            color_fondo = (255, 0, 0) if tiempo == 0 else (180, 0, 0)
            color_borde = (255, 255, 0) if tiempo == 0 else (255, 80, 80)

            # Fondo rojo con borde amarillo/rojo parpadeante
            pygame.draw.rect(VENTANA, color_borde, self.boton_reiniciar.inflate(10, 10), border_radius=16)
            pygame.draw.rect(VENTANA, color_fondo, self.boton_reiniciar, border_radius=12)

            texto_alerta = grande.render("¡PERDISTE TODO!", True, (255, 255, 0))
            texto_sindinero = fuente.render("¡Sin dinero!", True, (255, 255, 255))
            texto_reiniciar = fuente.render("Reiniciar", True, (255, 255, 255))

            ventana.blit(texto_alerta, texto_alerta.get_rect(center=(ANCHO//2, y_btn + 25)))
            ventana.blit(texto_sindinero, texto_sindinero.get_rect(center=(ANCHO//2, y_btn + 55)))
            ventana.blit(texto_reiniciar, texto_reiniciar.get_rect(center=(ANCHO//2, y_btn + 75)))
