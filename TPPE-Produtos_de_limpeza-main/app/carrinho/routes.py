from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from carrinho import models, schemas
from database import get_db

router = APIRouter(prefix="/carrinhos", tags=["Carrinhos"])

@router.post("/", response_model=schemas.CarrinhoOut)
def criar_carrinho(carrinho: schemas.CarrinhoCreate, db: Session = Depends(get_db)):
    existente = db.query(models.Carrinho).filter_by(cliente_id=carrinho.cliente_id).first()
    if existente:
        raise HTTPException(status_code=400, detail="Este cliente já possui um carrinho.")
    novo = models.Carrinho(**carrinho.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/", response_model=list[schemas.CarrinhoOut])
def listar_carrinhos(db: Session = Depends(get_db)):
    return db.query(models.Carrinho).all()

@router.get("/{carrinho_id}", response_model=schemas.CarrinhoOut)
def buscar_carrinho(carrinho_id: int, db: Session = Depends(get_db)):
    carrinho = db.query(models.Carrinho).get(carrinho_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    return carrinho

@router.put("/{carrinho_id}", response_model=schemas.CarrinhoOut)
def atualizar_carrinho(carrinho_id: int, dados: schemas.CarrinhoUpdate, db: Session = Depends(get_db)):
    carrinho = db.query(models.Carrinho).get(carrinho_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    for key, value in dados.dict().items():
        setattr(carrinho, key, value)
    db.commit()
    db.refresh(carrinho)
    return carrinho

@router.delete("/{carrinho_id}")
def deletar_carrinho(carrinho_id: int, db: Session = Depends(get_db)):
    carrinho = db.query(models.Carrinho).get(carrinho_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    db.delete(carrinho)
    db.commit()
    return {"detail": "Carrinho excluído com sucesso"}
