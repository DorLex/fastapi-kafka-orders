from typing import TYPE_CHECKING

from starlette import status
from starlette.testclient import TestClient

from src.app.bll.accounts.dto.user import UserCreateDTO

if TYPE_CHECKING:
    from httpx import Response


async def test_login(client: TestClient, base_test_user_credentials: UserCreateDTO) -> None:
    url: str = '/api/v1/auth/token'

    body: dict = {
        'username': base_test_user_credentials.username,
        'password': base_test_user_credentials.password,
    }

    response: Response = client.post(url, json=body)
    response_body: dict = response.json()

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response_body.get('access_token')
