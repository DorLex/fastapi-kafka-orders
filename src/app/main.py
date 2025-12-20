from fastapi import FastAPI

from src.app.accounts.api import auth, registration, users
from src.app.orders.api import orders

app: FastAPI = FastAPI(title='Orders-App')

app.include_router(users.router)
app.include_router(orders.router)
app.include_router(registration.router)
app.include_router(auth.router)
