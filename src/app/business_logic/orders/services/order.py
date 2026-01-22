from fastapi import HTTPException
from starlette import status

from src.app.business_logic.common.dto.filters import PaginationParams
from src.app.business_logic.orders.dto.filters import OrderFilter
from src.app.business_logic.orders.dto.order import OrderCreateDTO, OrderPartialUpdateDTO, OrderResponseDTO
from src.app.business_logic.orders.dto.order_with_owner import OrderWithOwnerDTO
from src.app.infrastructure.orders.repositories.order import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    async def create_order(self, user_id: int, order_data: OrderCreateDTO) -> OrderResponseDTO:
        return await self.repository.create_order(user_id, order_data)

    async def get_order_by_id(self, order_id: int) -> OrderResponseDTO | None:
        return await self.repository.get_order_by_id(order_id)

    async def update_order_partial(self, order_id: int, order_data: OrderPartialUpdateDTO) -> OrderResponseDTO:
        updated_order: OrderResponseDTO | None = await self.repository.update_order_partial(order_id, order_data)
        if not updated_order:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f'Заказ не найден: {order_id=}',
            )

        return updated_order

    async def get_orders_by_filter(self, filters: OrderFilter) -> list[OrderResponseDTO]:
        return await self.repository.get_orders_by_filter(filters)

    async def get_orders_with_owner(self, filters: PaginationParams) -> list[OrderWithOwnerDTO]:
        return await self.repository.get_orders_with_owner(filters)
