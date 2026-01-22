from src.app.business_logic.accounts.dto.user import UserResponseDTO
from src.app.business_logic.orders.dto.order import OrderResponseDTO


class OrderWithOwnerDTO(OrderResponseDTO):
    user: UserResponseDTO
