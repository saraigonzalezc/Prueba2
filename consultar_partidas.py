import pymongo
from datetime import datetime

# Conexión a MongoDB
cliente = pymongo.MongoClient("mongodb://localhost:27017/")
db = cliente["cardo"]
partidas = db["partidas"]

# Obtener todas las partidas
todas_las_partidas = partidas.find()

print(" HISTORIAL DE PARTIDAS CARDÓ:\n")

for partida in todas_las_partidas:
    print("=" * 40)
    print(f" {partida['jugador1']} vs  {partida['jugador2']}")
    print(f" Fecha: {partida['fecha'].strftime('%d/%m/%Y %H:%M')}")
    print(f" Rondas: {len(partida['rondas'])}")
    print(f" Ganador: {partida['ganador']}")
    print(f" Puntos:")
    for jugador, puntos in partida["puntos"].items():
        print(f"   - {jugador}: {puntos} puntos")

    print("\n🕹️ Detalles por ronda:")
    for ronda in partida["rondas"]:
        print(f"\n🔁 Ronda {ronda['numero']}")
        print(f"   - Cardoelector: {ronda['cardoelector']}")
        print(f"   - Cardomante: {ronda['cardomante']}")
        print(f"   - Carta correcta: {ronda['carta_correcta']}")
        print(f"   - Ganador de la ronda: {ronda['gana']}")
        print("   - Cartas mostradas:")
        for carta in ronda["cartas"]:
            for tipo, descripcion in carta.items():
                if tipo != "puntaje":
                    print(f"     • {tipo.capitalize()}: {descripcion} ({carta['puntaje']} pts)")
    print("=" * 40 + "\n")

