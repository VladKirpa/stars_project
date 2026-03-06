from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User

async def get_current_user(
    x_user_id: int = Header(..., description="ID пользователя из Telegram"), 
    session: AsyncSession = Depends(get_db)
) -> User:
    
    user = await session.scalar(select(User).where(User.tg_id == x_user_id))
    
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized: User not found")
    if user.is_banned:
        raise HTTPException(status_code=403, detail="User is banned")
        
    return user