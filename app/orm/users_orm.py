from app.models import User
from app.database import async_session_factory
from sqlalchemy import select, update, delete, func
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserRead
from typing import List
import asyncio

async def add_user(user_in: UserRead, session) -> User:
    user = await session.scalar(select(User).where(User.tg_id == user_in.tg_id))
    if user:
        udpated_data = user_in.model_dump()
        for k,v in udpated_data.items():
            if k == 'tg_id':
                continue
            
            if v != getattr(user, k, v):
                setattr(user, k,v)

        await session.commit()
        return user
        
    #if not exist
    new_user = User(**user_in.model_dump())
    session.add(new_user)
    await session.commit() # save to get ID 
    await session.refresh(new_user) # refresh object to get correct ID 
    return new_user
    


