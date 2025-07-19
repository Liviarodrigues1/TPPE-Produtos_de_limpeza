import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

produto_exemplo = {
    "nome": "Teclado Mecânico",
    "preco": 299.90,
    "estoque": 50
}

@pytest.fixture(name="produto_fixture")
def setup_produto():
    response = client.post("/produtos", json=produto_exemplo)
    assert response.status_code == 200
    json_data = response.json()
    yield json_data
    client.delete(f"/produtos/{json_data['id']}")

def test_criar_produto():
    response = client.post("/produtos", json=produto_exemplo)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["nome"] == produto_exemplo["nome"]
    assert float(json_data["preco"]) == produto_exemplo["preco"]
    assert json_data["estoque"] == produto_exemplo["estoque"]
    client.delete(f"/produtos/{json_data['id']}")

def test_listar_produtos(produto_fixture):
    response = client.get("/produtos")
    assert response.status_code == 200
    data = response.json()
    assert any(produto["id"] == produto_fixture["id"] for produto in data)

def test_buscar_produto_por_id(produto_fixture):
    produto_id = produto_fixture["id"]
    response = client.get(f"/produtos/{produto_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == produto_exemplo["nome"]

def test_atualizar_produto(produto_fixture):
    produto_id = produto_fixture["id"]
    update_data = {
        "nome": produto_fixture["nome"],
        "preco": 199.99,
        "estoque": produto_fixture["estoque"]
    }
    response = client.put(f"/produtos/{produto_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert float(data["preco"]) == update_data["preco"]

def test_excluir_produto():
    response = client.post("/produtos", json=produto_exemplo)
    assert response.status_code == 200
    produto_id = response.json()["id"]

    response = client.delete(f"/produtos/{produto_id}")
    assert response.status_code == 200
    assert response.json().get("detail") == "Produto excluído com sucesso"

    response = client.get(f"/produtos/{produto_id}")
    assert response.status_code == 404
