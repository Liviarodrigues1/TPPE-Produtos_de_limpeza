from fastapi import FastAPI
from produto.routes import router as produto_router
from cliente.routes import router as cliente_router
from carrinho.routes import router as carrinho_router
from pedido.routes import router as pedido_router
from pagamento.routes import router as pagamento_router
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(produto_router)
app.include_router(cliente_router)
app.include_router(carrinho_router)
app.include_router(pedido_router)
app.include_router(pagamento_router)

@app.get("/")
def root():
    return {"message": "API: Loja de Produtos Online"}