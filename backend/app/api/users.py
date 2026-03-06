from fastapi import FastAPI, Depends, HTTPException, APIRouter
import asyncio
from app.schemas.user import UserCreate, UserRead
from app.orm.users_orm import add_user, get_user_referrals
from app.database import get_db
from sqlalchemy import select, func
from app.models.task import TaskCompletion, CompletionStatus
from app.models.user import User

router = APIRouter()

@router.post('/auth', response_model=UserRead)
async def auth(user_in: UserCreate, session=Depends(get_db)):
    try:
        user = await add_user(user_in, session)
        
        frozen_query = select(func.sum(TaskCompletion.stars_reward)).where(
            TaskCompletion.user_complete == user.id,
            TaskCompletion.status == CompletionStatus.FROZEN
        )
        frozen_sum = await session.scalar(frozen_query) or 0
        
        count_query = select(func.count(TaskCompletion.id)).where(
            TaskCompletion.user_complete == user.id,
            TaskCompletion.status.in_([CompletionStatus.FROZEN, CompletionStatus.COMPLETED])
        )
        tasks_count = await session.scalar(count_query) or 0

        ref_count_query = select(func.count(User.id)).where(User.referral_id == user.tg_id)
        ref_count = await session.scalar(ref_count_query) or 0

        user.frozen_balance = frozen_sum
        user.completed_tasks_count = tasks_count
        user.referrals_count = ref_count

        return user
    except Exception as e:
        print(f'Error {e}')
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get('/{tg_id}/referrals', response_model=list[UserRead])
async def get_referrals(tg_id: int, session = Depends(get_db)):
    referrals = await get_user_referrals(tg_id, session)
    return referrals