from pydantic import BaseModel, EmailStr, ConfigDict


class UserBaseDTO(BaseModel):
    username: str
    email: EmailStr


class UserCreateDTO(UserBaseDTO):
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'username': 'user_1',
                    'email': 'example@email.com',
                    'password': '123456789',
                },
            ],
        },
    )


# TODO: не нужен?
# class UserInDBSchema(UserBaseDTO):
#     hashed_password: str


class UserResponseDTO(UserBaseDTO):
    id: int

    model_config = ConfigDict(from_attributes=True)
