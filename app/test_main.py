# Função de teste comentada por enquanto, pois não será usada agora

# def test_hello_world():
#     # Importa o TestClient da FastAPI para simular requisições HTTP nos testes
#     from fastapi.testclient import TestClient
#     
#     # Importa o objeto `app` da aplicação principal localizada em app/main.py
#     from app.main import app
#     
#     # Cria um cliente de teste com a aplicação
#     client = TestClient(app)
#     
#     # Envia uma requisição GET para o endpoint raiz "/"
#     response = client.get("/")
#     
#     # Verifica se o status da resposta é 200 (OK)
#     assert response.status_code == 200
#     
#     # Verifica se o conteúdo da resposta corresponde ao esperado
#     assert response.json() == {"message": "Hello, World!"}
