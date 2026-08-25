import uuid
from datetime import datetime, time

from db.database import Base
from sqlalchemy import String, Integer, DateTime, Boolean, JSON, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class API(Base):
    __tablename__ = "registered_apis"

    id: Mapped[str] = mapped_column(
        String(50), primary_key=True, default=lambda: str(uuid.uuid4)
    )

    user_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("registered_users.id"), index=True, nullable=False
    )

    api_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    url: Mapped[str] = mapped_column(
        String(2048), nullable=False
    )

    url_method: Mapped[str] = mapped_column(
        String(15), nullable=False
    )

    url_headers: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )

    time_interval: Mapped[int] = mapped_column(
        Integer, default=60, nullable=False
    )

    timeout: Mapped[int] = mapped_column(
        Integer, default=10, nullable=False
    )

    expected_status_code: Mapped[int] = mapped_column(
        Integer,
        default=200,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )