from asgiref.sync import async_to_sync
from celery import Celery
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
import os
from dotenv import load_dotenv

# from twilio.rest import Client

from ..utils.mail import TEMPLATE_DIR


load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


fast_mail = FastMail(
    ConnectionConfig(
        # **notification_settings.model_dump(
        #     exclude=["TWILIO_SID", "TWILIO_AUTH_TOKEN", "TWILIO_NUMBER"]
        ),
        TEMPLATE_FOLDER=TEMPLATE_DIR,
    )
)

# twilio_client = Client(
#     notification_settings.TWILIO_SID,
#     notification_settings.TWILIO_AUTH_TOKEN,
# )

send_message = async_to_sync(fast_mail.send_message)


app = Celery(
    "api_tasks",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/(9)",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/(9)",
    broker_connection_retry_on_startup=True,
)


@app.task
def send_mail(
    recipients: list[str],
    subject: str,
    body: str,
):
    send_message(
        message=MessageSchema(
            recipients=recipients,
            subject=subject,
            body=body,
            subtype=MessageType.plain,
        ),
    )
    return "Message Sent!"


@app.task
def send_email_with_template(
    recipients: list[EmailStr],
    subject: str,
    context: dict,
    template_name: str,
):
    send_message(
        message=MessageSchema(
            recipients=recipients,
            subject=subject,
            template_body=context,
            subtype=MessageType.html,
        ),
        template_name=template_name,
    )


# @app.task
# def send_sms(to: str, body: str):
#     twilio_client.messages.create(
#         from_=notification_settings.TWILIO_NUMBER,
#         to=to,
#         body=body,
#     )
