def validar_apuestas(apuestas):
 
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

    return True
