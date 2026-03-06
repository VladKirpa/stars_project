import datetime
import enum
from sqlalchemy import (
    DECIMAL, func, String, Enum as SQLEnum, BIGINT, ForeignKey
    )
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal # Decimal for Mapped
from app.database import bigint_pk

class WithdrawalStatus(enum.Enum):
    PENDING='pending'
    APPROVED='approved'
    REJECTED='rejected'


class WithdrawalRequest(Base):
    __tablename__='withdrawal_requests'

    id: Mapped[bigint_pk]
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'))
    amount: Mapped[int] = mapped_column(BIGINT)
    username: Mapped[str] = mapped_column(String)
    status: Mapped[WithdrawalStatus] = mapped_column(SQLEnum(WithdrawalStatus))
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        server_default=func.now())


