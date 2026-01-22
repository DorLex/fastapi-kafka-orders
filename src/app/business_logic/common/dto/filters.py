from pydantic import BaseModel, PositiveInt


class PaginationParams(BaseModel):
    limit: PositiveInt = 10
    offset: int = 0
