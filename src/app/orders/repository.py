from logging import getLogger, Logger

from sqlalchemy import ScalarResult, select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.accounts.models import User
from src.app.orders.dto.order import OrderCreateSchema
from src.app.orders.enums import OrderStatusEnum
from src.app.orders.models import Order

logger: Logger = getLogger(__name__)


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_order(self, user: User, order_data: OrderCreateSchema) -> Order:
        order: Order = Order(
            user_id=user.id,
            title=order_data.title,
            description=order_data.description,

        )

        self.db.add(order)
        await self.db.flush()

        return order

    async def get_orders(self, skip: int = 0, limit: int = 100) -> list[Order]:
        query: Select = select(Order).offset(skip).limit(limit)
        result: ScalarResult[Order] = await self.db.scalars(query)
        return result.all()

    async def get_orders_with_owner(self, skip: int = 0, limit: int = 100) -> list[Order]:
        query: Select = (
            select(Order)
            .options(joinedload(Order.user))
            .order_by(Order.id)
            .offset(skip).limit(limit)
        )

        result: ScalarResult[Order] = await self.db.scalars(query)
        return result.all()

    async def get_order_by_id(self, order_id: int) -> Order | None:
        query: Select = select(Order).where(Order.id == order_id)
        return await self.db.scalar(query)

    async def get_order_by_user(self, user: User, skip: int = 0, limit: int = 100):
        query = select(Order).where(Order.user_id == user.id).offset(skip).limit(limit)
        result = await self.db.scalars(query)
        return result.all()

    async def update_status(self, db_order: Order, status: OrderStatusEnum) -> Order:
        if not isinstance(status, OrderStatusEnum):
            raise ValueError('Недопустимый статус заказа')

        db_order.status = status
        await self.db.flush()

        logger.info(f'Статус заказа №{db_order.id} изменен на {status.value}')

        return db_order
