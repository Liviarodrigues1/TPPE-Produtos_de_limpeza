from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class PedidoBase(BaseModel):
    cliente_id: int
    produto_id: int
    quantidade: int = 1
    preco_unitario: Decimal

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(PedidoBase):
    pass

class PedidoOut(PedidoBase):
    id: int
    data_pedido: datetime
    valor_total: Decimal

    class Config:
        orm_mode = True
