from typing import TYPE_CHECKING

from starlette import status
from starlette.testclient import TestClient

from src.app.bll.accounts.dto.user import UserResponseDTO

if TYPE_CHECKING:
    from httpx import Response


class TestUsers:
    async def test_get_users(self, client: TestClient, auth_headers: dict) -> None:
        url: str = '/api/v1/users'
        response: Response = client.get(url, headers=auth_headers)
        response_body: list[dict] = response.json()

        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response_body) > 0

    async def test_get_user_me(self, client: TestClient, auth_headers: dict, base_test_user: UserResponseDTO) -> None:
        url: str = '/api/v1/users/me'
        response: Response = client.get(url, headers=auth_headers)
        response_body: dict = response.json()

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response_body.get('id') == base_test_user.id
        assert response_body.get('username') == base_test_user.username
        assert response_body.get('email') == base_test_user.email

    # async def test_read_users_with_orders(self, client: TestClient, auth_headers) -> None:
    #     url: str = '/api/v1/...'
    #     response = client.get(url, headers=auth_headers)
    #
    #     assert response.status_code == status.HTTP_200_OK, response.text
    #     assert len(response.json()) > 0
