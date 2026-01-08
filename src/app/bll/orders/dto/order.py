from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderBaseDTO(BaseModel):
    title: str
    description: str


class OrderCreateDTO(OrderBaseDTO):
    pass


class OrderResponseDTO(OrderBaseDTO):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderNotificationDTO(BaseModel):
    order_id: int
    message: str
