from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter
import asyncio
from app.schemas.task import TaskRead
from app.orm.tasks_orm import find_available_task
from app.database import get_db


router = APIRouter()

@router.get('/tasks/available', response_model=list[TaskRead])
async def get_available_tasks(user_id:int, session=Depends(get_db)):
    
    try:
        available_tasks = await find_available_task(user_id, session)
        return available_tasks
    except Exception as e:
        print(f'Error {e}')
        raise HTTPException(500, detail=str(e))
    