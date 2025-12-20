from src.app.accounts.schemas.user import UserOutSchema
from src.app.orders.schemas.order import OrderOutSchema


class UserWithOrdersSchema(UserOutSchema):
    orders: list[OrderOutSchema]
