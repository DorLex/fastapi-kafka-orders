from typing import ClassVar

from sqladmin import ModelView
from sqlalchemy.orm import InstrumentedAttribute
from starlette.requests import Request

from src.app.business_logic.orders.dto.order import OrderCreateDTO, OrderPartialUpdateDTO
from src.app.business_logic.orders.services.order import OrderService
from src.app.infrastructure.orders.models.order import Order
from src.app.infrastructure.orders.repositories.order import OrderRepository
from src.common.db.connection import AsyncSessionMaker


class OrderAdmin(ModelView, model=Order):
    column_list: ClassVar[list[str | InstrumentedAttribute]] = [Order.id, Order.user_id, Order.title, Order.status]
    column_searchable_list: ClassVar[list[InstrumentedAttribute]] = [Order.title]
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
            return

        OrderCreateDTO(**data)

    async def after_model_change(
        self,
        _data: dict,
        model: Order,
        is_created: bool,  # noqa: FBT001
        _request: Request,
    ) -> None:
        if not is_created:
            async with AsyncSessionMaker() as db:
                order_service: OrderService = OrderService(OrderRepository(db))
                # триггерим поле updated_at
                await order_service.update_order_partial(model.id, OrderPartialUpdateDTO())
                await db.commit()
