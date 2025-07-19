from sqlalchemy import Column, Integer, String, DECIMAL
from database import Base

class Produto(Base):
    __tablename__ = "Produto"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(DECIMAL(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False)