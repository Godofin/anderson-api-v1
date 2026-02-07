from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from routes import router as gigdex_router
from database import engine
import models

# Criar tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GigDex API",
    description="API para o Rastreador de Shows e Festivais GigDex.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gigdex_router, prefix="/api/v1")

@app.get("/", tags=["Status"])
async def read_root():
    return {"message": "Bem-vindo à API GigDex! O seu rastreador de shows."}

@app.get("/health", tags=["Status"])
async def health_check():
    return {"status": "ok"}
