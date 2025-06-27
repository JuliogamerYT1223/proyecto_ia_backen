from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Optional, Annotated
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class Mesa(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre: str
    capacidad: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, json_encoders={ObjectId: str})
