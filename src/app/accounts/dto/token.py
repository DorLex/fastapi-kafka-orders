from pydantic import BaseModel


class TokenResponseDTO(BaseModel):
    access_token: str


class TokenDTO(BaseModel):
    user_id: int | None = None
    username: str | None = None
