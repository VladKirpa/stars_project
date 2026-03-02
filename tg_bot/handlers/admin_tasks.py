import html
from decimal import Decimal
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from tg_bot.utils.states import TaskCreateStates
from app.orm.admin.create_custom_tasks import create_custom_admin_order

admin_tasks_router = Router()

def is_admin(tg_id: int) -> bool:
    return tg_id in settings.ADMIN_IDS

# ask for channel url
@admin_tasks_router.callback_query(F.data == "admin_create_task")
async def start_task_creation(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
        
    await state.set_state(TaskCreateStates.waiting_for_url)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="admin_back")]])
    await call.message.edit_text("🔗 <b>Шаг 1/4:</b> Введи URL канала (например, https://t.me/channel):", reply_markup=kb, parse_mode="HTML")

# subs quantity
@admin_tasks_router.message(TaskCreateStates.waiting_for_url)
async def process_task_url(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
        
    await state.update_data(channel_url=message.text.strip())
    await state.set_state(TaskCreateStates.waiting_for_subs)
    
    await message.answer("👥 <b>Шаг 2/4:</b> Количество подписчиков? (целое число):", parse_mode="HTML")

# price for sub
@admin_tasks_router.message(TaskCreateStates.waiting_for_subs)
async def process_task_subs(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
        
    try:
        subs = int(message.text.strip())
        if subs <= 0:
            raise ValueError
    except ValueError:
        return await message.answer("❌ Ошибка: Введи корректное целое число больше нуля.")
        
    await state.update_data(subs_quantity=subs)
    await state.set_state(TaskCreateStates.waiting_for_pay)
    
    await message.answer("💸 <b>Шаг 3/4:</b> Какая будет оплата за 1 подписку? (Можно с точкой например 2.5):", parse_mode="HTML")

# ask description for task
@admin_tasks_router.message(TaskCreateStates.waiting_for_pay)
async def process_task_pay(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
        
    try:
        pay = Decimal(message.text.strip().replace(',', '.'))
        if pay <= 0:
            raise ValueError
    except Exception:
        return await message.answer("❌ Ошибка: Введи корректное число больше нуля.")
        
    await state.update_data(worker_pay=pay)
    await state.set_state(TaskCreateStates.waiting_for_desc)
    
    await message.answer("📝 <b>Шаг 4/4:</b> Введи описание задания (оно будет отображаться юзерам):", parse_mode="HTML")

# waiting for data and create task
@admin_tasks_router.message(TaskCreateStates.waiting_for_desc)
async def process_task_desc(message: Message, state: FSMContext, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return
        
    description = message.text.strip()
    data = await state.get_data()
    
    try:
        result = await create_custom_admin_order(
            admin_tg_id=message.from_user.id,
            channel_url=data['channel_url'],
            subs_quantity=data['subs_quantity'],
            custom_worker_pay=data['worker_pay'],
            description=description,
            session=session
        )
        
        await message.answer(
            f"✅ <b>ЗАДАНИЕ СОЗДАНО!</b>\n\n"
            f"ID заказа: {result['order_id']}\n"
            f"{result['message']}", 
            parse_mode="HTML"
        )
    except Exception as e:
        safe_error = html.escape(str(e))
        await message.answer(f"❌ <b>Ошибка базы данных:</b>\n<code>{safe_error}</code>", parse_mode="HTML")
    finally:
        await state.clear()