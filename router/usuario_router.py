from fastapi import APIRouter, HTTPException
from models.usuario_model import Usuario, ActualizarUsuario, LoginUsuario
from data.usuario_data import (
    obtener_todos_usuarios,
    obtener_un_usuario,
    obtener_un_usuario_correo,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario
)

usuario = APIRouter()

# Obtener todos los usuarios
@usuario.get("/api/user")
async def obtener_usuarios():
    usuario = await obtener_todos_usuarios()
    return usuario

# Obtener un usuario
@usuario.get("/api/user/{id}", response_model=Usuario)
async def obtener_usuario(id: str):
    usuario = await obtener_un_usuario(id)
    if usuario:
        return usuario
    raise HTTPException(404, f"Usuario con {id} no encontrado")

# Crear un usuario
@usuario.post("/api/user", response_model=Usuario)
async def guardar_usuario(usuario: Usuario):
    correoUsuario = await obtener_un_usuario_correo(usuario.correo)
    if correoUsuario:
        raise HTTPException(409, "Usuario con el correo ya existe")
    
    response = await crear_usuario(usuario.dict())
    if response:
        return response
    raise HTTPException(400, "Algo salio mal")

# Actualizar un usuario
@usuario.put("/api/user/{id}", response_model=Usuario)
async def renovar_usuario(id: str, usuario: ActualizarUsuario):
    response = await actualizar_usuario(id, usuario)
    if response:
        return response
    raise HTTPException(404, f"Usuario con {id} no encontrado")

# Eliminar un usuario
@usuario.delete("/api/user/{id}")
async def quitar_usuario(id: str):
    response = await eliminar_usuario(id)
    if response:
        return "Usuario eliminado correctamente"
    raise HTTPException(404, f"Usuario con {id} no encontrado")

# TODO: Separar de Login para no sobrecargar
# Iniciar Sesión
@usuario.post("/api/login", response_model=Usuario)
async def iniciar_sesion(data: LoginUsuario):
    usuario = await obtener_un_usuario_correo(data.correo)
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")

    if usuario["password"] != data.password:
        raise HTTPException(401, "Contraseña incorrecta")

    return Usuario(**usuario)