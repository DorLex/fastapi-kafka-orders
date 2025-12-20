from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from __logger.logger import get_logger
from src.app.accounts.models import User
from src.app.orders.enums import OrderStatusEnum
from src.app.orders.models import Order
from src.app.orders.schemas.order import OrderCreateSchema

logger = get_logger(__name__)


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, db_user: User, order: OrderCreateSchema) -> Order:
        db_order: Order = Order(
            title=order.title,
            description=order.description,
            owner_id=db_user.id,
        )

        self._session.add(db_order)
        await self._session.flush()

        return db_order

    async def get_all(self, skip: int = 0, limit: int = 100):
        query = select(Order).offset(skip).limit(limit)
        result = await self._session.scalars(query)
        return result.all()

    async def get_all_with_owner(self, skip: int = 0, limit: int = 100):
        query = (
            select(Order)
            .options(joinedload(Order.user))
            .order_by(Order.id)
            .offset(skip).limit(limit)
        )

        result = await self._session.scalars(query)
        return result.all()

    async def get_by_id(self, order_id: int) -> Order:
        query = select(Order).where(Order.id == order_id)
        return await self._session.scalar(query)

    async def get_by_user(self, db_user: User, skip: int = 0, limit: int = 100):
        query = select(Order).where(Order.user_id == db_user.id).offset(skip).limit(limit)
        result = await self._session.scalars(query)
        return result.all()

    async def update_status(self, db_order: Order, status: OrderStatusEnum) -> Order:
        if not isinstance(status, OrderStatusEnum):
            raise ValueError('Недопустимый статус заказа')

        db_order.status = status
        await self._session.flush()

        logger.info(f'Статус заказа №{db_order.id} изменен на {status.value}')

        return db_order
