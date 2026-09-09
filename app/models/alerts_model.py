from db.database import Base
from sqlalchemy import String, Integer, DateTime,ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from datetime import datetime

class Alerts(Base):
    __tablename__ = 'alert_logs'

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )

    api_id: Mapped[str] = mapped_column(
        String(50), 
        ForeignKey("registered_apis.id"), 
        nullable=False, index=True
    )

    type: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )

    message: Mapped[str | None] = mapped_column(
        Text, 
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow
    )

    resolved: Mapped[bool] = mapped_column(
        Boolean, 
        default=False,
        nullable=False
    )

    resolved_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=True
    )

    apis = Relationship(
        "API",
        back_populates="alert",
        cascade="all, delete-orphan"
    )