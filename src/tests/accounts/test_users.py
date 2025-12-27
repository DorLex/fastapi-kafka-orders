from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


class TestUsers:

    async def test_read_users(self, app: FastAPI, client: AsyncClient, auth_headers):
        url = app.url_path_for('read_users')
        response = await client.get(url, headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response.json()) > 0

    async def test_read_users_me(self, app: FastAPI, client: AsyncClient, auth_headers, base_test_user_data):
        url = app.url_path_for('read_users_me')
        response = await client.get(url, headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json().get('username') == base_test_user_data.get('username')

    async def test_read_users_with_orders(self, app: FastAPI, client: AsyncClient, auth_headers):
        url = app.url_path_for('read_users_with_orders')
        response = await client.get(url, headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response.json()) > 0
