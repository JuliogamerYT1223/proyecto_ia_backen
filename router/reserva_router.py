from fastapi import APIRouter, HTTPException
from models.reserva_model import Reserva
from models.mesa_model import Mesa
from data.reserva_data import crear_reserva, reserva_existente, obtener_reservas_por_fecha, obtener_todos_las_reservas, eliminar_reserva
from data.mesa_data import obtener_todas_mesas, obtener_mesa_por_id, crear_mesa
from datetime import datetime

reserva = APIRouter()

@reserva.get("/api/mesas-disponibles")
async def mesas_disponibles(cantidad_personas: int, fecha_hora: str):
    fecha = datetime.fromisoformat(fecha_hora)
    fecha = fecha.replace(minute=0, second=0, microsecond=0)
    
    todas_mesas = await obtener_todas_mesas()
    reservas = await obtener_reservas_por_fecha(fecha)

    mesas_ocupadas_ids = {str(r["mesa_id"]) for r in reservas}
    
    mesas_libres = [
        mesa for mesa in todas_mesas
        if mesa.capacidad >= cantidad_personas and str(mesa.id) not in mesas_ocupadas_ids
    ]
    return mesas_libres


@reserva.post("/api/reservar", response_model=Reserva)
async def nueva_reserva(reserva: Reserva):
    if await reserva_existente(reserva.mesa_id, reserva.fecha_hora, reserva.usuario_id):
        raise HTTPException(409, "Ya tienes una reserva en esa mesa y horario.")
    
    mesa = await obtener_mesa_por_id(reserva.mesa_id)
    if not mesa:
        raise HTTPException(404, "Mesa no encontrada")

    creada = await crear_reserva(reserva.model_dump(by_alias=True))
    return Reserva(**creada)

@reserva.post("/api/agregar-mesas", response_model=Mesa)
async def agregar_mesas(mesa: Mesa):
    response = await crear_mesa(mesa.dict())
    if response:
        return response
    raise HTTPException(400, "Algo salio mal")

@reserva.get("/api/reservas")
async def obtener_todas_las_reservas():
    reservas = await obtener_todos_las_reservas()
    return reservas

# Eliminar una reserva
@reserva.delete("/api/reserva/{id}")
async def quitar_reserva(id: str):
    response = await eliminar_reserva(id)
    if response:
        return "Reserva eliminado correctamente"
    raise HTTPException(404, f"Reserva con {id} no encontrado")