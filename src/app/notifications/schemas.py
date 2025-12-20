from pydantic import EmailStr, BaseModel


class EmailSchema(BaseModel):
    emails: list[EmailStr]
    subject: str
    message: str
