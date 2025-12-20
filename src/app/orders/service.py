from src.app.accounts.models import User
from src.app.orders.dto.order import OrderCreateSchema
from src.app.orders.enums import OrderStatusEnum
from src.app.orders.models import Order
from src.app.orders.repository import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    async def create_order(self, db_user: User, order: OrderCreateSchema) -> Order:
        return await self.repository.create_order(db_user, order)

    async def get_orders(self, skip: int = 0, limit: int = 100) -> list[Order]:
        return await self.repository.get_orders(skip, limit)

    async def get_orders_with_owner(self, skip: int = 0, limit: int = 100) -> list[Order]:
        return await self.repository.get_orders_with_owner(skip, limit)

    async def get_order_by_id(self, order_id: int) -> Order | None:
        return await self.repository.get_order_by_id(order_id)

    async def get_order_by_user(self, user: User, skip: int = 0, limit: int = 100) -> list[Order]:
        return await self.repository.get_order_by_user(user, skip, limit)

    async def update_status(self, order: Order, status: OrderStatusEnum) -> Order:
        # TODO: сделать в целом update_order, скорее всего частичный.
        return await self.repository.update_status(order, status)
