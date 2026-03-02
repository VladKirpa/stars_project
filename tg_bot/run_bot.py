import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.config import settings
from tg_bot.middlewares.db import DbSessionMiddleware
from tg_bot.handlers.user import user_router
from tg_bot.middlewares.auth import AuthMiddleware
from tg_bot.handlers.admin import admin_router
from tg_bot.handlers.admin_tasks import admin_tasks_router
from tg_bot.handlers.admin_withdraw import admin_withdraw_router
from tg_bot.handlers.admin_orders import admin_orders_router

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.BOT_TOKEN) 
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware())
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())

    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(admin_tasks_router)
    dp.include_router(admin_withdraw_router)
    dp.include_router(admin_orders_router)

    print("🚀 Started...")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Stopped.")