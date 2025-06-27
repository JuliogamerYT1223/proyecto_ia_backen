from .client import reserva_collection
from models.reserva_model import Reserva
from bson import ObjectId
from datetime import datetime

async def obtener_reservas_por_fecha(fecha_hora: datetime):
    return await reserva_collection.find({"fecha_hora": fecha_hora}).to_list(None)

async def crear_reserva(reserva: dict):
    if "_id" in reserva and reserva["_id"] is None:
        del reserva["_id"]

    nueva = await reserva_collection.insert_one(reserva)
    return await reserva_collection.find_one({"_id": nueva.inserted_id})

async def reserva_existente(mesa_id: str, fecha_hora: datetime, usuario_id: str):
    return await reserva_collection.find_one({
        "mesa_id": ObjectId(mesa_id),
        "fecha_hora": fecha_hora,
        "usuario_id": ObjectId(usuario_id)
    })

async def obtener_todos_las_reservas():
    reservas = []
    cursor = reserva_collection.find({})
    async for document in cursor:
        reservas.append(Reserva(**document))
    return reservas

# Eliminar un reserva
async def eliminar_reserva(id: str):
    await reserva_collection.delete_one({"_id": ObjectId(id)})
    return True