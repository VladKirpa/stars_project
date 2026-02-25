from app.models import Order, Task, TaskCompletion, User
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.schemas.order import OrderCreate, OrderRead
from app.config import DEFAULT_REWARD_FOR_SUB, DEFAULT_WORKER_PAY, SYSTEM_BANK_ID
from fastapi import HTTPException


async def create_order(order_data: OrderCreate, session) -> Order:
    try:
        user = await session.scalar(select(User).where(order_data.creator_id == User.id).with_for_update()) # check is user exist
        if user:
            total_price = order_data.subs_quantity * DEFAULT_REWARD_FOR_SUB
            if user.stars_balance >= total_price:                   # check is stars balance enough to create order
                user.stars_balance -= total_price
                bank = await session.get(User, SYSTEM_BANK_ID) 
                bank.stars_balance += total_price                       # send total price to bank
                new_order = Order(
                    subs_quantity=order_data.subs_quantity,
                    channel_id=order_data.channel_id,
                    creator_id=order_data.creator_id,
                    action_type=order_data.action_type,
                    reward_for_sub=DEFAULT_REWARD_FOR_SUB,
                    worker_pay=DEFAULT_WORKER_PAY,
                    description=order_data.description
                )
                session.add(new_order)
                await session.flush()       # set new order id to create task
                new_task = Task(order_id=new_order.id)
                session.add(new_task)
                await session.commit()
                await session.refresh(new_order)
                return new_order
            else:
                raise HTTPException(status_code=400 ,detail='Insufissent stars_balance')
        else:
            raise HTTPException(status_code=400 ,detail='Incorect user')
    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc

    except Exception as e:
        await session.rollback()
        raise e
    

async def get_created_orders(tg_id, session) -> list[Order]: # Allow creators get their order stats

    query = select(Order).join(User).where(tg_id == User.tg_id).options(selectinload(Order.tasks).selectinload(Task.completions))
    result = await session.execute(query)
    return result.scalars().all()
    



async def read_order(order: OrderRead, session) -> Order:
    pass