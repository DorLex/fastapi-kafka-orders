from sqlalchemy.ext.asyncio import AsyncSession

from src.app.accounts.models import User
from src.app.notifications import EmailSchema
from src.app.notifications.services.email_build import EmailBuildService
from src.app.notifications import EmailNotificationService
from src.app.orders.enums import OrderStatusEnum
from src.app.orders.models import Order
from src.app.orders.repository import OrderRepository
from src.app.orders.schemas.order import OrderCreateSchema


class OrderService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = OrderRepository(self._session)
        self._notification_service = EmailNotificationService()
        self._email_build_service = EmailBuildService()

    async def create(self, db_user: User, order: OrderCreateSchema) -> Order:
        return await self._repository.create(db_user, order)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Order]:
        return await self._repository.get_all(skip, limit)

    async def get_all_with_owner(self, skip: int = 0, limit: int = 100) -> list[Order]:
        return await self._repository.get_all_with_owner(skip, limit)

    async def get_by_id(self, order_id: int) -> Order:
        return await self._repository.get_by_id(order_id)

    async def get_by_user(self, db_user: User, skip: int = 0, limit: int = 100) -> list[Order]:
        return await self._repository.get_by_user(db_user, skip, limit)

    async def update_status(self, db_order: Order, status: OrderStatusEnum) -> Order:
        updated_order = await self._repository.update_status(db_order, status)
        email: EmailSchema = self._email_build_service.build_order_status_changed_email(updated_order)
        await self._notification_service.send_email(email)

        return updated_order
