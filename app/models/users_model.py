import uuid
from datetime import datetime

from db.database import Base
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

class Users(Base):
    __tablename__ = "registered_users"

    id : Mapped[str] = mapped_column(
        String(50), primary_key=True, default=lambda: str(uuid.uuid4)
    )

    username : Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )

    email_id : Mapped[str] = mapped_column(
        String(200), nullable=False, unique=True
    )

    password : Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    created_at : Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )