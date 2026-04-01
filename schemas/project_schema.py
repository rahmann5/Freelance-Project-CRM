from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional
from models.project import Status

class ProjectBase(BaseModel):
    client_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    state: Optional[Status] = Status.PLANNED
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    hourly_rate: Optional[Decimal] = None
    fixed_price: Optional[Decimal] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    client_id: Optional[int] = None

class ClientSimple(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
    
class ProjectRead(ProjectBase):
    id: int
    client: Optional[ClientSimple]   
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        

