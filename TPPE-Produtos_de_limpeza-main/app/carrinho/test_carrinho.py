import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

cliente_exemplo = {
    "nome": "João da Silva",
    "email": "joao@email.com",
    "telefone": "11988888888"
}

produto_exemplo = {
    "nome": "Mouse Gamer",
    "preco": 149.90,
    "estoque": 30
}

@pytest.fixture(name="cliente_produto_fixture")
def setup_cliente_produto():
    # Criar cliente
    cliente_resp = client.post("/clientes", json=cliente_exemplo)
    assert cliente_resp.status_code == 200
    cliente_id = cliente_resp.json()["id"]

    # Criar produto
    produto_resp = client.post("/produtos", json=produto_exemplo)
    assert produto_resp.status_code == 200
    produto_id = produto_resp.json()["id"]

    yield {"cliente_id": cliente_id, "produto_id": produto_id}

    # Cleanup
    client.delete(f"/carrinhos/{cliente_id}")
    client.delete(f"/clientes/{cliente_id}")
    client.delete(f"/produtos/{produto_id}")

def test_criar_carrinho(cliente_produto_fixture):
    data = {
        "cliente_id": cliente_produto_fixture["cliente_id"],
        "produto_id": cliente_produto_fixture["produto_id"],
        "quantidade": 2
    }
    response = client.post("/carrinhos", json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["cliente_id"] == data["cliente_id"]
    assert json_data["produto_id"] == data["produto_id"]
    assert json_data["quantidade"] == data["quantidade"]

def test_listar_carrinhos(cliente_produto_fixture):
    client.post("/carrinhos", json={
        "cliente_id": cliente_produto_fixture["cliente_id"],
        "produto_id": cliente_produto_fixture["produto_id"],
        "quantidade": 1
    })

    response = client.get("/carrinhos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(c["cliente_id"] == cliente_produto_fixture["cliente_id"] for c in data)

def test_buscar_carrinho_por_id(cliente_produto_fixture):
    post_resp = client.post("/carrinhos", json={
        "cliente_id": cliente_produto_fixture["cliente_id"],
        "produto_id": cliente_produto_fixture["produto_id"],
        "quantidade": 1
    })
    assert post_resp.status_code == 200
    carrinho_id = post_resp.json()["id"]

    response = client.get(f"/carrinhos/{carrinho_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == carrinho_id

def test_atualizar_carrinho(cliente_produto_fixture):
    post_resp = client.post("/carrinhos", json={
        "cliente_id": cliente_produto_fixture["cliente_id"],
        "produto_id": cliente_produto_fixture["produto_id"],
        "quantidade": 1
    })
    assert post_resp.status_code == 200
    carrinho_id = post_resp.json()["id"]

    update_data = {
        "cliente_id": cliente_produto_fixture["cliente_id"],
        "produto_id": cliente_produto_fixture["produto_id"],
        "quantidade": 5
    }

    response = client.put(f"/carrinhos/{carrinho_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["quantidade"] == 5

def test_excluir_carrinho(cliente_produto_fixture):
    post_resp = client.post("/carrinhos", json={
        "cliente_id": cliente_produto_fixture["cliente_id"],
        "produto_id": cliente_produto_fixture["produto_id"],
        "quantidade": 1
    })
    assert post_resp.status_code == 200
    carrinho_id = post_resp.json()["id"]

    delete_resp = client.delete(f"/carrinhos/{carrinho_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json().get("detail") == "Carrinho excluído com sucesso"

    # Verificar se realmente foi excluído
    response = client.get(f"/carrinhos/{carrinho_id}")
    assert response.status_code == 404
