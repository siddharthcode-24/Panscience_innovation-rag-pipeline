from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.document import Base
from app.config import settings
import os

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()