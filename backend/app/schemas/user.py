from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class UserBase(BaseModel):
    tg_id: int
    username: str | None = None

class UserCreate(UserBase):
    referral_id: int | None = None

class UserRead(UserBase):
    id: int
    referral_id: int | None = None
    balance: Decimal
    stars_balance: Decimal
    strikes: int
    is_banned: bool
    frozen_balance: Decimal = Decimal('0.0')
    completed_tasks_count: int = 0
    referrals_count: int = 0
    referral_earned: int = 0

    model_config = ConfigDict(from_attributes=True)