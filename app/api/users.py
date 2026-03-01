from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter
import asyncio
from app.schemas.user import UserCreate, UserRead
from app.orm.users_orm import add_user, get_user_referrals
from app.database import get_db

router = APIRouter()

@router.post('/auth', response_model=UserRead)
async def auth(user_in: UserCreate, session = Depends(get_db)):
    try:
        user = await add_user(user_in, session)
        return user
    except Exception as e:
        print(f'Error {e}')
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get('/{tg_id}/referrals', response_model=list[UserRead])
async def get_referrals(tg_id: int, session = Depends(get_db)):
    # return referral by tg_id
    referrals = await get_user_referrals(tg_id, session)
    return referrals
    
