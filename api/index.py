# main.py

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
# Corrigido para importação ABSOLUTA para funcionar no Render/Vercel
from routes import router as event_router
from database import engine
import models

# --- CRIAÇÃO DAS TABELAS NO BANCO DE DADOS ---
# Isso garante que as tabelas existam quando a API iniciar.
# Em produção, o ideal é usar Alembic para migrações, mas isso resolve para o Vercel.
models.Base.metadata.create_all(bind=engine)

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="API de Eventos - Anderson Viagem e Turismo",
    description="API para gerenciar os eventos de excursão usando Postgres (Neon/Vercel).",
    version="1.1.0"
)

# Adiciona o middleware de CORS à sua aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

# Inclui as rotas definidas no arquivo routes.py
app.include_router(event_router, prefix="/api/v1")

# --- Endpoints de Status ---

# Rota "raiz" para verificar se a API está online
@app.get("/", tags=["Status"])
async def read_root():
    """ Rota principal para verificar o status da API. """
    return {"message": "Bem-vindo à API de Eventos!"}

# Endpoint de "health check" para o UptimeRobot (via GET)
@app.get("/health", tags=["Status"], summary="Health check endpoint (GET)")
async def health_check_get():
    """
    Endpoint leve para monitoramento contínuo (health check).
    Ideal para verificar no navegador se a API está rodando. Retorna um status 'ok'.
    """
    return {"status": "ok"}

# Endpoint de "health check" para o UptimeRobot (via HEAD)
@app.head("/health", tags=["Status"], summary="Health check endpoint (HEAD)")
async def health_check_head():
    """
    Endpoint super leve para monitoramento (health check) via HEAD.
    """
    return Response(status_code=200)