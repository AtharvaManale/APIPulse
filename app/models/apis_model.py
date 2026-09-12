import uuid
from datetime import datetime

from app.db.database import Base
from sqlalchemy import String, Integer, DateTime, Boolean, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from app.models.users_model import Users  # noqa: F401
from app.models.monitored_logs_model import MonitoredLogs  # noqa: F401
from app.models.alerts_model import Alerts  # noqa: F401

class API(Base):

    __tablename__ = "registered_apis"

    __table_args__ = (
        UniqueConstraint(
            "url",
            "url_method",
            name = "unique_url_url_method" 
        ),
    )

    id: Mapped[str] = mapped_column(
        String(50), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )

    user_id: Mapped[str] = mapped_column(
        String(50), 
        ForeignKey("registered_users.id"), 
        index=True, 
        nullable=False
    )

    api_name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        String(500), 
        nullable=False
    )

    url_method: Mapped[str] = mapped_column(
        String(15), 
        nullable=False
    )

    url_headers: Mapped[dict | None] = mapped_column(
        JSON, 
        nullable=True
    )

    time_interval: Mapped[int] = mapped_column(
        Integer, 
        default=60, 
        nullable=False
    )

    timeout: Mapped[int] = mapped_column(
        Integer, 
        default=10, 
        nullable=False
    )

    expected_status_code: Mapped[int] = mapped_column(
        Integer,
        default=200,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=False,
        nullable=False
    )

    created_at : Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow
    )

    user = Relationship(
        "Users",
        back_populates="apis",
    )

    logs = Relationship(
        "MonitoredLogs",
        back_populates="api",
        cascade="all, delete-orphan"
    )

    alerts = Relationship(
        "Alerts",
        back_populates="api",
        cascade="all, delete-orphan"
    )