from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional
from models.invoice import Status

class InvoiceBase(BaseModel):
    client_id: int
    project_id: Optional[int] = None
    issue_date: datetime
    total_amount: Decimal
    status: Status = Status.DRAFT
    due_date: datetime

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    client_id: Optional[int] = None
    project_id: Optional[int] = None
    issue_date: Optional[datetime] = None
    total_amount: Optional[Decimal] = None
    status: Optional[Status] = None
    due_date: Optional[datetime] = None
    paid_at: Optional[datetime] = None

class InvoiceRead(InvoiceBase):
    id: int
    paid_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True