from typing import TYPE_CHECKING

from starlette import status
from starlette.testclient import TestClient

from src.app.business_logic.accounts.dto.user import UserHashedPasswordDTO, UserResponseDTO
from src.app.infrastructure.accounts.repositories.user import UserRepository
from src.tests.conftest import TestAsyncSessionMaker

if TYPE_CHECKING:
    from httpx import Response


class TestUsers:
    async def test_registration(self, client: TestClient) -> None:
        username: str = 'user_1'
        email: str = 'user_1@test.com'

        body: dict = {
            'username': username,
            'email': email,
            'password': '123456789',
        }

        url: str = '/api/v1/users'

        response: Response = client.post(url, json=body)
        response_body: dict = response.json()

        assert response.status_code == status.HTTP_201_CREATED, response.text
        assert response_body.get('username') == username
        assert response_body.get('email') == email
        assert response_body.get('password') is None

        async with TestAsyncSessionMaker() as db:
            user: UserHashedPasswordDTO | None = await UserRepository(db).get_user_for_login(username)
            assert user.username == username
            assert user.email == email

    def test_get_users(self, client: TestClient, auth_headers: dict) -> None:
        url: str = '/api/v1/users'
        response: Response = client.get(url, headers=auth_headers)
        response_body: list[dict] = response.json()

        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response_body) > 0

    def test_get_user_me(self, client: TestClient, auth_headers: dict, base_test_user: UserResponseDTO) -> None:
        url: str = '/api/v1/users/me'
        response: Response = client.get(url, headers=auth_headers)
        response_body: dict = response.json()

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response_body == base_test_user.model_dump(mode='json')
