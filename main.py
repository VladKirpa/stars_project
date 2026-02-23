from fastapi import FastAPI
from app.api import users, orders

app = FastAPI()
app.include_router(users.router)
app.include_router(orders.router)


@app.get('/')
async def root():
    return {'message': 'Hello world!'}






{
  "subs_amount": 100,
  "reward_for_sub": 0.5,
  "channel_id": "tg/channel",
  "creator_id": 90,
  "action_type": "SUBSCRIBE_CHANNEL"
}