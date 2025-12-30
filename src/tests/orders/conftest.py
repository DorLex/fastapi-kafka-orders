# import pytest
#
# from src.app.dal.orders.models.order import Order
# from src.app.dal.orders.repositories.order import OrderRepository
# from src.app.bll.orders.dto.order import OrderCreateSchema
# from src.tests.conftest import SessionTest
#
#
# @pytest.fixture(scope='session')
# async def base_test_order_data():
#     return {
#         'title': 'base_test_order',
#         'description': 'base_test_order description',
#     }
#
#
# @pytest.fixture(scope='session', autouse=True)
# async def base_test_order(prepare_db, base_test_user, base_test_order_data):
#     order = OrderCreateSchema(**base_test_order_data)
#
#     async with SessionTest() as session:
#         db_order: Order = await OrderRepository(session).create_order(base_test_user, order)
#         await session.commit()
#
#         return db_order
