from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, func
from database import Base

class Pedido(Base):
    __tablename__ = "Pedido"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("Cliente.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("Produto.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    data_pedido = Column(DateTime, server_default=func.now())
    valor_total = Column(Numeric(10, 2), nullable=False)
