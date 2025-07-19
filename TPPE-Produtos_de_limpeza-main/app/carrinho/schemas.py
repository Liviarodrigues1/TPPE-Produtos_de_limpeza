from pydantic import BaseModel

class CarrinhoBase(BaseModel):
    cliente_id: int
    produto_id: int
    quantidade: int = 1

class CarrinhoCreate(CarrinhoBase):
    pass

class CarrinhoUpdate(CarrinhoBase):
    pass

class CarrinhoOut(CarrinhoBase):
    id: int

    class Config:
        orm_mode = True
