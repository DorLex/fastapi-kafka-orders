import pytest

from src.app.bll.accounts.dto.user import UserResponseDTO
from src.app.bll.orders.dto.order import OrderCreateDTO, OrderResponseDTO
from src.app.bll.orders.services.order import OrderService
from src.app.dal.orders.repositories.order import OrderRepository
from src.tests.conftest import TestAsyncSessionMaker

# @pytest.fixture(scope='session')
# async def base_test_order_data():
#     return {
#         'title': 'base_test_order',
#         'description': 'base_test_order description',
#     }


@pytest.fixture(scope='session')
async def base_test_order_data() -> OrderCreateDTO:
    return OrderCreateDTO(title='test_order', description='test_order_description')


@pytest.fixture(scope='session', autouse=True)
async def base_test_order(base_test_user: UserResponseDTO, base_test_order_data: OrderCreateDTO) -> OrderResponseDTO:
    async with TestAsyncSessionMaker() as db:
        order_service: OrderService = OrderService(OrderRepository(db))
        order: OrderResponseDTO = await order_service.create_order(base_test_user.id, base_test_order_data)
        await db.commit()

    return order
