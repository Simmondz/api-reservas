from fastapi import APIRouter
from app.database import db

router = APIRouter(prefix="/estadisticas", tags=["Estadísticas"])


@router.get("/espacios")
def estadisticas_por_espacio():
    pipeline = [
        {"$match": {"estado": "activa"}},
        {"$group": {
            "_id": "$espacio_id",
            "total": {"$sum": 1},
            "nombre": {"$first": "$espacio_info.nombre"},
        }},
        {"$sort": {"total": -1}},
    ]
    resultado = list(db.reservas.aggregate(pipeline))
    for r in resultado:
        r["_id"] = str(r["_id"])
    return resultado
