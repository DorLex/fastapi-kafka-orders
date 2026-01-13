from typing import TYPE_CHECKING

from starlette import status
from starlette.testclient import TestClient

if TYPE_CHECKING:
    from httpx import Response


class TestUsers:
    async def test_get_users(self, client: TestClient, auth_headers: dict) -> None:
        url: str = '/api/v1/users'
        response: Response = client.get(url, headers=auth_headers)
        response_body: list[dict] = response.json()

        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response_body) > 0

    # async def test_read_users_me(self, client: TestClient, auth_headers, base_test_user_data) -> None:
    #     url: str = '/api/v1/...'
    #     response = client.get(url, headers=auth_headers)
    #
    #     assert response.status_code == status.HTTP_200_OK, response.text
    #     assert response.json().get('username') == base_test_user_data.get('username')
    #
    # async def test_read_users_with_orders(self, client: TestClient, auth_headers) -> None:
    #     url: str = '/api/v1/...'
    #     response = client.get(url, headers=auth_headers)
    #
    #     assert response.status_code == status.HTTP_200_OK, response.text
    #     assert len(response.json()) > 0
