from pydantic import PositiveInt

from src.app.bll.common.dto.filters import PaginationParams


class OrderFilter(PaginationParams):
    user_id: PositiveInt = None
