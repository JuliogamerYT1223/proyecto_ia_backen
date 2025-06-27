from fastapi import APIRouter, Form, File, UploadFile
from typing import Optional 
from models.correo_email import Formulario
from models.correo_email import ReservaCorreo 
from utils.enviar_correo import create_messages, send_email_messages
from utils.enviar_quejas import create_reclamo_messages
from utils.enviar_reserva import create_reserva_messages

correo = APIRouter()

@correo.post("/send-email")
async def send_email(data: Formulario):
    admin_msg, user_msg = create_messages(data)
    send_email_messages(admin_msg, user_msg)
    return {"message": "Correos enviados correctamente"}

@correo.post("/send-reclamacion")
async def send_reclamacion(
    correo: str = Form(...),
    servicio: str = Form(...),
    nombres: str = Form(...),
    dni: str = Form(...),
    celular: str = Form(...),
    asunto: str = Form(...),
    descripcion: str = Form(...),
    archivo: Optional[UploadFile] = File(None)
):
    data = {
        "correo": correo,
        "servicio": servicio,
        "nombres": nombres,
        "dni": dni,
        "celular": celular,
        "asunto": asunto,
        "descripcion": descripcion,
    }

    admin_msg, user_msg = await create_reclamo_messages(data, archivo)
    send_email_messages(admin_msg, user_msg)
    return {"message": "Reclamo enviado correctamente"}
