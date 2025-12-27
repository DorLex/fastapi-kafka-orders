from fastapi import FastAPI

from src.app.api.accounts import auth, users
from src.app.api.orders import orders

app: FastAPI = FastAPI(title='Orders-App')

app.include_router(users.router)
app.include_router(orders.router)
app.include_router(auth.router)
