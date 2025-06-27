from pydantic import BaseModel, EmailStr, Field

class Formulario(BaseModel):
    nombre: str
    celular: str
    correo: str
    descripcion: str

class Reclamacion(BaseModel):
    correo: EmailStr
    servicio: str
    nombres: str
    dni: str = Field(..., min_length=8, max_length=8)
    celular: str = Field(..., min_length=9, max_length=9)
    asunto: str
    descripcion: str

class ReservaCorreo(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str
    fecha: str
    hora: str
    personas: int
    mensaje: str = "No especificado"