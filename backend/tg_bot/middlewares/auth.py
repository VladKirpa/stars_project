from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        
        session: AsyncSession = data['session']
        
        tg_user = None
        if isinstance(event, Message):
            tg_user = event.from_user
        elif isinstance(event, CallbackQuery):
            tg_user = event.from_user
            
        if not tg_user:
            return await handler(event, data)

        user_db = await session.scalar(select(User).where(User.tg_id == tg_user.id))

        if user_db and user_db.is_banned:
            ban_text = "🚫 Ваш аккаунт заблокирован.\n\nПо вопросам разбана пишите: @managgee"
            
            if isinstance(event, Message):
                await event.answer(ban_text)
            elif isinstance(event, CallbackQuery):
                await event.answer(ban_text, show_alert=True)
            return 
        
        data['user_db'] = user_db
        
        return await handler(event, data)