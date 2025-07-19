from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cliente import models, schemas
from database import get_db

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=schemas.ClienteOut)
def criar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    if db.query(models.Cliente).filter_by(email=cliente.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/", response_model=list[schemas.ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(models.Cliente).all()

@router.get("/{cliente_id}", response_model=schemas.ClienteOut)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.put("/{cliente_id}", response_model=schemas.ClienteOut)
def atualizar_cliente(cliente_id: int, dados: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for key, value in dados.dict().items():
        setattr(cliente, key, value)
    db.commit()
    db.refresh(cliente)
    return cliente

@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente)
    db.commit()
    return {"detail": "Cliente excluído com sucesso"}
