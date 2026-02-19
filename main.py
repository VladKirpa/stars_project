from fastapi import FastAPI
from app.api import users

app = FastAPI()
app.include_router(users.router)


@app.get('/')
async def root():
    return {'message': 'Hello world!'}

