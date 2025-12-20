from fastapi import FastAPI

from src.app.accounts.routers import auth, registration, users
from src.app.orders.routers import orders
from src.app.notifications.routers import router as notifications_router

app = FastAPI(
    title='Orders App',
)

app.include_router(users.router)
app.include_router(orders.router)
app.include_router(registration.router)
app.include_router(auth.router)
app.include_router(notifications_router)
