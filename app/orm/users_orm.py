from app.models import User
from sqlalchemy import select
from app.schemas.user import UserCreate

async def add_user(user_in: UserCreate, session) -> User:

    user = await session.scalar(select(User).where(User.tg_id == user_in.tg_id))
    
    if user:
        # refresh user if user exists
        if user_in.username and user.username != user_in.username:
            user.username = user_in.username
            await session.commit()
        return user
        
    
    ref_id = user_in.referral_id
    
    if ref_id == user_in.tg_id:
        ref_id = None
        
    # Check if this ref exists
    if ref_id:
        referrer = await session.scalar(select(User).where(User.tg_id == ref_id))
        if not referrer:
            ref_id = None

    new_user = User(
        tg_id=user_in.tg_id,
        username=user_in.username,
        referral_id=ref_id
    )
    session.add(new_user)
    await session.commit() 
    await session.refresh(new_user) 
    return new_user


async def get_user_referrals(tg_id: int, session) -> list[User]:  # return ref stats
    query = select(User).where(User.referral_id == tg_id)
    result = await session.scalars(query)
    return list(result.all())

