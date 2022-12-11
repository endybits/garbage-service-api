from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import SQLALCHEMY_DB_URI

engine = create_engine(SQLALCHEMY_DB_URI)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)