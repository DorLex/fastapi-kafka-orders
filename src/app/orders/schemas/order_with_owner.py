from src.app.accounts.schemas import UserOutSchema
from src.app.orders.schemas.order import OrderOutSchema


class OrderWithOwnerSchema(OrderOutSchema):
    owner: UserOutSchema
