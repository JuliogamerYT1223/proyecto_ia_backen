from pydantic import BaseModel, BeforeValidator, Field, ConfigDict
from typing import Optional, Annotated
from bson import ObjectId
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class Producto(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre: str
    descripcion: str
    precio: float
    disponible: Optional[bool] = True
    fecha: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y"))
    imagen: Optional[str] = None
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )

class ActualizarProducto(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    disponible: Optional[bool] = None
    imagen: Optional[str] = None
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )