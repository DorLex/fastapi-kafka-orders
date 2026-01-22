from typing import TYPE_CHECKING

from starlette import status
from starlette.testclient import TestClient

from src.app.business_logic.orders.dto.order import OrderResponseDTO

if TYPE_CHECKING:
    from httpx import Response


class TestOrderNegative:
    def test_create_order(self, client: TestClient, auth_headers: dict) -> None:
        url: str = '/api/v1/orders'
        body: dict = {'incorrect_field': 'qwe'}

        response: Response = client.post(url, json=body, headers=auth_headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT, response.text

    def test_update_order_partial(
        self,
        client: TestClient,
        auth_headers: dict,
        base_test_order: OrderResponseDTO,
    ) -> None:
        url: str = f'/api/v1/orders/{base_test_order.id}'
        body: dict = {'status': 'incorrect_status'}

        response: Response = client.patch(url, json=body, headers=auth_headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT, response.text
