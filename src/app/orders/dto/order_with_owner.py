from src.app.accounts.dto.user import UserResponseDTO
from src.app.orders.dto.order import OrderResponseDTO


class OrderWithOwnerSchema(OrderResponseDTO):
    owner: UserResponseDTO
