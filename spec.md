# Sistema de Gestión de Citas — API de Reservas de Servicios

## Descripción

API REST para la gestión de reservas de horas en servicios que requieren agendamiento previo (barberías, consultorios, etc.). Permite registrar usuarios y espacios, crear reservas con validación de disponibilidad, y consultar/cancelar citas.

## Stack Tecnológico (MVP)

- **Lenguaje:** Python 3.11
- **Framework:** FastAPI
- **Driver MongoDB:** PyMongo
- **Base de datos:** MongoDB Atlas (Free Tier M0)
- **Hosting:** Render (Free Tier)

## Modelo de Datos

### Colección: usuarios
| Campo | Tipo | Descripción |
|-------|------|-------------|
| _id | ObjectId | Identificador único |
| nombre | string | Nombre del usuario |
| email | string | Correo electrónico |
| telefono | string | Teléfono de contacto |
| fecha_registro | datetime | Fecha de registro |

### Colección: espacios
| Campo | Tipo | Descripción |
|-------|------|-------------|
| _id | ObjectId | Identificador único |
| nombre | string | Nombre del espacio |
| tipo | string | Tipo de servicio |
| activo | boolean | Si está disponible |
| atributos | array | Características variables |

### Colección: reservas
| Campo | Tipo | Descripción |
|-------|------|-------------|
| _id | ObjectId | Identificador único |
| usuario_id | ObjectId | Referencia al usuario |
| espacio_id | ObjectId | Referencia al espacio |
| usuario_info | object | Nombre y email del usuario (desnormalizado) |
| espacio_info | object | Nombre y tipo del espacio (desnormalizado) |
| fecha | date | Fecha de la reserva |
| hora_inicio | string | Hora de inicio (HH:MM) |
| hora_fin | string | Hora de fin (HH:MM) |
| estado | string | "activa" o "cancelada" |

## Endpoints REST

| Método | Ruta | Descripción | Éxito | Error |
|--------|------|-------------|-------|-------|
| POST | /usuarios | Registrar usuario | 201 | 400, 422 |
| POST | /espacios | Registrar espacio | 201 | 400, 422 |
| POST | /reservas | Crear reserva | 201 | 409, 422 |
| GET | /reservas | Listar reservas | 200 | 400 |
| GET | /reservas/disponibilidad | Verificar disponibilidad | 200 | 400 |
| PATCH | /reservas/{id}/cancelar | Cancelar reserva | 200 | 404 |
| GET | /estadisticas/espacios | Reservas por espacio | 200 | 500 |

## Patrones aplicados

- **Extended Reference Pattern:** En reservas se duplican datos de usuario y espacio para evitar joins.
- **Attribute Pattern:** En espacios, atributos variables en un array.

## Índices

- reservas: `{ espacio_id: 1, fecha: 1 }`
- reservas: `{ usuario_id: 1 }`
- reservas: `{ fecha: 1, estado: 1 }`
- espacios: `{ tipo: 1, activo: 1 }`
