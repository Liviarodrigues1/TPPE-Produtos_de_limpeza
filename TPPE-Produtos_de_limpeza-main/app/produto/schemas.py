from pydantic import BaseModel
from decimal import Decimal

class ProdutoBase(BaseModel):
    nome: str
    preco: Decimal
    estoque: int

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: int

    class Config:
        orm_mode = True
