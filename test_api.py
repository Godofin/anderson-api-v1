import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
import schemas
from routes import router
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Usar SQLite em memória para testes rápidos
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router, prefix="/api/v1")

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/api/v1/users",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_get_artists():
    response = client.get("/api/v1/artists")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

if __name__ == "__main__":
    print("Iniciando testes...")
    try:
        test_create_user()
        print("✓ Teste de criação de usuário passou!")
        test_get_artists()
        print("✓ Teste de listagem de artistas passou!")
        print("Todos os testes básicos passaram!")
    except Exception as e:
        print(f"Erro nos testes: {e}")
