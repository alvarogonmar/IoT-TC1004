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
