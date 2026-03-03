from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter
import asyncio
from app.schemas.task import TaskRead
from app.orm.tasks_orm import find_available_task, complete_task_transaction
from app.database import get_db
from app.celery_app import unlock_funds_task
from sqlalchemy import select, func
from app.models import User
from app.models.task import TaskCompletion, CompletionStatus

router = APIRouter()

@router.get('/tasks/available', response_model=list[TaskRead])
async def get_available_tasks(user_id: int, session=Depends(get_db)):
    # user_id - tg id from frontend
    internal_user = await session.scalar(
        select(User).where(User.tg_id == user_id)
    )
    
    if not internal_user:
        return []

    # here DB id
    available_tasks = await find_available_task(internal_user.id, session)
    return available_tasks


@router.post('/tasks/complete')
async def complete_task(user_id:int, task_id:int ,session=Depends(get_db)) -> dict:

    is_completed = await complete_task_transaction(user_id, task_id, session)
    
    if is_completed:
        
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        
        if user and user.referral_id:
            count_query = select(func.count(TaskCompletion.id)).where(
                TaskCompletion.user_complete == user.id,
                TaskCompletion.status.in_([CompletionStatus.FROZEN, CompletionStatus.COMPLETED])
            )
            total_completed = await session.scalar(count_query) or 0
            
            if total_completed == 10:
                referrer = await session.scalar(
                    select(User).where(User.tg_id == user.referral_id).with_for_update()
                )
                if referrer:
                    referrer.balance += 3
                    referrer.referral_earned += 3
                    await session.commit()

        return is_completed
    
    raise HTTPException(status_code=400, detail="Task completion failed")


@router.post('/tasks/force-unlock-check')
async def trigger_unlock_funds():
    #manual balance unlock
    task = unlock_funds_task.delay()
    return {"status": "Task sent to worker", "celery_task_id": task.id}

