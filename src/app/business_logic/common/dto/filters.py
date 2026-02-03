from pydantic import BaseModel, NonNegativeInt, PositiveInt


class PaginationParams(BaseModel):
    limit: PositiveInt = 10
    offset: NonNegativeInt = 0
