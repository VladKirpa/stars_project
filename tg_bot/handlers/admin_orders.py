from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import html

from app.config import settings
from tg_bot.utils.states import OrderCancelStates
from app.orm.admin.orders import cancel_order_by_admin

admin_orders_router = Router()

def is_admin(tg_id: int) -> bool:
    return tg_id in settings.ADMIN_IDS

@admin_orders_router.callback_query(F.data == "admin_cancel_order")
async def start_cancel_order(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
        
    await state.set_state(OrderCancelStates.waiting_for_id)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Отмена", callback_data="admin_back")]])
    await call.message.edit_text("🔢 Введи <b>ID заказа</b>, который нужно отменить:", reply_markup=kb, parse_mode="HTML")

@admin_orders_router.message(OrderCancelStates.waiting_for_id)
async def process_cancel_order(message: Message, state: FSMContext, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    order_input = message.text.strip()
    
    if not order_input.isdigit():
        return await message.answer("❌ Ошибка: ID должен состоять только из цифр. Попробуй еще раз:")

    try:
        order_id = int(order_input)
        result = await cancel_order_by_admin(order_id=order_id, session=session)
        
        await message.answer(
            f"✅ <b>Заказ #{order_id} отменен!</b>\n"
            f"💰 Возвращено юзеру: <code>{result['refunded_amount']}</code> звезд.\n"
            f"ℹ️ {result['message']}",
            parse_mode="HTML"
        )
        
    except Exception as e:
        error_text = str(e)
        if hasattr(e, 'detail'):
            error_text = e.detail
            
        await message.answer(f"❌ <b>Не удалось отменить заказ:</b>\n<code>{html.escape(error_text)}</code>", parse_mode="HTML")
    
    finally:
        await state.clear()