from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

# Conexión a la Base de Datos "MongoDB"
client = AsyncIOMotorClient(config("MONGODB_URL"))
database = client.get_database("restaurante_bd") # Nombre de la Base de Datos

# Creación de la tablas de la BD
product_collection = database.get_collection("productos")
user_collection = database.get_collection("usuarios")
order_collection = database.get_collection("pedidos")
mesa_collection = database.get_collection("mesas")
reserva_collection = database.get_collection("reservas")