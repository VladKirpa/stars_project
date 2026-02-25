from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter
import asyncio
from app.schemas.task import TaskRead
from app.orm.tasks_orm import find_available_task, complete_task_transaction
from app.database import get_db


router = APIRouter()

@router.get('/tasks/available', response_model=list[TaskRead])
async def get_available_tasks(user_id:int, session=Depends(get_db)):

    available_tasks = await find_available_task(user_id, session)
    return available_tasks

    

@router.post('/tasks/complete')
async def complete_task(user_id:int, task_id:int ,session=Depends(get_db)) -> dict:

    is_completed = await complete_task_transaction(user_id, task_id, session)
    if is_completed:
        return is_completed
        