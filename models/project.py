from typing import TYPE_CHECKING
from database import Base
from enum import Enum
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Text, Enum as SQLEnum, Numeric, ForeignKey, DateTime, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.task import Task
    from models.invoice import Invoice

class Status(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Project(Base):

    __tablename__ = "projects"

    __table_args__ = (
        CheckConstraint(
            "(hourly_rate IS NOT NULL AND fixed_price IS NULL) OR"
            "(hourly_rate IS NULL AND fixed_price IS NOT NULL)",
            name="check_price_type"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    state: Mapped[Status] = mapped_column(SQLEnum(Status, name="state_enum"),
                                            default=Status.PLANNED,
                                            server_default=Status.PLANNED.value,
                                            nullable=False,
                                            index=True
                                          )
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    hourly_rate: Mapped[Decimal | None] = mapped_column(Numeric (10, 2), nullable=True)
    fixed_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
        )
    
    # A project belongs to one client
    client = relationship("Client", back_populates="projects")
    tasks: Mapped["Task"] = relationship(
        'Task', 
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True
        )
    
    