import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

cliente_exemplo = {
    "nome": "Maria da Silva",
    "email": "maria@email.com",
    "telefone": "11999999999"
}

@pytest.fixture(name="cliente_fixture")
def novo_cliente():
    response = client.post("/clientes", json=cliente_exemplo)
    assert response.status_code == 200
    cliente = response.json()
    yield cliente
    client.delete(f"/clientes/{cliente['id']}")

def test_adicionar_cliente():
    response = client.post("/clientes", json=cliente_exemplo)
    assert response.status_code == 200
    cliente = response.json()
    assert cliente["nome"] == cliente_exemplo["nome"]
    assert cliente["email"] == cliente_exemplo["email"]
    assert cliente["telefone"] == cliente_exemplo["telefone"]
    assert "id" in cliente
    client.delete(f"/clientes/{cliente['id']}")

def test_listar_clientes(cliente_fixture):
    response = client.get("/clientes")
    assert response.status_code == 200
    assert any(cliente["id"] == cliente_fixture["id"] for cliente in response.json())

def test_buscar_cliente(cliente_fixture):
    response = client.get(f"/clientes/{cliente_fixture['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == cliente_fixture["id"]

def test_atualizar_cliente(cliente_fixture):
    novo_dado = {
        "nome": cliente_fixture["nome"],
        "email": cliente_fixture["email"],
        "telefone": "11888888888"
    }
    response = client.put(f"/clientes/{cliente_fixture['id']}", json=novo_dado)
    assert response.status_code == 200
    assert response.json()["telefone"] == novo_dado["telefone"]

def test_remover_cliente():
    response = client.post("/clientes", json=cliente_exemplo)
    assert response.status_code == 200
    cliente = response.json()
    response = client.delete(f"/clientes/{cliente['id']}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Cliente excluído com sucesso"
