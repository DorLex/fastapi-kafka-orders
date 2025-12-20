from pydantic import BaseModel, EmailStr, ConfigDict


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'username': 'alex',
                    'email': 'example@gmail.com',
                    'password': '123456789',
                }
            ]
        }
    )


class UserInDBSchema(UserBaseSchema):
    hashed_password: str


class UserOutSchema(UserBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
