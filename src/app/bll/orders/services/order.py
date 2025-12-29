from src.app.dal.accounts.models.user import User
from src.app.bll.orders.dto.order import OrderCreateSchema
from src.common.constants.order import OrderStatusEnum
from src.app.dal.orders.models.order import Order
from src.app.dal.orders.repositories.order import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    async def create_order(self, user_id: int, order: OrderCreateSchema) -> Order:
        return await self.repository.create_order(user_id, order)

    async def get_orders(self, skip: int = 0, limit: int = 100) -> list[Order]:
        return await self.repository.get_orders(skip, limit)

    async def get_orders_with_owner(self, skip: int = 0, limit: int = 100) -> list[Order]:
        return await self.repository.get_orders_with_owner(skip, limit)

    async def get_order_by_id(self, order_id: int) -> Order | None:
        return await self.repository.get_order_by_id(order_id)

    async def get_order_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Order]:
        return await self.repository.get_order_by_user(user_id, skip, limit)

    async def update_status(self, order: Order, status: OrderStatusEnum) -> Order:
        # TODO: сделать в целом update_order, скорее всего частичный.
        return await self.repository.update_status(order, status)
