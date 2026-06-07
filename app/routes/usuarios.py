from fastapi import APIRouter, HTTPException
from app.database import db
from app.schemas import UsuarioCreate
from datetime import datetime

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", status_code=201)
def crear_usuario(usuario: UsuarioCreate):
    doc = {
        "nombre": usuario.nombre,
        "email": usuario.email,
        "telefono": usuario.telefono,
        "fecha_registro": datetime.utcnow(),
    }
    result = db.usuarios.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc
