from fastapi import FastAPI
from router.producto_router import producto
from router.usuario_router import usuario
from router.correo_router import correo
from router.reserva_router import reserva
from router.chatbot import chatbot
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from fastapi.staticfiles import StaticFiles
import os

# Asegura que exista la carpeta de subida
os.makedirs("uploads", exist_ok=True)

app = FastAPI(title="AI Support Chatbot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Esto permite acceder a http://localhost:8000/uploads/nombre.jpg
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Ruta raíz
@app.get("/")
async def root():
    return {
        "message": "AI Support Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chatbot": "/api/chatbot",
            "users": "/api/user",
            "products": "/api/product",
            "reservations": "/api/reservation",
            "email": "/api/email"
        }
    }

# * Importar todas las rutas
app.include_router(producto)
app.include_router(usuario)
app.include_router(correo)
app.include_router(reserva)
app.include_router(chatbot, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
