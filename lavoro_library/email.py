import os

from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig

connection_config = ConnectionConfig(
    MAIL_USERNAME="lavoro.projektr@gmail.com",
    MAIL_PASSWORD=os.environ.get("EMAIL_PASSWORD"),
    MAIL_FROM="lavoro.projektr@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Lavoro",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email(recipient_email: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[recipient_email],
        body=body,
        subtype=MessageType.html
    )

    fm = FastMail(connection_config)
    await fm.send_message(message)
    return True
