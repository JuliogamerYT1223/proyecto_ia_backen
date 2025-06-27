from email.message import EmailMessage
from typing import Optional
from fastapi import UploadFile
from decouple import config

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = config("CORREO_SENDER")
SMTP_PASS = config("CORREO_PASSWORD")

async def create_reclamo_messages(data: dict, archivo: Optional[UploadFile]):
    admin_msg = EmailMessage()
    admin_msg["Subject"] = f"📥 Nuevo Reclamo - {data['asunto']}"
    admin_msg["From"] = SMTP_USER
    admin_msg["To"] = "vinalosreyes@gmail.com"

    body = f"""
📝 Nuevo Reclamo Recibido:

📧 Correo: {data['correo']}
🧾 Servicio: {data['servicio']}
👤 Nombres: {data['nombres']}
🆔 DNI: {data['dni']}
📱 Celular: {data['celular']}
📌 Asunto: {data['asunto']}

🖋️ Descripción:
{data['descripcion']}
"""

    admin_msg.set_content(body)

    if archivo:
        file_data = await archivo.read()
        maintype, subtype = archivo.content_type.split("/")
        admin_msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=archivo.filename)

    user_msg = EmailMessage()
    user_msg["Subject"] = "✅ Reclamo recibido - Viña Los Reyes"
    user_msg["From"] = SMTP_USER
    user_msg["To"] = data["correo"]

    user_msg.set_content(f"""
¡Hola {data['nombres']}! 👋

Hemos recibido tu reclamo con el siguiente detalle:

🧾 Servicio: {data['servicio']}
📌 Asunto: {data['asunto']}
🖋️ Descripción:
{data['descripcion']}

Nos pondremos en contacto contigo pronto. Gracias por tu confianza 🍇

Atentamente,
Viña Los Reyes
""")

    return admin_msg, user_msg
