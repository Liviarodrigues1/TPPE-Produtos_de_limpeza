from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class Carrinho(Base):
    __tablename__ = "Carrinho"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("Cliente.id"), unique=True, nullable=False)
    produto_id = Column(Integer, ForeignKey("Produto.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
