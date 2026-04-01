from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from models.task import Status
from typing import Optional

class TaskBase(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    status: Status
    estimated_hours: Optional[Decimal] = None
    actual_hours: Optional[Decimal] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    project_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    estimated_hours: Optional[Decimal] = None
    actual_hours: Optional[Decimal] = None

class TaskRead(TaskBase):
    id:int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True