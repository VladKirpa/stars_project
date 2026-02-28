import asyncio
from datetime import datetime, timedelta, timezone
from celery import Celery
from sqlalchemy import select
from app.config import settings
from app.database import async_session_factory
from app.models import User, TaskCompletion, TransactionLog
from app.models.task import CompletionStatus
from app.models.transaction_log import WalletType, ActionType

celery_app = Celery(
    "stars_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.beat_schedule = {
    'unlock-frozen-funds-every-hour': {
        'task': 'app.celery_app.unlock_funds_task',
        'schedule': 600.0,
    },
}
celery_app.conf.timezone = 'UTC'    

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

async def async_unlock_frozen_funds():
    async with async_session_factory() as session:
        try:
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            
            # check unlock date
            query = select(TaskCompletion).where(
                TaskCompletion.status == CompletionStatus.FROZEN,
                TaskCompletion.unlock_date <= now
            ).with_for_update()
            
            result = await session.scalars(query)
            frozen_tasks = result.all()

            if not frozen_tasks:
                return "No funds to unlock yet"

            unlocked_count = 0
            for task in frozen_tasks:
                task.status = CompletionStatus.COMPLETED
                
                # find user
                user = await session.get(User, task.user_complete, with_for_update=True)
                if user:
                    user.balance += task.stars_reward
                    
                    # save bill
                    session.add(TransactionLog(
                        user_id=user.id,
                        amount=task.stars_reward,
                        wallet_type=WalletType.EARNED,
                        action_type=ActionType.TASK_PAYMENT,
                        order_id=task.task_id 
                    ))
                    unlocked_count += 1

            await session.commit()
            print(f"DEBUG: Unlocked {unlocked_count} tasks")
            return f"Unlocked funds for {unlocked_count} tasks."

        except Exception as e:
            await session.rollback()
            print(f"CELERY CRITICAL ERROR: {str(e)}")
            return f"Error: {e}"

@celery_app.task
def unlock_funds_task():
    # user our celery helper to run
    return run_async(async_unlock_frozen_funds())