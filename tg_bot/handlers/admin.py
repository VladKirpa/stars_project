import html
from decimal import Decimal
from app.models import User
from sqlalchemy import select
from app.orm.admin.finances import manual_balance_update
from app.orm.admin.user_stats import get_user_profile
from app.orm.admin.user import ban_user, unban_user
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from tg_bot.utils.states import AdminStates

from app.config import settings
from app.orm.admin.fin_stats import get_global_financial_stats

admin_router = Router()

# check ids from .env
def is_admin(tg_id: int) -> bool:
    return tg_id in settings.ADMIN_IDS

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Финансовая статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🔍 Найти пользователя", callback_data="admin_find_user")]
    ])
    
    await message.answer("👑 <b>AdminPanel</b> 👑", reply_markup=kb, parse_mode="HTML")

@admin_router.callback_query(F.data == "admin_stats")
async def show_stats(call: CallbackQuery, session: AsyncSession):
    if not is_admin(call.from_user.id):
        return

    await call.answer("Загружаю данные...") 
    
    # Вызываем твою шикарную ORM-функцию
    stats = await get_global_financial_stats(session)
    
    text = (
        "📊 <b>Глобальная финансовая статистика:</b>\n\n"
        f"💰 На балансах юзеров: <b>{stats['total_user_balances']}</b>\n"
        f"❄️ В заморозке (холд): <b>{stats['total_frozen_funds']}</b>\n"
        f"📈 Прибыль системы: <b>{stats['total_system_revenue']}</b>\n"
        f"⚙️ Эмиссия админа (долг): <b>{stats['admin_emission_debt']}</b>\n"
        f"💸 Всего выведено: <b>{stats['total_withdrawn']}</b>"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@admin_router.callback_query(F.data == "admin_back")
async def back_to_menu(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
        
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Финансовая статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🔍 Найти пользователя", callback_data="admin_find_user")]
    ])
    
    await call.message.edit_text("👑 <b>AdminPanel</b> 👑", reply_markup=kb, parse_mode="HTML")

# find user button
@admin_router.callback_query(F.data == "admin_find_user")
async def ask_for_user(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
        
    await call.message.edit_text("✍️ <b>Введи ID пользователя или его @username:</b>", parse_mode="HTML")
    await state.set_state(AdminStates.waiting_for_user_id)

#waiting for admin text
@admin_router.message(AdminStates.waiting_for_user_id)
async def process_user_search(message: Message, state: FSMContext, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    identifier = message.text.strip()
    
    try:
        user_data = await get_user_profile(identifier, session)
        
        text = (
            f"👤 <b>Пользователь найден:</b>\n\n"
            f"ID: <code>{user_data['id']}</code>\n"
            f"Юзернейм: @{user_data['username'] or 'Нет'}\n"
            f"Обычный баланс: <b>{user_data['balance']} 💵</b>\n"
            f"Звездный баланс: <b>{user_data['stars_balance']} ⭐️</b>\n"
            f"В холде: {user_data['frozen_balance']} ❄️\n"
            f"Страйки: {user_data['strikes']} ⚠️\n"
            f"Статус: {'🔴 ЗАБАНЕН' if user_data['is_banned'] else '🟢 Активен'}"
        )

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Разбанить 🟢" if user_data['is_banned'] else "Забанить 🔴", 
                callback_data=f"admin_ban_{user_data['id']}"
            )],
            [InlineKeyboardButton(text="💰 Выдать баланс", callback_data=f"admin_topup_{user_data['id']}")],
            [InlineKeyboardButton(text="🔙 В меню", callback_data="admin_back")]
        ])

        await message.answer(text, reply_markup=kb, parse_mode="HTML")
        await state.clear() 

    except Exception as e:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
        ])
        await message.answer("❌ <b>Пользователь не найден в базе.</b>\nПроверь ID или вернись в меню.", reply_markup=kb, parse_mode="HTML")
        await state.clear()

#ban/unban user

@admin_router.callback_query(F.data.startswith("admin_ban_"))
async def toggle_user_ban(call: CallbackQuery, session: AsyncSession):
    if not is_admin(call.from_user.id):
        return
        
    user_id = int(call.data.split("_")[2])
    user = await session.scalar(select(User).where(User.id == user_id))
    if not user:
        return await call.answer("❌ Юзер не найден!", show_alert=True)
    
    try:
        if user.is_banned:
            result = await unban_user(user_id=user_id, session=session)
            await call.answer("🟢 " + result["message"], show_alert=True)
            
            await call.message.edit_text(
                f"👤 <b>Пользователь {user_id}</b>\n\n🟢 <b>РАЗБАНЕН</b>\n<i>Страйки обнулены. Баланс остался нулевым.</i>", 
                parse_mode="HTML"
            )
            
        else:
            result = await ban_user(user_id=user_id, session=session)
            await call.answer("🔴 " + result["message"], show_alert=True)
            
            await call.message.edit_text(
                f"👤 <b>Пользователь {user_id}</b>\n\n🔴 <b>ЗАБАНЕН</b>\n<i>Средства конфискованы, активные таски отменены.</i>", 
                parse_mode="HTML"
            )
            
    except Exception as e:
        safe_error = html.escape(str(e))
        await call.message.answer(f"❌ <b>Ошибка:</b>\n<code>{safe_error}</code>", parse_mode="HTML")


# top up balance

@admin_router.callback_query(F.data.startswith("admin_topup_"))
async def choose_balance_type(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
        
    user_id = int(call.data.split("_")[2])
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐️ Звездный баланс", callback_data=f"admin_baltype_stars_{user_id}")],
        [InlineKeyboardButton(text="💵 Обычный баланс", callback_data=f"admin_baltype_regular_{user_id}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_back")]
    ])
    
    await call.message.edit_text("⚖️ <b>Выбери балик?</b>", reply_markup=kb, parse_mode="HTML")

@admin_router.callback_query(F.data.startswith("admin_baltype_"))
async def ask_topup_amount(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
        
    parts = call.data.split("_")
    bal_type = parts[2]
    user_id = int(parts[3])
    
    is_stars = (bal_type == "stars")
    bal_name = "⭐️ Звездный" if is_stars else "💵 Обычный"
    
    await state.update_data(target_user_id=user_id, is_stars=is_stars)
    await state.set_state(AdminStates.waiting_for_topup_amount)
    
    await call.message.edit_text(
        f"Выбран <b>{bal_name}</b> баланс.\n\n"
        f"💰 <b>Введи сумму пополнения:</b>\n"
        f"<i>(Только положительное число)</i>", 
        parse_mode="HTML"
    )

@admin_router.message(AdminStates.waiting_for_topup_amount)
async def process_topup_amount(message: Message, state: FSMContext, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    user_id = data.get("target_user_id")
    is_stars = data.get("is_stars")

    try:
        raw_text = message.text.strip().replace(',', '.')
        amount = Decimal(raw_text)
        
        if amount <= 0:
            await message.answer("❌ <b>Ошибка:</b> Сумма должна быть больше нуля.", parse_mode="HTML")
            return
            
    except Exception:
        await message.answer("❌ <b>Ошибка:</b> Введи корректное число (например, 100 или 50.5).", parse_mode="HTML")
        return

    try:
        result = await manual_balance_update(
            identifier=user_id, 
            amount=amount, 
            is_stars_balance=is_stars, 
            session=session
        )
        
        bal_name = "⭐️ Звездного" if is_stars else "💵 Обычного"
        await message.answer(
            f"✅ <b>Успешно!</b>\n"
            f"Баланс: {bal_name}\n"
            f"{result['message']}\n"
            f"Новое значение: <b>{result['new_balance']}</b>", 
            parse_mode="HTML"
        )
        
    except Exception as e:
        safe_error_msg = html.escape(str(e))
        await message.answer(f"❌ <b>Ошибка при выдаче:</b>\n<code>{safe_error_msg}</code>", parse_mode="HTML")
    
    finally:
        await state.clear()


