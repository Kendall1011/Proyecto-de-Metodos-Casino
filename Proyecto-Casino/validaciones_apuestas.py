from datos_juego import rojos, negros

def es_apuesta_ganadora(apuesta, resultado):
    if isinstance(apuesta, int):
        return apuesta == resultado
    if apuesta == "ROJO":
        return resultado in rojos
    if apuesta == "NEGRO":
        return resultado in negros
    if apuesta == "PAR":
        return resultado % 2 == 0 and resultado != 0
    if apuesta == "IMPAR":
        return resultado % 2 == 1
    if apuesta == "1-18":
        return 1 <= resultado <= 18
    if apuesta == "19-36":
        return 19 <= resultado <= 36
    if apuesta == "1st 12":
        return 1 <= resultado <= 12
    if apuesta == "2nd 12":
        return 13 <= resultado <= 24
    if apuesta == "3rd 12":
        return 25 <= resultado <= 36
    if apuesta == "2to1_0":
        return resultado in [3,6,9,12,15,18,21,24,27,30,33,36]
    if apuesta == "2to1_1":
        return resultado in [2,5,8,11,14,17,20,23,26,29,32,35]
    if apuesta == "2to1_2":
        return resultado in [1,4,7,10,13,16,19,22,25,28,31,34]
    return False
rojos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
negros = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]

def validar_apuestas(apuestas, resultado_final):
 
    apuestas = [ap.lower() if isinstance(ap, str) else ap for ap in apuestas]

    if 'rojo' in apuestas and 'negro' in apuestas:
        return False

    if 'par' in apuestas and 'impar' in apuestas:
        return False

    if 'alto' in apuestas and 'bajo' in apuestas:
        return False

    docenas = {'1st 12', '2nd 12', '3rd 12'}
    if docenas.issubset(set(apuestas)):
        return False

    columnas = {'2 to 1 (left)', '2 to 1 (middle)', '2 to 1 (right)'}
    if columnas.issubset(set(apuestas)):
        return False

    if resultado_final is None:
        return True  # O ajusta según tu lógica, pero evita comparar con None

    for apuesta in apuestas:
        if apuesta == "1st 12":
            return 1 <= resultado_final <= 12
        if apuesta == "2nd 12":
            return 13 <= resultado_final <= 24
        if apuesta == "3rd 12":
            return 25 <= resultado_final <= 36
        # ...columnas igual...

    return True

def gana(apuesta, resultado_final):
    if resultado_final == 0:
        return apuesta == 0  # Solo gana si se apostó directo al 0
    if isinstance(apuesta, int):
        return apuesta == resultado_final
    if apuesta == "rojo":
        return resultado_final in rojos
    if apuesta == "negro":
        return resultado_final in negros
    if apuesta == "par":
        return resultado_final % 2 == 0
    if apuesta == "impar":
        return resultado_final % 2 == 1
    if apuesta == "alto":
        return 19 <= resultado_final <= 36
    if apuesta == "bajo":
        return 1 <= resultado_final <= 18
    if apuesta == "1st 12":
        return 1 <= resultado_final <= 12
    if apuesta == "2nd 12":
        return 13 <= resultado_final <= 24
    if apuesta == "3rd 12":
        return 25 <= resultado_final <= 36
    # ...otros casos...
    return False
