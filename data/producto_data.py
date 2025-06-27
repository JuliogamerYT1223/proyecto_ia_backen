from models.producto_model import Producto
from bson import ObjectId
from .client import product_collection

# Obtener todos los productos
async def obtener_todos_productos():
    productos = []
    cursor = product_collection.find({})
    async for document in cursor:
        productos.append(Producto(**document))
    return productos

# Obtener un producto
async def obtener_un_producto(id: str):
    producto = await product_collection.find_one({"_id": ObjectId(id)})
    return producto

# Obtener el nombre del producto
async def obtener_un_producto_nombre(nombre):
    nombre_producto = await product_collection.find_one({"nombre": nombre})
    return nombre_producto

# Crear un producto
async def crear_producto(producto):
    nuevo_producto = await product_collection.insert_one(producto)
    created_producto = await product_collection.find_one({"_id": nuevo_producto.inserted_id})
    return created_producto

# Actualizar un producto
async def actualizar_producto(id: str, data):
    producto = {k:v for k, v in data.dict().items() if v is not None}
    await product_collection.update_one({"_id": ObjectId(id)}, {"$set": producto})
    document = await product_collection.find_one({"_id": ObjectId(id)})
    return document

# Eliminar un producto
async def eliminar_producto(id: str):
    await product_collection.delete_one({"_id": ObjectId(id)})
    return True