import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.config import settings
from tg_bot.utils.states import AdminStates

admin_alert_router = Router()

def is_admin(tg_id: int) -> bool:
    return tg_id in settings.ADMIN_IDS

@admin_alert_router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return

    await call.message.edit_text(
        "📢 <b>Режим рассылки</b>\n\n"
        "Отправь сообщение (текст, фото, видео или кружочек).\n"
        "Оно будет разослано всем пользователям бота.",
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_broadcast)
    await call.answer()

@admin_alert_router.message(AdminStates.waiting_for_broadcast)
async def process_broadcast(message: Message, state: FSMContext, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    
    status_msg = await message.answer("⏳ <i>Рассылка запущена. Это займет некоторое время...</i>", parse_mode="HTML")
    
    users = await session.scalars(select(User.tg_id))
    
    success_count = 0
    fail_count = 0
    
    for tg_id in users:
        try:
            await message.send_copy(chat_id=tg_id)
            success_count += 1
            await asyncio.sleep(0.05) 
        except Exception:
            fail_count += 1

    await status_msg.edit_text(
        f"✅ <b>Рассылка успешно завершена!</b>\n\n"
        f"📬 Доставлено: <b>{success_count}</b>\n"
        f"❌ Не доставлено (бокировка/удален): <b>{fail_count}</b>",
        parse_mode="HTML"
    )