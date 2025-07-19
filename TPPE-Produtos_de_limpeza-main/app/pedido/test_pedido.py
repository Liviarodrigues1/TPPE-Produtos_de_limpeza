import pytest
from fastapi.testclient import TestClient
from main import app  # Certifique-se de importar do local correto

client = TestClient(app)

cliente_exemplo = {
    "nome": "Maria Compradora",
    "email": "maria@email.com",
    "telefone": "11999999999"
}

produto_exemplo = {
    "nome": "Teclado Mecânico",
    "preco": 199.90,
    "estoque": 50
}

@pytest.fixture
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
    client.delete(f"/pedidos/{cliente_id}")  # não funcionará se o ID não for de pedido — pode ser ignorado se for falso positivo
    client.delete(f"/clientes/{cliente_id}")
    client.delete(f"/produtos/{produto_id}")

def test_criar_pedido(setup_cliente_produto):
    data = {
        "cliente_id": setup_cliente_produto["cliente_id"],
        "produto_id": setup_cliente_produto["produto_id"],
        "quantidade": 3,
        "preco_unitario": 199.90
    }
    response = client.post("/pedidos/", json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["cliente_id"] == data["cliente_id"]
    assert json_data["produto_id"] == data["produto_id"]
    assert float(json_data["valor_total"]) == pytest.approx(3 * 199.90, 0.01)

def test_listar_pedidos(setup_cliente_produto):
    # Garante que pelo menos um pedido existe
    client.post("/pedidos/", json={
        "cliente_id": setup_cliente_produto["cliente_id"],
        "produto_id": setup_cliente_produto["produto_id"],
        "quantidade": 2,
        "preco_unitario": 199.90
    })

    response = client.get("/pedidos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(p["cliente_id"] == setup_cliente_produto["cliente_id"] for p in data)

def test_buscar_pedido_por_id(setup_cliente_produto):
    post_resp = client.post("/pedidos/", json={
        "cliente_id": setup_cliente_produto["cliente_id"],
        "produto_id": setup_cliente_produto["produto_id"],
        "quantidade": 1,
        "preco_unitario": 199.90
    })
    assert post_resp.status_code == 200
    pedido_id = post_resp.json()["id"]

    response = client.get(f"/pedidos/{pedido_id}")
    assert response.status_code == 200
    assert response.json()["id"] == pedido_id

def test_atualizar_pedido(setup_cliente_produto):
    post_resp = client.post("/pedidos/", json={
        "cliente_id": setup_cliente_produto["cliente_id"],
        "produto_id": setup_cliente_produto["produto_id"],
        "quantidade": 2,
        "preco_unitario": 199.90
    })
    pedido_id = post_resp.json()["id"]

    update_data = {
        "cliente_id": setup_cliente_produto["cliente_id"],
        "produto_id": setup_cliente_produto["produto_id"],
        "quantidade": 5,
        "preco_unitario": 189.90
    }

    response = client.put(f"/pedidos/{pedido_id}", json=update_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["quantidade"] == 5
    assert float(json_data["valor_total"]) == pytest.approx(5 * 189.90, 0.01)

def test_excluir_pedido(setup_cliente_produto):
    post_resp = client.post("/pedidos/", json={
        "cliente_id": setup_cliente_produto["cliente_id"],
        "produto_id": setup_cliente_produto["produto_id"],
        "quantidade": 1,
        "preco_unitario": 199.90
    })
    pedido_id = post_resp.json()["id"]

    delete_resp = client.delete(f"/pedidos/{pedido_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json().get("detail") == "Pedido excluído com sucesso"

    # Verifica se realmente foi excluído
    get_resp = client.get(f"/pedidos/{pedido_id}")
    assert get_resp.status_code == 404
