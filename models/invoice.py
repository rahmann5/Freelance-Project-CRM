from typing import TYPE_CHECKING
from enum import Enum
from decimal import Decimal
from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, func,Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

if TYPE_CHECKING:
    from models.project import Project
    from models.client import Client

class Status(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"

class Invoice(Base):

    __tablename__ = "invoices"

    __table_args__= (
        CheckConstraint("due_date >= issue_date", name = "invoice_due_after_issue_date"),

        CheckConstraint("(status != 'paid') OR (paid_at IS NOT NULL)", name="invoice_paid_requires_paid_at_date")
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'), nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), nullable=True)
    issue_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[Status] = mapped_column(SQLEnum(Status, name="invoice_status"),
                                           default=Status.DRAFT,
                                           nullable=False
                                           )
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    client: Mapped["Client"] = relationship("Client", back_populates="invoices")
    

