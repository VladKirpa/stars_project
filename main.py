import logging
from fastapi import FastAPI
from app.api import users, orders, tasks, webhooks, finances
from app.config import settings

logger = logging.getLogger("uvicorn.error")

app = FastAPI()

app.include_router(users.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(webhooks.router, prefix="/api")
app.include_router(finances.router, prefix="/api")

@app.get('/')
async def root():
    return {'status': 'working', 'bot_connected': True}