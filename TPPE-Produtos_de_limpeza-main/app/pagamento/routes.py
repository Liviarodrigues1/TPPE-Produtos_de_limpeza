from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pagamento import models, schemas
from database import get_db

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

@router.post("/", response_model=schemas.PagamentoOut)
def criar_pagamento(pagamento: schemas.PagamentoCreate, db: Session = Depends(get_db)):
    novo_pagamento = models.Pagamento(**pagamento.dict())
    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)
    return novo_pagamento

@router.get("/", response_model=list[schemas.PagamentoOut])
def listar_pagamentos(db: Session = Depends(get_db)):
    return db.query(models.Pagamento).all()

@router.get("/{pagamento_id}", response_model=schemas.PagamentoOut)
def buscar_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(models.Pagamento).get(pagamento_id)
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return pagamento

@router.delete("/{pagamento_id}")
def deletar_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(models.Pagamento).get(pagamento_id)
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    db.delete(pagamento)
    db.commit()
    return {"detail": "Pagamento excluído com sucesso"}
