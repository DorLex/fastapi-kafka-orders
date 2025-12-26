from src.app.bll.accounts.dto.user import UserResponseDTO
from src.app.bll.orders.dto.order import OrderResponseDTO


class UserWithOrdersDTO(UserResponseDTO):
    orders: list[OrderResponseDTO]
