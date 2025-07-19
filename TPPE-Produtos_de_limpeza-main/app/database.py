from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

DATABASE_URL = "postgresql://produto_de_limpeza_user:tYAvKKBuU0RfmJbs4azvWuv1GtXrU4Uc@dpg-d1tp9qjipnbc73cjffc0-a.oregon-postgres.render.com:5432/produto_de_limpeza"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
