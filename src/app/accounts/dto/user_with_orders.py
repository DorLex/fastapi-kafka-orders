from src.app.accounts.dto.user import UserResponseDTO
from src.app.orders.dto.order import OrderResponseDTO


class UserWithOrdersDTO(UserResponseDTO):
    orders: list[OrderResponseDTO]
