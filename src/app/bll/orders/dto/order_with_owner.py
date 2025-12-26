from src.app.bll.accounts.dto import UserResponseDTO
from src.app.bll.orders.dto.order import OrderResponseDTO


class OrderWithOwnerSchema(OrderResponseDTO):
    owner: UserResponseDTO
