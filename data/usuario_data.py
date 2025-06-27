from models.usuario_model import Usuario
from bson import ObjectId
from .client import user_collection

# Obtener todos los usuarios
async def obtener_todos_usuarios():
    usuarios = []
    cursor = user_collection.find({})
    async for document in cursor:
        usuarios.append(Usuario(**document))
    return usuarios

# Obtener un usuario
async def obtener_un_usuario(id: str):
    usuario = await user_collection.find_one({"_id": ObjectId(id)})
    return usuario

# Obtener el correo del usuario
async def obtener_un_usuario_correo(correo):
    correo_usuario = await user_collection.find_one({"correo": correo})
    return correo_usuario

# Crear un usuario
async def crear_usuario(usuario):
    nuevo_usuario = await user_collection.insert_one(usuario)
    created_usuario = await user_collection.find_one({"_id": nuevo_usuario.inserted_id})
    return created_usuario

# Actualizar un usuario
async def actualizar_usuario(id: str, data):
    usuario = {k:v for k, v in data.dict().items() if v is not None}
    await user_collection.update_one({"_id": ObjectId(id)}, {"$set": usuario})
    document = await user_collection.find_one({"_id": ObjectId(id)})
    return document

# Eliminar un usuario
async def eliminar_usuario(id: str):
    await user_collection.delete_one({"_id": ObjectId(id)})
    return True