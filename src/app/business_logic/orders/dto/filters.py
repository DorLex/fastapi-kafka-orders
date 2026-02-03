from pydantic import PositiveInt

from src.app.business_logic.common.dto.filters import PaginationParams


class OrderFilter(PaginationParams):
    user_id: PositiveInt = None
