from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Numeric, func
from database import Base
import enum

class MetodoPagamentoEnum(str, enum.Enum):
    cartao_credito = "cartao_credito"
    boleto = "boleto"
    pix = "pix"

class Pagamento(Base):
    __tablename__ = "Pagamento"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("Pedido.id"), nullable=False)
    data_pagamento = Column(DateTime, server_default=func.now())
    metodo = Column(Enum(MetodoPagamentoEnum), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
