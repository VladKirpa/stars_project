from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class UserBase(BaseModel):
    tg_id: int
    username: str | None = None


class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    tg_id: int
    username: str | None = None
    referral_id: int | None = None
    balance: Decimal
    stars_balance: Decimal

    
    model_config = ConfigDict(from_attributes=True)

