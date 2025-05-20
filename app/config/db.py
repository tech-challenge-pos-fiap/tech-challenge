from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

DATABASE_URL = f'postgresql://{os.environ.get("POSTGRES_USER", "tech-challenge")}:{os.environ.get("POSTGRES_PASSWORD", "tech-challenge")}@{os.environ.get("POSTGRES_HOST", "postgres")}:{os.environ.get("POSTGRES_PORT", "5432")}/{os.environ.get("POSTGRES_DATABASE", "tech-challenge")}'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
