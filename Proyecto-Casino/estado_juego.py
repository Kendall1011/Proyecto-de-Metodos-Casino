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
      
    casillas = []           # ← requerido para el tablero
    casillas_extra = [] 
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
# Dinero inicial
dinero_j1 = 100000
dinero_j2 = 100000

def es_apuesta_valida(apuestas, nueva_apuesta):
    tipos = [a[0] if isinstance(a, tuple) else a for a in apuestas]
    # ROJO y NEGRO juntos
    if (("ROJO" in tipos and nueva_apuesta == "NEGRO") or
        ("NEGRO" in tipos and nueva_apuesta == "ROJO")):
        return False
    # PAR e IMPAR juntos
    if (("PAR" in tipos and nueva_apuesta == "IMPAR") or
        ("IMPAR" in tipos and nueva_apuesta == "PAR")):
        return False
    # 1-18 y 19-36 juntos
    if (("1-18" in tipos and nueva_apuesta == "19-36") or
        ("19-36" in tipos and nueva_apuesta == "1-18")):
        return False
    # Docenas incompatibles
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