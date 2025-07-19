from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pedido import models, schemas
from database import get_db

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=schemas.PedidoOut)
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    valor_total = pedido.quantidade * pedido.preco_unitario
    novo_pedido = models.Pedido(
        cliente_id=pedido.cliente_id,
        produto_id=pedido.produto_id,
        quantidade=pedido.quantidade,
        preco_unitario=pedido.preco_unitario,
        valor_total=valor_total
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido

@router.get("/", response_model=list[schemas.PedidoOut])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(models.Pedido).all()

@router.get("/{pedido_id}", response_model=schemas.PedidoOut)
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedido).get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.put("/{pedido_id}", response_model=schemas.PedidoOut)
def atualizar_pedido(pedido_id: int, dados: schemas.PedidoUpdate, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedido).get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    for key, value in dados.dict().items():
        setattr(pedido, key, value)
    pedido.valor_total = pedido.quantidade * pedido.preco_unitario
    db.commit()
    db.refresh(pedido)
    return pedido

@router.delete("/{pedido_id}")
def deletar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedido).get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(pedido)
    db.commit()
    return {"detail": "Pedido excluído com sucesso"}
