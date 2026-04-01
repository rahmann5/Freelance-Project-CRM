from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from schemas.project_schema import ProjectRead

class ClientBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    company_name: Optional[str] = None
    is_active: bool = True

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    is_active: Optional[bool] = None

class ClientRead(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ClientWithInvoiceTotal(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    total_invoice_amount: Decimal = 0

    class Config:
        from_attributes = True

class ClientWithUnpaidInvoiceTotal(ClientBase):
    id: int
    total_unpaid_invoice_amount: Decimal = 0

    class Config:
        from_attributes = True

class ClientWithProjects(ClientRead):
    projects: List[ProjectRead] = Field(default_factory=list)

    class Config:
        from_attributes = True
