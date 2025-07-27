from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr, SecretStr
import os

from ..utils.mail import TEMPLATE_DIR


# print(f"******************** tempalte directory: {TEMPLATE_DIR}")
# print("MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
# print("MAIL_PASSWORD length:", len(os.getenv("MAIL_PASSWORD") or ""))
# print("MAIL_FROM length:", os.getenv("MAIL_FROM"))
# print(f"********************==============================================")


class NotificationService:
    def __init__(self, tasks: BackgroundTasks):
        self.tasks = tasks
        self.fastmail = FastMail(
            ConnectionConfig(
                MAIL_USERNAME=str(os.getenv("MAIL_USERNAME")),
                MAIL_PASSWORD=SecretStr(os.getenv("MAIL_PASSWORD")),
                MAIL_FROM=os.getenv("MAIL_FROM"),
                MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
                MAIL_SERVER=str(os.getenv("MAIL_SERVER")),
                MAIL_STARTTLS=bool(int(os.getenv("MAIL_STARTTLS", 1))),
                MAIL_SSL_TLS=bool(int(os.getenv("MAIL_SSL_TLS", 0))),
                TEMPLATE_FOLDER=TEMPLATE_DIR,
            )
        )

    async def send_email(
        self,
        recipients: list[EmailStr],
        subject: str,
        body: str,
    ):
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=recipients,
                subject=subject,
                body=body,
                subtype=MessageType.plain,
            ),
        )

    async def send_email_with_template(
        self,
        recipients: list[EmailStr],
        subject: str,
        context: dict,
        template_name: str,
    ):

        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=recipients,
                subject=subject,
                template_body=context,
                subtype=MessageType.html,
            ),
            template_name=template_name,
        )
