import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv


load_dotenv('.env')


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=587, 
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="FastAPI",
    MAIL_STARTTLS=True,  
    MAIL_SSL_TLS=False,  
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER='./templates'
)


async def send_email_async(subject: str, email_to: str, body: dict):
    print(subject, email_to, body)
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype='html',
    )
    fm = FastMail(conf)
    await fm.send_message(message)

def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype='html',
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
