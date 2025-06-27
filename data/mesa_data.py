from .client import mesa_collection
from models.mesa_model import Mesa
from bson import ObjectId

async def obtener_todas_mesas():
    mesas = []
    cursor = mesa_collection.find({})
    async for doc in cursor:
        mesas.append(Mesa(**doc))
    return mesas

async def obtener_mesa_por_id(id: str):
    return await mesa_collection.find_one({"_id": ObjectId(id)})

async def crear_mesa(data: dict):
    nueva = await mesa_collection.insert_one(data)
    return await mesa_collection.find_one({"_id": nueva.inserted_id})
