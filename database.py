from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL de conexão fornecida (Neon / Vercel Postgres)
# Usando a versão "pooled" para melhor performance em serverless
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a "engine" de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria a classe de Sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos (tabelas)
Base = declarative_base()

# Dependência para pegar a sessão do banco em cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()