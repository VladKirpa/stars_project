from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate
from app.orm.users_orm import add_user
from tg_bot.locales.texts import get_text
from tg_bot.keyboards.inline import get_webapp_keyboard

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, session):
    lang = message.from_user.language_code # catch lang setting 

    # looking for referral link in start message
    ref_id = None
    if command.args and command.args.isdigit():
        ref_id = int(command.args)

    user_data = UserCreate(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        referral_id=ref_id
    )

    user = await add_user(user_data, session)

    text = get_text(lang, 'welcome').format(name=message.from_user.first_name)
    kb = get_webapp_keyboard(lang)

    await message.answer(text, reply_markup=kb)