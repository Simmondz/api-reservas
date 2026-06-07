from fastapi import APIRouter, HTTPException, Query
from app.database import db
from app.schemas import ReservaCreate
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/reservas", tags=["Reservas"])


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    if "usuario_id" in doc:
        doc["usuario_id"] = str(doc["usuario_id"])
    if "espacio_id" in doc:
        doc["espacio_id"] = str(doc["espacio_id"])
    return doc


@router.get("/disponibilidad")
def verificar_disponibilidad(
    espacio_id: str = Query(...),
    fecha: str = Query(..., description="YYYY-MM-DD"),
    hora_inicio: str = Query(..., description="HH:MM"),
    hora_fin: str = Query(..., description="HH:MM"),
):
    conflicto = db.reservas.find_one({
        "espacio_id": ObjectId(espacio_id),
        "fecha": datetime.strptime(fecha, "%Y-%m-%d"),
        "estado": "activa",
        "hora_inicio": {"$lt": hora_fin},
        "hora_fin": {"$gt": hora_inicio},
    })
    return {"disponible": conflicto is None}


@router.post("/", status_code=201)
def crear_reserva(reserva: ReservaCreate):
    # Validar usuario existe
    usuario = db.usuarios.find_one({"_id": ObjectId(reserva.usuario_id)})
    if not usuario:
        raise HTTPException(status_code=422, detail="Usuario no encontrado")

    # Validar espacio existe
    espacio = db.espacios.find_one({"_id": ObjectId(reserva.espacio_id)})
    if not espacio:
        raise HTTPException(status_code=422, detail="Espacio no encontrado")

    fecha = datetime.strptime(reserva.fecha, "%Y-%m-%d")

    # Validar disponibilidad
    conflicto = db.reservas.find_one({
        "espacio_id": ObjectId(reserva.espacio_id),
        "fecha": fecha,
        "estado": "activa",
        "hora_inicio": {"$lt": reserva.hora_fin},
        "hora_fin": {"$gt": reserva.hora_inicio},
    })
    if conflicto:
        raise HTTPException(status_code=409, detail="Horario no disponible")

    doc = {
        "usuario_id": ObjectId(reserva.usuario_id),
        "espacio_id": ObjectId(reserva.espacio_id),
        "usuario_info": {"nombre": usuario["nombre"], "email": usuario["email"]},
        "espacio_info": {"nombre": espacio["nombre"], "tipo": espacio["tipo"]},
        "fecha": fecha,
        "hora_inicio": reserva.hora_inicio,
        "hora_fin": reserva.hora_fin,
        "estado": "activa",
    }
    result = db.reservas.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    doc["usuario_id"] = str(doc["usuario_id"])
    doc["espacio_id"] = str(doc["espacio_id"])
    doc["fecha"] = reserva.fecha
    return doc


@router.get("/")
def listar_reservas(
    usuario_id: str = Query(None),
    fecha: str = Query(None, description="YYYY-MM-DD"),
):
    filtro = {}
    if usuario_id:
        filtro["usuario_id"] = ObjectId(usuario_id)
    if fecha:
        filtro["fecha"] = datetime.strptime(fecha, "%Y-%m-%d")

    reservas = list(db.reservas.find(filtro).sort("fecha", 1))
    return [serialize(r) for r in reservas]


@router.patch("/{reserva_id}/cancelar")
def cancelar_reserva(reserva_id: str):
    result = db.reservas.update_one(
        {"_id": ObjectId(reserva_id), "estado": "activa"},
        {"$set": {"estado": "cancelada"}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Reserva no encontrada o ya cancelada")
    return {"message": "Reserva cancelada exitosamente"}
