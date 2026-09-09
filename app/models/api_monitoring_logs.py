from datetime import datetime

from db.database import Base
from sqlalchemy import String, BigInteger, Integer, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, Relationship

class MonitoredLogs(Base):
    __tablename__ = "monitored_logs"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )

    api_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("registered_apis.id"), nullable=False, index=True
    )

    checked_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True
    )

    status_code: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    latency_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    is_success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    error_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    response_size: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    apis = Relationship(
        "API",
        back_populates="logs",
        cascade="all, delete-orphan"
    )