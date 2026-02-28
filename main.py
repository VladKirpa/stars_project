from fastapi import FastAPI
from app.api import users, orders, tasks, admin, webhooks, finances

app = FastAPI()
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(tasks.router)
app.include_router(admin.router)
app.include_router(webhooks.router)
app.include_router(finances.router)


@app.get('/')
async def root():
    return {'message': 'Hello!'}

