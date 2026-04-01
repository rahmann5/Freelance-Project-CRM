from typing import TYPE_CHECKING
from decimal import Decimal
from enum import Enum
from datetime import datetime
from sqlalchemy import String, Text, Enum as SQLEnum, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

if TYPE_CHECKING:
    from models.project import Project

class Status(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id', ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[Status] = mapped_column(SQLEnum(Status, name="status_name"), 
                                           default=Status.TODO,
                                           nullable=False
                                           )
    estimated_hours: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    actual_hours: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    project: Mapped["Project"]= relationship('Project', back_populates="tasks")

    


