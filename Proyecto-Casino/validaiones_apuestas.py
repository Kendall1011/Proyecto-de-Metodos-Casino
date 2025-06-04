rojos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
negros = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]

def validar_apuestas(apuestas, resultado_final):
 
    apuestas = [ap.lower() for ap in apuestas]

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
