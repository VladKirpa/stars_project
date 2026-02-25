import datetime
import enum
from sqlalchemy import (
    DECIMAL, func, String, Enum as SQLEnum, BIGINT, ForeignKey
    )
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal # Decimal for Mapped
from app.database import bigint_pk

class PaymentStatus(enum.Enum):
    CREATED='created'
    PAID='paid'
    EXPIRED='expired'


class PendingPayment(Base):
    __tablename__='pending_payments'
    
    id: Mapped[bigint_pk]
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'))
    external_id: Mapped[str] = mapped_column(String, index=True ,unique=True)
    provider: Mapped[str] = mapped_column(String)
    amount_stars: Mapped[Decimal] = mapped_column(DECIMAL(12,2))
    amount_fiat: Mapped[Decimal] = mapped_column(DECIMAL(12,2))
    currency: Mapped[str] = mapped_column(String, default='USDT')
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus))
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        server_default=func.now(), nullable=False)
    

