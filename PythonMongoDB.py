import os
import random
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Leer la variable MONGO_URI
mongo_uri = os.getenv("MONGO_URI")

# Conexión a MongoDB
client = MongoClient(mongo_uri)
db = client['MiDG']
collection = db['Temperaturas']

# Simular lecturas
for i in range(20):

