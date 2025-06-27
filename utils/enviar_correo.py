import smtplib
from email.message import EmailMessage
from decouple import config

def create_messages(data):
    admin_msg = EmailMessage()
    admin_msg["Subject"] = "📥 Nuevo mensaje del formulario"
    admin_msg["From"] = config("CORREO_EMPRESA")
    admin_msg["To"] = config("CORREO_EMPRESA")
    admin_msg.set_content(
        f"""
📩 NUEVO MENSAJE

Nombre: {data.nombre}
Teléfono: {data.celular}
Correo: {data.correo}

Descripción:
{data.descripcion}
"""
    )

    user_msg = EmailMessage()
    user_msg["Subject"] = "📨 Gracias por tu mensaje"
    user_msg["From"] = config("CORREO_EMPRESA")
    user_msg["To"] = data.correo
    user_msg.set_content(
        f"""
Hola {data.nombre},

Gracias por contactarnos. Hemos recibido tu mensaje con los siguientes datos:

Nombre: {data.nombre}
Teléfono: {data.celular}
Correo: {data.correo}
Descripción: {data.descripcion}

Nos pondremos en contacto contigo pronto.

Saludos,
Vina Los Reyes
"""
    )

    return admin_msg, user_msg


def send_email_messages(admin_msg, user_msg):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(config("CORREO_SENDER"), config("CORREO_PASSWORD"))
        smtp.send_message(admin_msg)
        smtp.send_message(user_msg)
