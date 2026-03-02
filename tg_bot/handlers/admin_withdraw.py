from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
import html

from app.config import settings
from app.orm.admin.finances import (
    count_pending_withdrawals, 
    get_pending_withdrawal_by_offset,
    approve_withdraw_transaction,
    reject_withdraw_transaction
)

admin_withdraw_router = Router()

def is_admin(tg_id: int) -> bool:
    return tg_id in settings.ADMIN_IDS

@admin_withdraw_router.callback_query(F.data.startswith("admin_withdraws_"))
async def show_withdrawals_page(call: CallbackQuery, session: AsyncSession, page_override: int = None):
    if not is_admin(call.from_user.id):
        return

    if page_override is not None:
        page = page_override
    else:
        try:
            page = int(call.data.split("_")[2])
        except (IndexError, ValueError):
            page = 0
    
    total = await count_pending_withdrawals(session)
    
    if total == 0:
        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="admin_back")]])
        return await call.message.edit_text("💸 <b>Нет активных заявок на вывод.</b>", reply_markup=kb, parse_mode="HTML")

    if page < 0: page = total - 1
    if page >= total: page = 0

    data = await get_pending_withdrawal_by_offset(session, offset=page)
    if not data:
        return await call.answer("Заявка не найдена", show_alert=True)
        
    request = data['request']
    user = data['user']

    text = (
        f"💸 <b>Заявка на вывод #{request.id}</b> ({page + 1} из {total})\n\n"
        f"👤 <b>Юзер:</b> @{user.username or 'Нет'} (ID: <code>{user.id}</code>)\n"
        f"💰 <b>Сумма к выводу:</b> {request.amount}\n"
        f"📅 <b>Дата:</b> {request.created_at.strftime('%Y-%m-%d %H:%M')}\n"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"admin_with_ok_{request.id}_{user.id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"admin_with_no_{request.id}_{user.id}")
        ],
        [
            InlineKeyboardButton(text="⬅️ Пред.", callback_data=f"admin_withdraws_{page - 1}"),
            InlineKeyboardButton(text="След. ➡️", callback_data=f"admin_withdraws_{page + 1}")
        ],
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="admin_back")]
    ])

    await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@admin_withdraw_router.callback_query(F.data.startswith("admin_with_"))
async def process_withdrawal_action(call: CallbackQuery, session: AsyncSession):
    if not is_admin(call.from_user.id):
        return

    parts = call.data.split("_")
    action = parts[2]
    withdraw_id = int(parts[3])
    target_user_id = int(parts[4])

    try:
        if action == "ok":
            res = await approve_withdraw_transaction(user_id=target_user_id, withdraw_id=withdraw_id, session=session)
            await call.answer("✅ " + res["message"], show_alert=True)
        elif action == "no":
            res = await reject_withdraw_transaction(user_id=target_user_id, withdraw_id=withdraw_id, session=session)
            await call.answer("❌ " + res["message"], show_alert=True)
            
        await show_withdrawals_page(call, session, page_override=0)
        
    except Exception as e:
        safe_error = html.escape(str(e))
        await call.message.answer(f"❌ <b>Ошибка:</b>\n<code>{safe_error}</code>", parse_mode="HTML")