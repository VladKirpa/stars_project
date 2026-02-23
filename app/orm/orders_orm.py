from app.models import Order, Task, TaskCompletion, User
from sqlalchemy import select, update, delete, func, join, insert
from sqlalchemy.orm import selectinload
from app.schemas.order import OrderCreate, OrderRead
from typing import List
import asyncio
from decimal import Decimal



PRICE_PER_SUB = Decimal("1") 
REWARD_PER_SUB = Decimal("0.25")


async def create_order(order_data: OrderCreate, session) -> Order:
    try:
        user = await session.scalar(select(User).where(order_data.creator_id == User.id)) # check is user exist
        if user:
            total_price = order_data.subs_quantity * PRICE_PER_SUB
            if user.stars_balance >= total_price:                   # check is stars balance enough to create order
                user.stars_balance -= total_price
                new_order = Order(
                    subs_quantity=order_data.subs_quantity,
                    channel_id=order_data.channel_id,
                    creator_id=order_data.creator_id,
                    action_type=order_data.action_type,
                    reward_for_sub=REWARD_PER_SUB
                )
                session.add(new_order)
                await session.commit()
                await session.refresh(new_order)
                return new_order                    # return new order
            else:
                raise ValueError('Insufissent stars_balance')
        else:
            raise NameError('Incorect user')

    except Exception as e:
        await session.rollback()
        raise e
    

async def get_created_orders(tg_id, session) -> list[Order]: # Allow creators get their order stats
    
    try:
        query = select(Order).join(User).where(tg_id == User.tg_id).options(selectinload(Order.tasks).selectinload(Task.completions))
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise e 



async def read_order(order: OrderRead, session) -> Order:
    pass