from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter
import asyncio
from app.schemas.user import UserCreate, UserRead
from app.orm.users_orm import add_user
from app.database import get_db, async_session_factory

router = APIRouter()

@router.post('/auth', response_model=UserRead)
async def auth(user_in: UserCreate, session = Depends(get_db)):
    try:
        user = await add_user(user_in, session)
        return user
    except Exception as e:
        print(f'Error {e}')
        raise HTTPException(status_code=500, detail=str(e))
        
    
