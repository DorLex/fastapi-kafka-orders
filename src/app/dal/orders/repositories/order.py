from logging import getLogger, Logger

from sqlalchemy import ScalarResult, select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.bll.orders.dto.order import OrderCreateDTO, OrderResponseDTO
from src.app.bll.orders.dto.order_with_owner import OrderWithOwnerDTO
from src.app.dal.orders.models.order import Order

logger: Logger = getLogger(__name__)


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_order(self, user_id: int, order_data: OrderCreateDTO) -> OrderResponseDTO:
        order: Order = Order(
            user_id=user_id,
            title=order_data.title,
            description=order_data.description,
        )

        self.db.add(order)
        await self.db.flush()

        return OrderResponseDTO.model_validate(order)

    async def get_orders(self, skip: int = 0, limit: int = 100) -> list[OrderResponseDTO]:
        query: Select = select(Order).offset(skip).limit(limit)
        result: ScalarResult[Order] = await self.db.scalars(query)

        return [OrderResponseDTO.model_validate(order) for order in result.all()]

    async def get_order_by_id(self, order_id: int) -> OrderResponseDTO | None:
        query: Select = select(Order).where(Order.id == order_id)
        order: Order | None = await self.db.scalar(query)

        return OrderResponseDTO.model_validate(order) if order else None

    async def get_order_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[OrderResponseDTO]:
        # TODO: сделать общий фильтр?
        query: Select = select(Order).where(Order.user_id == user_id).offset(skip).limit(limit)
        result: ScalarResult[Order] = await self.db.scalars(query)

        return [OrderResponseDTO.model_validate(order) for order in result.all()]

    async def get_orders_with_owner(self, skip: int = 0, limit: int = 100) -> list[OrderWithOwnerDTO]:
        query: Select = (
            select(Order)
            .options(joinedload(Order.user))
            .order_by(Order.id)
            .offset(skip).limit(limit)
        )

        result: ScalarResult[Order] = await self.db.scalars(query)
        return [OrderWithOwnerDTO.model_validate(order) for order in result.all()]

    # async def update_status(self, db_order: Order, status: OrderStatusEnum) -> Order:
    #     if not isinstance(status, OrderStatusEnum):
    #         raise ValueError('Недопустимый статус заказа')
    #
    #     # TODO: это вобще не так нужно сделать, и скорее всего через общий patch
    #
    #     db_order.status = status
    #     await self.db.flush()
    #
    #     logger.info(f'Статус заказа №{db_order.id} изменен на {status.value}')
    #
    #     return db_order
