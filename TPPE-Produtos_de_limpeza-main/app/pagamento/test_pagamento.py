import pytest
from fastapi.testclient import TestClient
from main import app
import random

client = TestClient(app)

def criar_cliente():
    cliente = {
        "nome": f"Cliente {random.randint(1000,9999)}",
        "email": f"teste{random.randint(1000,9999)}@email.com",
        "telefone": "11999999999"
    }
    resp = client.post("/clientes", json=cliente)
    assert resp.status_code == 200
    return resp.json()

def criar_produto():
    produto = {
        "nome": f"Produto {random.randint(1000,9999)}",
        "preco": 100.0,
        "estoque": 10
    }
    resp = client.post("/produtos", json=produto)
    assert resp.status_code == 200
    return resp.json()

def criar_pedido(cliente_id, produto_id):
    pedido = {
        "cliente_id": cliente_id,
        "produto_id": produto_id,
        "quantidade": 2,
        "preco_unitario": 100.0
    }
    resp = client.post("/pedidos", json=pedido)
    assert resp.status_code == 200
    return resp.json()

@pytest.fixture
def dados_pagamento():
    cliente = criar_cliente()
    produto = criar_produto()
    pedido = criar_pedido(cliente["id"], produto["id"])

    pagamento = {
        "pedido_id": pedido["id"],
        "metodo": "pix",  # Precisa bater com o Enum: "pix", "boleto", "cartao_credito"
        "valor": pedido["valor_total"]
    }

    yield pagamento, cliente["id"], produto["id"], pedido["id"]

    # Cleanup final (caso algo falhe no meio)
    client.delete(f"/pedidos/{pedido['id']}")
    client.delete(f"/clientes/{cliente['id']}")
    client.delete(f"/produtos/{produto['id']}")

def test_criar_pagamento(dados_pagamento):
    pagamento, cliente_id, produto_id, pedido_id = dados_pagamento
    resp = client.post("/pagamentos", json=pagamento)
    assert resp.status_code == 200
    data = resp.json()
    assert data["pedido_id"] == pagamento["pedido_id"]
    assert float(data["valor"]) == float(pagamento["valor"])
    assert data["metodo"] == pagamento["metodo"]

    # Cleanup
    client.delete(f"/pagamentos/{data['id']}")
    client.delete(f"/pedidos/{pedido_id}")
    client.delete(f"/clientes/{cliente_id}")
    client.delete(f"/produtos/{produto_id}")

def test_listar_pagamentos(dados_pagamento):
    pagamento, cliente_id, produto_id, pedido_id = dados_pagamento
    resp = client.post("/pagamentos", json=pagamento)
    assert resp.status_code == 200
    pag_id = resp.json()["id"]

    lista = client.get("/pagamentos")
    assert lista.status_code == 200
    assert any(p["id"] == pag_id for p in lista.json())

    # Cleanup
    client.delete(f"/pagamentos/{pag_id}")
    client.delete(f"/pedidos/{pedido_id}")
    client.delete(f"/clientes/{cliente_id}")
    client.delete(f"/produtos/{produto_id}")

def test_buscar_pagamento(dados_pagamento):
    pagamento, cliente_id, produto_id, pedido_id = dados_pagamento
    resp = client.post("/pagamentos", json=pagamento)
    assert resp.status_code == 200
    pag_id = resp.json()["id"]

    busca = client.get(f"/pagamentos/{pag_id}")
    assert busca.status_code == 200
    assert busca.json()["id"] == pag_id

    # Cleanup
    client.delete(f"/pagamentos/{pag_id}")
    client.delete(f"/pedidos/{pedido_id}")
    client.delete(f"/clientes/{cliente_id}")
    client.delete(f"/produtos/{produto_id}")

def test_remover_pagamento(dados_pagamento):
    pagamento, cliente_id, produto_id, pedido_id = dados_pagamento
    resp = client.post("/pagamentos", json=pagamento)
    assert resp.status_code == 200
    pag_id = resp.json()["id"]

    delete = client.delete(f"/pagamentos/{pag_id}")
    assert delete.status_code == 200

    busca = client.get(f"/pagamentos/{pag_id}")
    assert busca.status_code == 404

    # Cleanup
    client.delete(f"/pedidos/{pedido_id}")
    client.delete(f"/clientes/{cliente_id}")
    client.delete(f"/produtos/{produto_id}")
