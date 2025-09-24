import pymongo
import random
import os
import time
from datetime import datetime

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def pedir_opcion(mensaje, opciones):
    while True:
        entrada = input(mensaje).strip()
        if entrada.isdigit():
            num = int(entrada)
            if 1 <= num <= opciones:
                return num - 1
        print(f"Por favor ingresa un número entre 1 y {opciones}.")

# Conexión a MongoDB
cliente = pymongo.MongoClient("mongodb://localhost:27017/")
db = cliente["cardo"]
colecciones = {
    "situaciones": db["situaciones"],
    "objetos": db["objetos"],
    "emociones": db["emociones"],
    "lugares": db["lugares"],
    "partidas": db["partidas"]
}

# Bienvenida
print(" Bienvenido al simulador de Cardo ")
jugador1 = input("Nombre del Jugador 1: ")
jugador2 = input("Nombre del Jugador 2: ")

# Número de rondas
try:
    rondas = int(input("¿Cuántas rondas desean jugar? (3 a 10): "))
    if rondas < 3 or rondas > 10:
        print("Número inválido, se jugarán 5 rondas por defecto.")
        rondas = 5
except ValueError:
    print("Entrada inválida, se jugarán 5 rondas por defecto.")
    rondas = 5

# Registro inicial de la partida
partida = {
    "jugador1": jugador1,
    "jugador2": jugador2,
    "fecha": datetime.now(),
    "rondas": [],
    "puntos": {
        jugador1: 0,
        jugador2: 0
    }
}

# Simulación de rondas
for ronda_num in range(1, rondas + 1):
    limpiar_consola()
    print(f" Ronda {ronda_num}/{rondas}")

    # Alternar roles
    cardoelector = jugador1 if ronda_num % 2 != 0 else jugador2
    cardomante = jugador2 if cardoelector == jugador1 else jugador1

    # Elegir cartas al azar
    cartas = {
        "situacion": colecciones["situaciones"].aggregate([{"$sample": {"size": 1}}]).next(),
        "objeto": colecciones["objetos"].aggregate([{"$sample": {"size": 1}}]).next(),
        "emocion": colecciones["emociones"].aggregate([{"$sample": {"size": 1}}]).next(),
        "lugar": colecciones["lugares"].aggregate([{"$sample": {"size": 1}}]).next()
    }

    # Mostrar opciones al cardoelector
    print(f"\n Hora de elegir {cardoelector}")
    opciones = random.sample(list(cartas.items()), 3)
    for i, (tipo, carta) in enumerate(opciones, 1):
        print(f"{i}) {carta['descripcion']} ({carta['puntos']})")

    eleccion_elector = pedir_opcion("Selecciona una carta (1-3): ", 3)
    carta_correcta = opciones[eleccion_elector]

    limpiar_consola()
    print(f" Hora de adivinar {cardomante}")
    for i, (tipo, carta) in enumerate(opciones, 1):
        print(f"{i}) {carta['descripcion']} ({carta['puntos']})")

    eleccion_mante = pedir_opcion("¿Cuál eliges? (1-3): ", 3)

    adivino = eleccion_mante == eleccion_elector
    puntos = carta_correcta[1]['puntos']

    # Asignar puntos
    if adivino:
        # Si adivina, gana puntos menos 1 si es 2 o 3 puntos
        puntos_ganados = puntos - 1 if puntos > 1 else puntos
        partida["puntos"][cardomante] += puntos_ganados
        resultado = f"{cardomante} adivinó correctamente ✅ y gana {puntos_ganados} puntos."
    else:
        # Si no adivina, gana el cardoelector el puntaje completo
        partida["puntos"][cardoelector] += puntos
        resultado = f"{cardomante} falló . {cardoelector} gana {puntos} puntos."

    print("\n Resultado de la ronda:")
    print(resultado)
    time.sleep(3)

    # Guardar ronda
    partida["rondas"].append({
        "numero": ronda_num,
        "cardoelector": cardoelector,
        "cardomante": cardomante,
        "cartas": [{tipo: carta["descripcion"], "puntos": carta["puntos"]} for tipo, carta in opciones],
        "carta_correcta": carta_correcta[1]["descripcion"],
        "gana": cardomante if adivino else cardoelector
    })

# Resultado final
limpiar_consola()
ganador = jugador1 if partida["puntos"][jugador1] > partida["puntos"][jugador2] else jugador2

print(f"🎉 ¡Gana {ganador}!")
print(f"Puntos:")
print(f"{jugador1}: {partida['puntos'][jugador1]}")
print(f"{jugador2}: {partida['puntos'][jugador2]}")

# Guardar partida
partida["ganador"] = ganador
colecciones["partidas"].insert_one(partida)
print("\n Partida guardada exitosamente en la base de datos.")
