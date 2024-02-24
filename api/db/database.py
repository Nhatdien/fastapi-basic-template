from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Replace the database URL with the correct one
SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(
    "postgresql://postgres:Nhatdien123@localhost:5432/url-shortener"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()