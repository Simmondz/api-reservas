from fastapi import APIRouter, HTTPException
from app.database import db
from app.schemas import EspacioCreate

router = APIRouter(prefix="/espacios", tags=["Espacios"])


@router.post("/", status_code=201)
def crear_espacio(espacio: EspacioCreate):
    doc = {
        "nombre": espacio.nombre,
        "tipo": espacio.tipo,
        "activo": espacio.activo,
        "atributos": [a.model_dump() for a in espacio.atributos],
    }
    result = db.espacios.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc
