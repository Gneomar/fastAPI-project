from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.auth import auth_router

from src.core.database import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is starting ...")
    await init_db()
    yield
    print(f"Server is stopping ...")

version = "v1"

app = FastAPI(
    title="API de Proyectos",
    description="API para gestionar proyectos y supervisores",
    version=version,
    lifespan=life_span,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes solo desde localhost:8000
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Rutas
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Hello World!"}

# Enter src path in terminal
# uvicorn src.main:app --reload --host 0.0.0.0 --port 8000