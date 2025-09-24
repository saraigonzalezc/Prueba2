import json
import random
import os

# Crear carpeta si no existe
carpeta = "datos_cartas"
os.makedirs(carpeta, exist_ok=True)

# Categorías y frases base
categorias = {
    "situaciones": "Situación inesperada número",
    "objetos": "Objeto misterioso número",
    "emociones": "Emoción intensa número",
    "lugares": "Lugar extraordinario número"
}

# Configuración de puntos (puntaje, cantidad)
puntos_config = [(3, 10), (2, 15), (1, 25)]  # Total: 50 cartas por categoría

# Generar cartas por categoría
for categoria, frase in categorias.items():
    cartas = []
    contador = 1
    for puntos, cantidad in puntos_config:
        for _ in range(cantidad):
            carta = {
                "descripcion": f"{frase} {contador}",
                "puntos": puntos
            }
            cartas.append(carta)
            contador += 1
    random.shuffle(cartas)  # Barajar cartas

    # Guardar en archivo JSON
    ruta_archivo = os.path.join(carpeta, f"{categoria}.json")
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(cartas, archivo, ensure_ascii=False, indent=2)

print(" Cartas generadas correctamente en la carpeta 'datos_cartas'")
