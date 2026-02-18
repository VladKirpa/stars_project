from app.models import User
from app.database import async_session_factory
from sqlalchemy import select, update, delete, func
from pydantic import BaseModel, ConfigDict
from typing import List
import asyncio

async def add_user(tg_id):
    async with async_session_factory() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user
        
        #if not exist
        new_user = User(tg_id=tg_id, username='popabobra')
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    


