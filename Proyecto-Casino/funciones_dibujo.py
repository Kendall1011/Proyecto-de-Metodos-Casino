import pygame
import math
from config import VENTANA, ANCHO, ROJO, NEGRO, VERDE, BLANCO, DORADO, MARRON_CLARO, MADERA, GRIS, pequena
from datos_juego import numeros, colores, fichas, rojos
from estado_juego import EstadoJuego

def obtener_numero(angulo_relativo):
    angulo = (angulo_relativo + 90) % 360
    sector = int(angulo / (360 / len(numeros)))
    return numeros[sector]

def dibujar_ruleta():
    sectores = len(numeros)
    angulo_sector = 360 / sectores
    pygame.draw.circle(VENTANA, DORADO, EstadoJuego.centro, EstadoJuego.radio_externo + 10)
    pygame.draw.circle(VENTANA, NEGRO, EstadoJuego.centro, EstadoJuego.radio_externo)

    for i in range(sectores):
        color = colores[i]
        start = math.radians(EstadoJuego.angulo_ruleta - 90 + i * angulo_sector)
        end = math.radians(EstadoJuego.angulo_ruleta - 90 + (i + 1) * angulo_sector)
        x1 = EstadoJuego.centro[0] + math.cos(start) * EstadoJuego.radio_externo
        y1 = EstadoJuego.centro[1] + math.sin(start) * EstadoJuego.radio_externo
        x2 = EstadoJuego.centro[0] + math.cos(end) * EstadoJuego.radio_externo
        y2 = EstadoJuego.centro[1] + math.sin(end) * EstadoJuego.radio_externo
        pygame.draw.polygon(VENTANA, color, [EstadoJuego.centro, (x1, y1), (x2, y2)])
        pygame.draw.line(VENTANA, BLANCO, EstadoJuego.centro, (x1, y1), 1)

        ang_medio = math.radians(EstadoJuego.angulo_ruleta - 90 + (i + 0.5) * angulo_sector)
        xt = EstadoJuego.centro[0] + math.cos(ang_medio) * (EstadoJuego.radio_externo - 25)
        yt = EstadoJuego.centro[1] + math.sin(ang_medio) * (EstadoJuego.radio_externo - 25)
        texto = pequena.render(str(numeros[i]), True, BLANCO)
        VENTANA.blit(texto, (xt - texto.get_width() // 2, yt - texto.get_height() // 2))

    pygame.draw.circle(VENTANA, MARRON_CLARO, EstadoJuego.centro, EstadoJuego.radio_interno)
    pygame.draw.circle(VENTANA, MADERA, EstadoJuego.centro, EstadoJuego.radio_centro)

def dibujar_bolita():
    x = EstadoJuego.centro[0] + math.cos(math.radians(EstadoJuego.bola_angulo)) * EstadoJuego.bola_distancia
    y = EstadoJuego.centro[1] + math.sin(math.radians(EstadoJuego.bola_angulo)) * EstadoJuego.bola_distancia
    pygame.draw.circle(VENTANA, BLANCO, (int(x), int(y)), EstadoJuego.bola_radio)

def dibujar_tablero():
    x0, y0 = ANCHO // 2 - 300, 360
    ancho, alto = 45, 30
    EstadoJuego.casillas.clear()
    EstadoJuego.casillas_extra.clear()

    pygame.draw.rect(VENTANA, VERDE, (x0, y0, ancho, alto * 3))
    pygame.draw.rect(VENTANA, NEGRO, (x0, y0, ancho, alto * 3), 2)
    VENTANA.blit(pequena.render("0", True, BLANCO), (x0 + 15, y0 + 35))
    EstadoJuego.casillas.append((0, pygame.Rect(x0, y0, ancho, alto * 3)))

    for fila in range(3):
        for col in range(12):
            num = EstadoJuego.numeros_tablero[fila][col]
            color = ROJO if num in rojos else NEGRO
            x = x0 + ancho + col * ancho
            y = y0 + fila * alto
            rect = pygame.Rect(x, y, ancho, alto)
            pygame.draw.rect(VENTANA, color, rect)
            pygame.draw.rect(VENTANA, BLANCO, rect, 2)
            texto = pequena.render(str(num), True, BLANCO)
            VENTANA.blit(texto, (x + 15, y + 7))
            EstadoJuego.casillas.append((num, rect))

    etiquetas = ["1-18", "PAR", "ROJO", "NEGRO", "IMPAR", "19-36"]
    for i, texto in enumerate(etiquetas):
        rect = pygame.Rect(x0 + ancho + i * ancho, y0 + alto * 3 + 5, ancho, alto)
        color = ROJO if texto == "ROJO" else NEGRO if texto == "NEGRO" else GRIS
        pygame.draw.rect(VENTANA, color, rect)
        pygame.draw.rect(VENTANA, BLANCO, rect, 2)
        if texto == "ROJO":
            # Dibuja un círculo rojo en vez de texto
            pygame.draw.circle(VENTANA, ROJO, rect.center, 10)
        elif texto == "NEGRO":
            # Dibuja un círculo negro en vez de texto
            pygame.draw.circle(VENTANA, NEGRO, rect.center, 10)
        else:
            t = pequena.render(texto, True, BLANCO)
            VENTANA.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))
        EstadoJuego.casillas_extra.append((texto, rect))

def dibujar_fichas():
    y = 580
    start_x = ANCHO // 2 - (len(fichas) * 40) // 2
    for i, (color, valor) in enumerate(fichas):
        x = start_x + i * 50
        seleccionada = (EstadoJuego.ficha_seleccionada == i)
        dibujar_ficha_estilo_casino(x, y, color, valor, seleccionada)
def dibujar_ficha_estilo_casino(x, y, color, valor, seleccionada=False):
    radio = 22

    # 🔘 Sombra inferior
    pygame.draw.circle(VENTANA, (30, 30, 30), (x + 2, y + 2), radio)

    # 🔴 Círculo principal
    pygame.draw.circle(VENTANA, color, (x, y), radio)

    # ⚪ Decoraciones tipo ficha (bloques blancos)
    for i in range(12):
        ang = math.radians(i * 30)
        cx = x + math.cos(ang) * (radio - 4)
        cy = y + math.sin(ang) * (radio - 4)
        pygame.draw.rect(VENTANA, BLANCO, pygame.Rect(cx - 2, cy - 2, 4, 4))

    # ⚫ Borde exterior negro
    pygame.draw.circle(VENTANA, NEGRO, (x, y), radio, 2)

    # 💡 Brillo decorativo (círculo semitransparente)
    brillo = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA)
    pygame.draw.circle(brillo, (255, 255, 255, 40), (radio, radio), radio)
    VENTANA.blit(brillo, (x - radio, y - radio))

    # 🔢 Valor centrado
    texto = pequena.render(valor, True, BLANCO)
    VENTANA.blit(texto, (x - texto.get_width() // 2, y - texto.get_height() // 2))

    # 🟡 Anillo blanco si está seleccionada
    if seleccionada:
        pygame.draw.circle(VENTANA, BLANCO, (x, y), radio + 4, 2)



def dibujar_apuestas():
    for (apuesta, ficha_index) in EstadoJuego.apuestas:
        for num, rect in EstadoJuego.casillas + EstadoJuego.casillas_extra:
            if num == apuesta:
                color, _ = fichas[ficha_index]
                pygame.draw.circle(VENTANA, color, rect.center, 8)
                pygame.draw.circle(VENTANA, NEGRO, rect.center, 8, 1)
def dibujar_apuestas_color(apuestas):
    for num, color in apuestas:
        for n, rect in EstadoJuego.casillas + EstadoJuego.casillas_extra:
            if n == num:
                x, y, w, h = rect
                cx = x + w // 2
                cy = y + h // 2
                pygame.draw.circle(VENTANA, color, (cx, cy), 10)
