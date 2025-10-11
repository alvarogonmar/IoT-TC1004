import random
import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv


# Cargar variables del archivo .env
load_dotenv()

# Leer la variable MONGO_URI
mongo_uri = os.getenv("MONGO_URI")

# Conexión a MongoDB
client = MongoClient(mongo_uri)
db = client['Almacenamiento-Tarea-4']
collection = db['Temperaturas']

sensores = [
    {"id": "temp_1", "tipo": "temperatura", "unidad": "Celsius"},
    {"id": "temp_2", "tipo": "temperatura", "unidad": "Celsius"},
    {"id": "temp_3", "tipo": "temperatura", "unidad": "Celsius"},
    {"id": "temp_4", "tipo": "temperatura", "unidad": "Celsius"},
    {"id": "hum_1", "tipo": "humedad", "unidad": "%"},
    {"id": "hum_2", "tipo": "humedad", "unidad": "%"}
]

for sensor in sensores:
    for i in range(20):
        if sensor["tipo"] == "temperatura":
            valor = random.uniform(15, 35)
        else:
            valor = random.uniform(40, 90)

        documento = {
            "sensor_id": sensor["id"],
            "tipo": sensor["tipo"],
            "valor": round(valor, 2),
            "unidad": sensor["unidad"],
            "fecha_hora": datetime.now()
        }

        collection.insert_one(documento)

        if sensor["tipo"] == "temperatura" and valor > 30:
            print(f"Alerta: En sensor: {sensor['id']} temperatura alta ({valor:.2f} °C)")
        elif sensor["tipo"] == "humedad" and valor < 50:
            print(f"Alerta: En sensor: {sensor['id']} humedad baja ({valor:.2f}%)")

print("Lecturas generadas y almacenadas correctamente.")