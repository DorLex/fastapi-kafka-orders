from fastapi import APIRouter

from src.app.api.v1.accounts import auth, users
from src.app.api.v1.orders import orders

api_v1_router: APIRouter = APIRouter(prefix='/api/v1')

api_v1_router.include_router(auth.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(orders.router)
