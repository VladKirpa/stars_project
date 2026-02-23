from app.models import Order, Task, TaskCompletion, User
from sqlalchemy import select, update, delete, func, join, insert, and_, outerjoin
from sqlalchemy.orm import selectinload
from app.schemas.order import OrderCreate, OrderRead
from typing import List
import asyncio
from decimal import Decimal



async def find_available_task(user_id: int, session) -> list[Task]:

    try:
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
    except Exception as e:
        raise e
    
