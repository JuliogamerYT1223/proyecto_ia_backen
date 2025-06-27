from pydantic import BaseModel, Field, ConfigDict, BeforeValidator, EmailStr
from typing import Optional, Annotated
from bson import ObjectId
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class Reserva(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    usuario_id: Optional[PyObjectId]
    mesa_id: PyObjectId
    fecha_hora: datetime
    cantidad_personas: int
    nombre_cliente: str
    correo: EmailStr
    telefono: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, json_encoders={ObjectId: str})
