from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = (f'mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}')

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping = True
)

SessionLocal = sessionmaker(
    autoflush = False,
    autocommit = False,
    bind = engine
)

class Base(DeclarativeBase):
    pass