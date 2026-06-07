# API de Reservas de Servicios

Sistema de Gestión de Citas — API REST con FastAPI y MongoDB.

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /usuarios | Registrar usuario |
| POST | /espacios | Registrar espacio |
| POST | /reservas | Crear reserva |
| GET | /reservas | Listar reservas |
| GET | /reservas/disponibilidad | Verificar disponibilidad |
| PATCH | /reservas/{id}/cancelar | Cancelar reserva |
| GET | /estadisticas/espacios | Estadísticas por espacio |

## Documentación interactiva

Una vez desplegado, acceder a `/docs` para Swagger UI.

## Variables de entorno

| Variable | Descripción |
|----------|-------------|
| MONGO_URI | Connection string de MongoDB Atlas |
| DB_NAME | Nombre de la base de datos (default: api_reservas) |

## Deploy en Render

1. Conectar repositorio de GitHub en Render
2. Configurar como **Web Service**
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Agregar variables de entorno: `MONGO_URI` y `DB_NAME`
