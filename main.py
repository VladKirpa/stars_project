from fastapi import FastAPI
from app.api import users, orders, tasks

app = FastAPI()
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(tasks.router)


@app.get('/')
async def root():
    return {'message': 'Hello!'}

