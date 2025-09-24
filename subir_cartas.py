import json
import os
from pymongo import MongoClient

# Conexión a MongoDB
cliente = MongoClient('mongodb://localhost:27017/')
db = cliente['cardo']

# Rutas de archivos
carpeta_datos = "datos_cartas"
colecciones = {
    "situaciones": "situaciones.json",
    "objetos": "objetos.json",
    "emociones": "emociones.json",
    "lugares": "lugares.json"
}

# Insertar cada archivo en su colección correspondiente
for coleccion, archivo in colecciones.items():
    ruta_archivo = os.path.join(carpeta_datos, archivo)
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        datos = json.load(f)
        db[coleccion].delete_many({})  # Limpiar colección antes de insertar
        db[coleccion].insert_many(datos)
        print(f"✅ Se subieron {len(datos)} cartas a la colección '{coleccion}'")

print(" ¡Cartas subidas correctamente a MongoDB!")
