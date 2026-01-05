from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from loguru import logger
from pathlib import Path
from app.api.v1 import upload, clients, process, export, history, analytics
from app.db.base import Base
from app.db.session import engine
from app.config import settings

# Настройка логирования
Path("logs").mkdir(exist_ok=True)
logger.add("logs/app.log", rotation="10 MB", retention="7 days", level="INFO")

app = FastAPI(title="DebtCall Automator API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(clients.router, prefix="/api/v1", tags=["clients"])
app.include_router(process.router, prefix="/api/v1", tags=["process"])
app.include_router(export.router, prefix="/api/v1", tags=["export"])
app.include_router(history.router, prefix="/api/v1", tags=["history"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])


@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске приложения."""
    logger.info("Запуск приложения DebtCall Automator API")
    
    # Создаем таблицы БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("База данных инициализирована")


@app.on_event("shutdown")
async def shutdown_event():
    """Очистка при остановке приложения."""
    logger.info("Остановка приложения")


@app.get("/")
def root():
    """Корневой endpoint."""
    return {
        "message": "DebtCall Automator API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/favicon.ico")
async def favicon():
    """Обработчик для favicon.ico - возвращает пустой ответ чтобы убрать 404 ошибку."""
    return Response(status_code=204)

