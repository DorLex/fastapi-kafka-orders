from src.app.bll.common.dto.filters import PaginationParams
from src.app.bll.orders.dto.filters import OrderFilter
from src.app.bll.orders.dto.order import OrderCreateDTO, OrderResponseDTO
from src.app.bll.orders.dto.order_with_owner import OrderWithOwnerDTO
from src.app.dal.orders.models.order import Order
from src.app.dal.orders.repositories.order import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    async def create_order(self, user_id: int, order_data: OrderCreateDTO) -> OrderResponseDTO:
        return await self.repository.create_order(user_id, order_data)

    async def get_orders_by_filter(self, filters: OrderFilter) -> list[OrderResponseDTO]:
        return await self.repository.get_orders_by_filter(filters)

    async def get_orders_with_owner(self, filters: PaginationParams) -> list[OrderWithOwnerDTO]:
        return await self.repository.get_orders_with_owner(filters)

    async def get_order_by_id(self, order_id: int) -> Order | None:
        return await self.repository.get_order_by_id(order_id)

    # async def update_status(self, order: Order, status: OrderStatusEnum) -> Order:
    #     # TODO: сделать в целом update_order, скорее всего частичный.
    #     return await self.repository.update_status(order, status)
