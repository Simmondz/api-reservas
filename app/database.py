import os
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "api_reservas")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def create_indexes():
    db.reservas.create_index([("espacio_id", ASCENDING), ("fecha", ASCENDING)])
    db.reservas.create_index([("usuario_id", ASCENDING)])
    db.reservas.create_index([("fecha", ASCENDING), ("estado", ASCENDING)])
    db.espacios.create_index([("tipo", ASCENDING), ("activo", ASCENDING)])
