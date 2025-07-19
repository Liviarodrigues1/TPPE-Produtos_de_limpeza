from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from enum import Enum

class MetodoPagamentoEnum(str, Enum):
    cartao_credito = "cartao_credito"
    boleto = "boleto"
    pix = "pix"

class PagamentoBase(BaseModel):
    pedido_id: int
    metodo: MetodoPagamentoEnum
    valor: Decimal

class PagamentoCreate(PagamentoBase):
    pass

class PagamentoOut(PagamentoBase):
    id: int
    data_pagamento: datetime

    class Config:
        orm_mode = True
