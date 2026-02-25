from app.models import Order, Task, TaskCompletion, User
from sqlalchemy import select, update, delete, func, join, insert, and_, outerjoin
from sqlalchemy.orm import selectinload
from app.schemas.order import OrderCreate, OrderRead
from typing import List
import asyncio
from decimal import Decimal
from app.config import SYSTEM_BANK_ID
from fastapi import HTTPException


async def find_available_task(user_id: int, session) -> list[Task]:
    # Select all tasks with antijoin where TaskCompletions is None to find available tasks for user
    query = (
            select(Task)
            .join(Order)
            .outerjoin(
                TaskCompletion,
                and_(
                    TaskCompletion.user_complete==user_id,
                    TaskCompletion.task_id==Task.id
                )
            )
            .where(
                TaskCompletion.id.is_(None),
                Order.status == 'pending'
            ).options(
                (selectinload(Task.order))
            )
        )
    
    result = await session.execute(query)
    return result.scalars().all()

    


async def complete_task_transaction(user_id: int, task_id: int, session):
    try: 
        is_complete = await session.scalar(select(TaskCompletion).where(
            TaskCompletion.user_complete==user_id,
            TaskCompletion.task_id==task_id
        ))      # block repeated execution

        if is_complete:
            raise HTTPException(status_code=400, detail='Task already done')
        
        order = await session.scalar(select(Order)
        .join(Task, Order.id == Task.order_id)
        .where(Task.id == task_id)
        .with_for_update()
        ) 

        if not order or order.status != 'pending':      # check order status
            raise HTTPException(400, detail='Order not available')
        
        counter = select(func.count(TaskCompletion.id)).select_from(TaskCompletion).join(Task).where(order.id == Task.order_id) # check is available task to complete
        count_curr_subs = await session.scalar(counter)
        if count_curr_subs >= order.subs_quantity:
            raise HTTPException(status_code=400, detail='Task not available')
        
        #Transaction 

        session.add(TaskCompletion(user_complete=user_id, task_id=task_id))
        worker = await session.get(User, user_id)
        if not worker:
            raise HTTPException(status_code=400, detail='User do not exists')
        system_bank = await session.get(User, SYSTEM_BANK_ID)                         #  <--- system bank id (change in config)

        if not system_bank: 
            raise HTTPException(status_code=400, detail='Bank account not defined')

        system_bank.stars_balance -= order.reward_for_sub                # write off full price from Escrow
        worker.balance += order.worker_pay                               # pay worker for task
        system_bank.balance += order.reward_for_sub - order.worker_pay   # count service margin and put it to bank balance

        if count_curr_subs + 1 >= order.subs_quantity:                   # close order if it was last sub
            order.status = 'completed'
        
        await session.commit()
        return {'message': 'Task compete successful'}

    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc

    except Exception as e:
        await session.rollback()
        print(f'Critical error: {repr(e)}')
        raise HTTPException(status_code=500, detail='Something went wrong')
        