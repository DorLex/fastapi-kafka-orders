from typing import TYPE_CHECKING

from starlette import status
from starlette.testclient import TestClient

from src.app.bll.accounts.dto.user import UserResponseDTO

if TYPE_CHECKING:
    from httpx import Response


async def test_login_by_access_token(client: TestClient, test_user: UserResponseDTO) -> None:
    body: dict = {
        'username': test_user.username,
        'password': 'test_user_password',
    }

    url: str = '/api/v1/auth/token'

    response: Response = client.post(url, json=body)
    response_body: dict = response.json()

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response_body.get('access_token')
