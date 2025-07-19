from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from produto import models, schemas
from database import get_db

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", response_model=schemas.ProdutoOut)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = models.Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.get("/", response_model=list[schemas.ProdutoOut])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.Produto).all()

@router.get("/{produto_id}", response_model=schemas.ProdutoOut)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.put("/{produto_id}", response_model=schemas.ProdutoOut)
def atualizar_produto(produto_id: int, dados: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in dados.dict().items():
        setattr(produto, key, value)
    db.commit()
    db.refresh(produto)
    return produto

@router.delete("/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return {"detail": "Produto excluído com sucesso"}
