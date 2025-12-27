from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


async def test_login_by_access_token(app: FastAPI, client: AsyncClient):
    user_data = {
        'username': 'test_user_for_auth',
        'email': 'test-user-for-auth@test.com',
        'password': '123456789',
    }

    url_registration = app.url_path_for('user_registration')
    await client.post(url_registration, json=user_data)

    url_login = app.url_path_for('login_by_access_token')
    response = await client.post(url_login, data=user_data)

    assert response.status_code == status.HTTP_200_OK, response.text
