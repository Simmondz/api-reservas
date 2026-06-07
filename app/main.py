from fastapi import FastAPI
from app.routes import usuarios, espacios, reservas, estadisticas
from app.database import create_indexes

app = FastAPI(
    title="Sistema de Gestión de Citas",
    description="API REST para gestión de reservas de servicios",
    version="1.0.0",
)

app.include_router(usuarios.router)
app.include_router(espacios.router)
app.include_router(reservas.router)
app.include_router(estadisticas.router)


@app.on_event("startup")
async def startup():
    create_indexes()


@app.get("/")
def root():
    return {"message": "API de Reservas funcionando", "docs": "/docs"}
