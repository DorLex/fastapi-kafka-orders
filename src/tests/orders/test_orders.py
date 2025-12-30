# import pytest
# from httpx import AsyncClient
# from starlette import status
#
# from src.common.constants.order import OrderStatusEnum
# from src.app.dal.orders.models.order import Order
# from src.app.dal.orders.repositories.order import OrderRepository
# from src.app.api.v1.orders import orders
# from src.tests.conftest import SessionTest, main_app
# from src.tests.orders.mocks import mock_get_producer
#
#
# class TestOrdersPositive:
#     order_data = {
#         'title': 'test_order_1',
#         'description': 'test_order_1 description',
#     }
#
#     url_orders = main_app.url_path_for('read_orders')
#     url_orders_my = main_app.url_path_for('read_my_orders')
#     url_orders_with_owner = main_app.url_path_for('read_orders_with_owner')
#
#     async def test_read_orders(self, client: AsyncClient, auth_headers):
#         response = await client.get(self.url_orders, headers=auth_headers)
#
#         assert response.status_code == status.HTTP_200_OK, response.text
#         assert len(response.json()) > 0
#
#     async def test_add_order(self, client: AsyncClient, auth_headers, monkeypatch):
#         monkeypatch.setattr(orders, 'get_producer', mock_get_producer)
#
#         response = await client.post(self.url_orders, json=self.order_data, headers=auth_headers)
#         assert response.status_code == status.HTTP_201_CREATED, response.text
#
#         order_id = response.json().get('order_id')
#         async with SessionTest() as session:
#             db_order: Order = await OrderRepository(session).get_order_by_id(order_id)
#             assert db_order.title == self.order_data.get('title')
#             assert db_order.description == self.order_data.get('description')
#
#     async def test_read_my_orders(self, client: AsyncClient, auth_headers):
#         response = await client.get(self.url_orders_my, headers=auth_headers)
#
#         assert response.status_code == status.HTTP_200_OK, response.text
#         assert len(response.json()) > 0
#
#     async def test_read_orders_with_owner(self, client: AsyncClient, auth_headers):
#         response = await client.get(self.url_orders_with_owner, headers=auth_headers)
#
#         assert response.status_code == status.HTTP_200_OK, response.text
#         assert len(response.json()) > 0
#
#     async def test_update_order_status(self, base_test_order):
#         async with SessionTest() as session:
#             db_order: Order = await OrderRepository(session).update_status(
#                 base_test_order,
#                 OrderStatusEnum.completed,
#             )
#             await session.commit()
#
#             assert db_order.status == OrderStatusEnum.completed
#
#
# class TestOrdersNegative:
#     incorrect_order_data = {
#         'title': 'test_order_2',
#     }
#
#     url_orders = main_app.url_path_for('add_order')
#
#     async def test_add_order(self, client: AsyncClient, auth_headers):
#         response = await client.post(self.url_orders, json=self.incorrect_order_data, headers=auth_headers)
#         assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
#
#     async def test_update_order_status(self, base_test_order):
#         async with SessionTest() as session:
#             with pytest.raises(ValueError):
#                 await OrderRepository(session).update_status(base_test_order, 'incorrect_status')  # type: ignore
