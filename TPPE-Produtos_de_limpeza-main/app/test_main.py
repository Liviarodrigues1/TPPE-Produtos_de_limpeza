# import sys
# import os

# Garante que o diretório raiz do projeto esteja no sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from fastapi.testclient import TestClient
# from app.main import app

# def test_hello_world():
    # Cria um cliente de teste com a aplicação
    # client = TestClient(app)
    
    # Envia uma requisição GET para o endpoint raiz "/"
    # response = client.get("/")
    
    # Verifica se o status da resposta é 200 (OK)
    # assert response.status_code == 200
    
    # Verifica se o conteúdo da resposta corresponde ao esperado
    # assert response.json() == {"message": "Hello, World!"}
