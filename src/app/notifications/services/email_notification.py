from fastapi_mail import MessageSchema, MessageType

from src.app.notifications.config import fast_mail
from src.app.notifications.schemas import EmailSchema


class EmailNotificationService:
    _fast_mail = fast_mail

    async def build_message(self, email: EmailSchema) -> MessageSchema:
        message = MessageSchema(
            subject=email.subject,
            recipients=email.emails,
            body=email.message,
            subtype=MessageType.plain,
        )

        return message

    async def send_email(self, email: EmailSchema) -> None:
        message = await self.build_message(email)
        await self._fast_mail.send_message(message)
