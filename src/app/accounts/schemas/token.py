from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenDataSchema(BaseModel):
    user_id: int | None = None
    username: str | None = None
