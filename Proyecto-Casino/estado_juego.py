class EstadoJuego:
    # Centro y radios
    ANCHO = 900
    centro = (ANCHO // 2, 160)
    radio_externo = 120
    radio_interno = 55
    radio_centro = 20
    bola_radio = 8
    bola_distancia = radio_externo - 20

    # Estado de juego
    angulo_ruleta = 0
    bola_angulo = 0
    velocidad = 0
    girando = False
    resultado_final = None
    ficha_seleccionada = None
    apuestas = []
    apuesta_anterior = []
    mensaje_resultado = ""
    resultado_guardado = False


    # Tablero
    casillas = []
    casillas_extra = []
    numeros_tablero = [
        [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
    ]
