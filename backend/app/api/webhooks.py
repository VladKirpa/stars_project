import logging
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aiogram import types
from app.database import get_db
from app.orm.procces_leave_orm import process_user_leave
from app.models import Order
from tg_bot.run_bot import dp, bot

logger = logging.getLogger("uvicorn.error")
router = APIRouter()

@router.post("/webhook")
async def telegram_webhook(request: Request, session: AsyncSession = Depends(get_db)):
    try:
        update_data = await request.json()
        if not update_data:
            return {"ok": True}

        update = types.Update.model_validate(update_data, context={"bot": bot})

        if "chat_member" in update_data:
            chat_member = update_data["chat_member"]
            new_status = chat_member["new_chat_member"]["status"]
            
            if new_status in ["left", "kicked"]:
                chat_id = chat_member["chat"]["id"]
                chat_username = chat_member["chat"].get("username")
                user_id = chat_member["new_chat_member"]["user"]["id"]
                
                target_url = f"https://t.me/{chat_username}" if chat_username else str(chat_id)
                
                stmt = select(Order.id).where(Order.channel_id == target_url).limit(1)
                order_id = await session.scalar(stmt)
                
                if order_id:
                    await process_user_leave(user_id=user_id, order_id=order_id, session=session)

        await dp.feed_update(bot, update)

    except Exception as e:
        logger.error(f"WEBHOOK error: {str(e)}", exc_info=True)

    return {"ok": True}