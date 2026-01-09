from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.common.constants.order import OrderStatusEnum


class OrderBaseDTO(BaseModel):
    title: str
    description: str


class OrderCreateDTO(OrderBaseDTO):
    pass


class OrderPartialUpdateDTO(BaseModel):
    title: str = None
    description: str = None
    status: OrderStatusEnum = None


class OrderResponseDTO(OrderBaseDTO):
    id: int
    user_id: int
    status: OrderStatusEnum
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderNotificationDTO(BaseModel):
    order_id: int
    message: str
