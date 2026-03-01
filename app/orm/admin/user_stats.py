from sqlalchemy import select, func
from app.models import User, TaskCompletion
from app.models.task import CompletionStatus
from decimal import Decimal
from fastapi import HTTPException

async def get_users_list(session, limit: int = 50, offset: int = 0):
    # return users with pagination, new on top 
    query = select(User).order_by(User.id.desc()).limit(limit).offset(offset)
    result = await session.scalars(query)
    return result.all()

async def get_user_profile(identifier: str | int, session) -> dict:
    # check is that username or user id 
    if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
        user_query = select(User).where(User.id == int(identifier))
    else:
        # clear @ from username, and use ilike to avoid capital letters 
        clean_username = str(identifier).replace('@', '')
        user_query = select(User).where(User.username.ilike(clean_username))

    user = await session.scalar(user_query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found in database")
    # count frozen balance selected user
    frozen_query = select(func.coalesce(func.sum(TaskCompletion.stars_reward), Decimal('0'))).where(
        TaskCompletion.user_complete == user.id,
        TaskCompletion.status == CompletionStatus.FROZEN
    )
    frozen_balance = await session.scalar(frozen_query)

    return {
        "id": user.id,
        "username": user.username,
        "balance": user.balance,
        "stars_balance": user.stars_balance,
        "frozen_balance": frozen_balance,
        "strikes": user.strikes,
        "is_banned": user.is_banned
    }