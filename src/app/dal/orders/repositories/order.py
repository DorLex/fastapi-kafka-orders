from logging import Logger, getLogger

from sqlalchemy import ScalarResult, Select, Update, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.bll.common.dto.filters import PaginationParams
from src.app.bll.orders.dto.filters import OrderFilter
from src.app.bll.orders.dto.order import OrderCreateDTO, OrderPartialUpdateDTO, OrderResponseDTO
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

    async def get_order_by_id(self, order_id: int) -> OrderResponseDTO | None:
        query: Select = select(Order).where(Order.id == order_id)
        order: Order | None = await self.db.scalar(query)

        return OrderResponseDTO.model_validate(order) if order else None

    async def update_order_partial(self, order_id: int, order_data: OrderPartialUpdateDTO) -> OrderResponseDTO | None:
        query: Update = (
            update(Order)
            .where(Order.id == order_id)
            .values(
                **order_data.model_dump(exclude_unset=True),
                updated_at=func.now(),
            )
            .returning(Order)
        )

        order: Order | None = await self.db.scalar(query)
        return OrderResponseDTO.model_validate(order) if order else None

    async def get_orders_by_filter(self, filters: OrderFilter) -> list[OrderResponseDTO]:
        query: Select = select(Order)

        if filters.user_id:
            query: Select = query.where(Order.user_id == filters.user_id)
        if filters.limit:
            query: Select = query.limit(filters.limit)
        if filters.offset:
            query: Select = query.offset(filters.offset)

        result: ScalarResult[Order] = await self.db.scalars(query)
        return [OrderResponseDTO.model_validate(order) for order in result.all()]

    async def get_orders_with_owner(self, filters: PaginationParams) -> list[OrderWithOwnerDTO]:
        query: Select = (
            select(Order).options(joinedload(Order.user)).order_by(Order.id).limit(filters.limit).offset(filters.offset)
        )

        result: ScalarResult[Order] = await self.db.scalars(query)
        return [OrderWithOwnerDTO.model_validate(order) for order in result.all()]
