from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from app.config import settings
from tg_bot.locales.texts import get_text

def get_webapp_keyboard(lang_code: str) -> InlineKeyboardMarkup:
    btn_text = get_text(lang_code, 'btn_app')
    
    # frontend link here
    web_app_url = getattr(settings, "WEBAPP_URL", "https://google.com")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn_text, web_app=WebAppInfo(url=web_app_url))]
    ])
    return keyboard