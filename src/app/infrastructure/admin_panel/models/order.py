from typing import ClassVar

from sqladmin import ModelView
from sqlalchemy.orm import InstrumentedAttribute
from starlette.requests import Request

from src.app.business_logic.orders.dto.order import OrderCreateDTO, OrderPartialUpdateDTO
from src.app.infrastructure.orders.models.order import Order


class OrderAdmin(ModelView, model=Order):
    column_list: ClassVar[list[str | InstrumentedAttribute]] = [Order.id, Order.user_id, Order.title, Order.status]
    form_excluded_columns: ClassVar[list[str | InstrumentedAttribute]] = [Order.created_at, Order.updated_at]

    async def on_model_change(
        self,
        data: dict,
        _model: Order,
        is_created: bool,  # noqa: FBT001
        _request: Request,
    ) -> None:
        if not is_created:
            OrderPartialUpdateDTO(**data)
            # TODO: проверить, как работает сейчас updated_at; подумать, как обновить updated_at
            return

        OrderCreateDTO(**data)
