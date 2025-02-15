import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, EmpresaDB, ObrigacaoAcessoriaDB
from main import app
from database import SessionLocal

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def reset_db():
    db = SessionLocalTest()
    try:
        db.query(EmpresaDB).delete()
        db.query(ObrigacaoAcessoriaDB).delete()
        db.commit()
    finally:
        db.close()
    yield db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

def test_create_empresa(client, reset_db):
    empresa_data = {
        "nome": "Empresa Teste",
        "cnpj": "12345678000195",
        "endereco": "Rua Teste, 123",
        "email": "contato@empresa.com",
        "telefone": "123456789"
    }

    response = client.post("/empresas/", json=empresa_data)
    print(response.status_code)  
    print(response.text)

    assert response.status_code == 200
    assert response.json()["nome"] == empresa_data["nome"]
    assert response.json()["cnpj"] == empresa_data["cnpj"]
    # Verifique que o campo 'id' foi retornado na resposta
    assert "id" in response.json(), "O campo 'id' não foi retornado na resposta"

def test_create_obrigacao(client, reset_db):
    empresa_data = {
        "nome": "Empresa Teste 2",
        "cnpj": "98765432000100",
        "endereco": "Rua Teste, 456",
        "email": "empresa2@teste.com",
        "telefone": "987654321"
    }

    empresa_response = client.post("/empresas/", json=empresa_data)
    print(empresa_response.json())  # Debug para verificar a resposta

    empresa_id = empresa_response.json().get("id")
    assert empresa_id is not None, "O campo 'id' não foi retornado na resposta"

    obrigacao_data = {
        "nome": "Declaração X",
        "periodicidade": "mensal",
        "empresa_id": empresa_id
    }

    response = client.post("/obrigacoes/", json=obrigacao_data)

    assert response.status_code == 200
    assert response.json()["nome"] == obrigacao_data["nome"]
    assert response.json()["empresa_id"] == empresa_id
