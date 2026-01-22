from typing import TYPE_CHECKING

from _pytest.monkeypatch import MonkeyPatch
from starlette import status
from starlette.testclient import TestClient

from src.app.api.v1.orders import orders
from src.app.business_logic.orders.dto.order import OrderResponseDTO
from src.app.business_logic.orders.services.order import OrderService
from src.app.infrastructure.orders.repositories.order import OrderRepository
from src.tests.conftest import TestAsyncSessionMaker
from src.tests.mocks.kafka.producer import mock_get_producer

if TYPE_CHECKING:
    from httpx import Response


class TestOrderPositive:
    def test_get_orders(self, client: TestClient, auth_headers: dict) -> None:
        url: str = '/api/v1/orders'
        response: Response = client.get(url, headers=auth_headers)
        response_body: list[dict] = response.json()

        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response_body) > 0

    def test_get_my_orders(self, client: TestClient, auth_headers: dict) -> None:
        url: str = '/api/v1/orders/my'
        response: Response = client.get(url, headers=auth_headers)
        response_body: list[dict] = response.json()

        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response_body) > 0

    async def test_create_order(self, client: TestClient, auth_headers: dict, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setattr(orders, 'get_producer', mock_get_producer)

        title: str = 'title_1'
        description: str = 'description 1'

        body: dict = {
            'title': title,
            'description': description,
        }

        url: str = '/api/v1/orders'

        response: Response = client.post(url, json=body, headers=auth_headers)
        response_body: dict = response.json()

        assert response.status_code == status.HTTP_201_CREATED, response.text

        async with TestAsyncSessionMaker() as db:
            order_service: OrderService = OrderService(OrderRepository(db))
            order: OrderResponseDTO | None = await order_service.get_order_by_id(response_body.get('order_id'))

            assert order.title == title
            assert order.description == description

    def test_update_order_partial(
        self,
        client: TestClient,
        auth_headers: dict,
        base_test_order: OrderResponseDTO,
    ) -> None:
        url: str = f'/api/v1/orders/{base_test_order.id}'
        body: dict = {
            'title': 'new_title',
            'status': 'in_processing',
            'description': 'new description',
        }

        response: Response = client.patch(url, json=body, headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK, response.text
