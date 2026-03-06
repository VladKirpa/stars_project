from pydantic import BaseModel, ConfigDict
from app.models import Task, TaskCompletion
from app.schemas.order import OrderShortRead


class TaskBase(BaseModel):

    #id order_id name desc

    order_id: int 
    

class TaskRead(TaskBase):
    id: int
    order: OrderShortRead
    
    model_config = ConfigDict(from_attributes=True)


