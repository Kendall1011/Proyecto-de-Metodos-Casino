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