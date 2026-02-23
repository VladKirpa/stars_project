from pydantic import BaseModel, ConfigDict
from app.models import Task, TaskCompletion


class TaskBase(BaseModel):

    #id order_id name desc

    order_id: int 
    name: str
    description: str | None=None



class TaskRead(TaskBase):
    id: int


    model_config = ConfigDict(from_attributes=True)