import datetime
from sqlalchemy import (
    DECIMAL, BIGINT, ForeignKey, VARCHAR, TIMESTAMP, func
    )
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal # Decimal for Mapped
from app.database import bigint_pk



class Order(Base):
    __tablename__ = 'orders'

    #Relationship
    tasks: Mapped[list['Task']] = relationship(back_populates='order')
    creator: Mapped["User"] = relationship(back_populates="orders")
    
    id: Mapped[bigint_pk] # Generated always as identity
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    channel_id: Mapped[str] = mapped_column(VARCHAR(255))
    subs_quantity: Mapped[int] = mapped_column(BIGINT)
    reward_for_sub: Mapped[Decimal] = mapped_column(DECIMAL)
    worker_pay: Mapped[Decimal] = mapped_column(DECIMAL)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), nullable=False)
    status: Mapped[str] = mapped_column(VARCHAR(50), default='pending')
    action_type: Mapped[str] = mapped_column(VARCHAR(30))
    description: Mapped[str] = mapped_column(VARCHAR(250), nullable=True)
    
    @property
    def total_completions(self) -> int:
        count = 0
        for task in self.tasks:
            count+=len(task.completions)
        
        return count
    
    
    


