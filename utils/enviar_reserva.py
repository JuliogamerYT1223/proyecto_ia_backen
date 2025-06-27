from email.message import EmailMessage
from decouple import config

SMTP_USER = config("CORREO_SENDER")

async def create_reserva_messages(data: dict):
    admin_msg = EmailMessage()
    admin_msg["Subject"] = f"📅 Nueva Reserva de {data['nombre']}"
    admin_msg["From"] = SMTP_USER
    admin_msg["To"] = "vinalosreyes@gmail.com"

    body_admin = f"""
🍷 Nueva Reserva Recibida:

👤 Nombre: {data['nombre']}
📧 Correo: {data['correo']}
📱 Teléfono: {data['telefono']}
📅 Fecha: {data['fecha']}
⏰ Hora: {data['hora']}
👥 Nº de Personas: {data['personas']}

📓 Mensaje adicional:
{data.get('mensaje', 'No especificado')}
"""

    admin_msg.set_content(body_admin)

    user_msg = EmailMessage()
    user_msg["Subject"] = "✅ Confirmación de Reserva - Viña Los Reyes"
    user_msg["From"] = SMTP_USER
    user_msg["To"] = data["correo"]

    user_msg.set_content(f"""
Hola {data['nombre']} 👋

Gracias por hacer tu reserva con nosotros.

Estos son los detalles que hemos recibido:

📅 Fecha: {data['fecha']}
⏰ Hora: {data['hora']}
👥 Nº de Personas: {data['personas']}

Nos pondremos en contacto contigo para confirmar. ¡Te esperamos con una copa lista! 🍇🍷

Saludos,
Viña Los Reyes
""")

    return admin_msg, user_msg
