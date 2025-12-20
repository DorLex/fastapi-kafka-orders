from asyncio import sleep
from logging import getLogger, Logger

from pydantic import EmailStr

from src.app.orders.enums import OrderStatusEnum
from src.app.orders.models import Order
from src.app.orders.repository import OrderRepository
from src.app.orders.service import OrderService
from src.common.db import AsyncSessionMaker

logger: Logger = getLogger(__name__)


class OrderProcessor:
    async def execute_order(self, order_id: int, customer_email: EmailStr) -> None:
        async with AsyncSessionMaker() as db:
            order_service: OrderService = OrderService(OrderRepository(db))

            order: Order | None = await order_service.get_order_by_id(order_id)
            try:
                if not order:
                    await self.order_not_found(order_id, customer_email)

                await order_service.update_status(order, OrderStatusEnum.in_processing)
                await db.commit()

                order_processing_successful: bool = await self.do_something_with_order(order)

                if not order_processing_successful:
                    await self.order_processing_failed(order)

                await order_service.update_status(order, OrderStatusEnum.completed)
                await db.commit()

            except Exception as ex:
                logger.error(ex)

    async def order_processing_failed(self, order: Order) -> None:
        await self._order_service.update_status(order, OrderStatusEnum.failed)
        raise Exception(f'Произошла ошибка при обработке заказа №{order.id}')

    async def do_something_with_order(self, _: Order) -> bool:
        await sleep(10)
        return True
