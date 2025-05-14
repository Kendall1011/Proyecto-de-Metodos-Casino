from config import VERDE, ROJO, NEGRO

# Lista de números de la ruleta
numeros = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11,
    30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]

# Determinar colores para cada número
rojos = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
negros = {n for n in numeros if n not in rojos and n != 0}
colores = [VERDE if n == 0 else (ROJO if n in rojos else NEGRO) for n in numeros]

# Fichas y sus valores
fichas = [
    ((255, 215, 0), "50"),
    ((210, 105, 30), "500"),
    ((220, 20, 60), "2.5K"),
    ((70, 130, 180), "10K"),
    ((255, 140, 0), "25K"),
    ((80, 80, 80), "50K"),
    ((200, 0, 100), "100K"),
    ((128, 0, 128), "250K")
]
