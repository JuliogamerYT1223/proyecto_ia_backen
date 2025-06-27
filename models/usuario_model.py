from pydantic import BaseModel, BeforeValidator, Field, ConfigDict, field_validator, EmailStr
from typing import Optional, Annotated
from bson import ObjectId
from datetime import datetime
from enums.usuario_rol import UsuarioRol
import re

PyObjectId = Annotated[str, BeforeValidator(str)]

class Usuario(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre: str
    correo: EmailStr
    password: str
    telefono: str
    rol: UsuarioRol = UsuarioRol.CLIENTE
    fecha: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y"))

    @field_validator("telefono")
    def validar_telefono(cls, v):
        if not re.fullmatch(r"\d{9}", v):
            raise ValueError("El teléfono debe tener exactamente 9 dígitos numéricos.")
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )

class ActualizarUsuario(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None
    telefono: Optional[str] = None
    rol: Optional[UsuarioRol] = None

    @field_validator("password")
    def validar_password(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        return v

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )

class LoginUsuario(BaseModel):
    correo: EmailStr
    password: str