from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None


class EspacioAtributo(BaseModel):
    nombre: str
    valor: str | int | float | bool


class EspacioCreate(BaseModel):
    nombre: str
    tipo: str
    activo: bool = True
    atributos: list[EspacioAtributo] = []


class ReservaCreate(BaseModel):
    usuario_id: str
    espacio_id: str
    fecha: str = Field(description="Formato YYYY-MM-DD")
    hora_inicio: str = Field(description="Formato HH:MM")
    hora_fin: str = Field(description="Formato HH:MM")
