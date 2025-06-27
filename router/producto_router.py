from fastapi import APIRouter, HTTPException, Form, File, UploadFile
import os
import shutil
from models.producto_model import Producto, ActualizarProducto
from data.producto_data import (
    obtener_todos_productos,
    obtener_un_producto,
    obtener_un_producto_nombre,
    crear_producto,
    actualizar_producto,
    eliminar_producto
)

producto = APIRouter()

# Obtener todos los productos
@producto.get("/api/product")
async def obtener_productos():
    productos = await obtener_todos_productos()
    return productos

# Obtener un producto
@producto.get("/api/product/{id}", response_model=Producto)
async def obtener_producto(id):
    producto = await obtener_un_producto(id)
    if producto:
        return producto
    raise HTTPException(404, f"Producto con {id} no encontrado")

# Crear un producto
@producto.post("/api/product", response_model=Producto)
async def guardar_producto(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    disponible: bool = Form(True),
    imagen: UploadFile = File(...)
):
    nombreEncontrado = await obtener_un_producto_nombre(nombre)
    if nombreEncontrado:
        raise HTTPException(409, "Producto con el nombre ya existe")

    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True) 
    ruta_imagen = os.path.join(uploads_dir, imagen.filename)

    with open(ruta_imagen, "wb") as buffer:
        shutil.copyfileobj(imagen.file, buffer)

    producto_data = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "disponible": disponible,
        "imagen": ruta_imagen 
    }

    response = await crear_producto(producto_data)
    if response:
        return response
    raise HTTPException(400, "Algo salió mal")

# Actualizar producto
@producto.put("/api/product/{id}", response_model=Producto)
async def renovar_producto(id: str, producto: ActualizarProducto):
    response = await actualizar_producto(id, producto)
    if response:
        return response
    raise HTTPException(404, f"Producto con {id} no encontrado")

# Eliminar producto
@producto.delete("/api/product/{id}")
async def quitar_producto(id: str):
    response = await eliminar_producto(id)
    if response:
        return "Producto eliminado correctamente"
    raise HTTPException(404, f"Producto con {id} no encontrado")