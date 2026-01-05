from pydantic import BaseModel, ConfigDict


class OrderBaseSchema(BaseModel):
    title: str
    description: str


class OrderCreateSchema(OrderBaseSchema):
    pass


class OrderResponseDTO(OrderBaseSchema):
    id: int
    user_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
