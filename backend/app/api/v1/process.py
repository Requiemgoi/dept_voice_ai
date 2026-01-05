from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
from loguru import logger
from typing import Optional
import uuid
import asyncio
from pydantic import BaseModel
from app.api.deps import get_database
from app.models.client import Client
from app.core.call_pipeline import process_call, process_response_audio
from app.config import settings


class BulkProcessRequest(BaseModel):
    client_ids: Optional[list[int]] = None
    use_demo_audio: bool = False

router = APIRouter()

# Хранилище задач массовой обработки (в продакшене использовать Redis или БД)
bulk_tasks: dict[str, dict] = {}


@router.post("/process/{client_id}")
async def process_client(
    client_id: int,
    use_demo_audio: bool = False,
    db: AsyncSession = Depends(get_database)
):
    """
    Обрабатывает одного клиента: запускает TTS, ожидает аудио ответ.
    
    Query параметры:
    - use_demo_audio: использовать демо аудио файлы для тестирования
    """
    try:
        # Получаем клиента
        result = await db.execute(select(Client).where(Client.id == client_id))
        client = result.scalar_one_or_none()
        
        if not client:
            raise HTTPException(status_code=404, detail=f"Клиент с ID {client_id} не найден")
        
        if client.status == 'processing':
            raise HTTPException(
                status_code=400,
                detail="Клиент уже обрабатывается"
            )
        
        # Запускаем обработку
        result = await process_call(client, use_demo_audio, db)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при обработке клиента {client_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process/{client_id}/response")
async def upload_response_audio(
    client_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_database)
):
    """
    Загружает аудио ответ от клиента и обрабатывает его через STT и классификатор.
    """
    try:
        # Проверяем расширение файла
        if not file.filename.endswith(('.wav', '.mp3', '.ogg', '.m4a')):
            raise HTTPException(
                status_code=400,
                detail="Поддерживаются только аудио файлы (.wav, .mp3, .ogg, .m4a)"
            )
        
        # Сохраняем файл
        audio_dir = Path(settings.AUDIO_STORAGE_PATH) / "responses"
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = audio_dir / f"{client_id}.wav"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Аудио ответ загружен: {file_path}")
        
        # Обрабатываем ответ
        result = await process_response_audio(client_id, str(file_path), db)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при загрузке ответа для клиента {client_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process/bulk")
async def process_bulk(
    request: BulkProcessRequest = Body(...),
    db: AsyncSession = Depends(get_database)
):
    """
    Запускает массовую обработку клиентов.
    
    Body:
    - client_ids: список ID клиентов (опционально, если не указан - обрабатываются все pending)
    - use_demo_audio: использовать демо аудио
    """
    try:
        client_ids = request.client_ids
        use_demo_audio = request.use_demo_audio
        
        # Если не указаны ID, берем всех pending клиентов
        if not client_ids:
            result = await db.execute(
                select(Client).where(Client.status == 'pending')
            )
            clients = result.scalars().all()
            client_ids = [c.id for c in clients]
        
        # Создаем задачу
        task_id = str(uuid.uuid4())
        bulk_tasks[task_id] = {
            "status": "processing",
            "total": len(client_ids),
            "processed": 0,
            "failed": 0,
            "client_ids": client_ids
        }
        
        # Запускаем обработку в фоне
        asyncio.create_task(process_bulk_background(task_id, client_ids, use_demo_audio))
        
        return {
            "task_id": task_id,
            "status": "started",
            "total": len(client_ids),
            "message": "Массовая обработка запущена"
        }
        
    except Exception as e:
        logger.error(f"Ошибка при запуске массовой обработки: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_bulk_background(
    task_id: str,
    client_ids: list[int],
    use_demo_audio: bool
):
    """
    Фоновая задача для массовой обработки.
    """
    from app.db.session import AsyncSessionLocal
    
    try:
        # Создаем новую сессию для фоновой задачи
        async with AsyncSessionLocal() as session:
            for client_id in client_ids:
                try:
                    result = await session.execute(select(Client).where(Client.id == client_id))
                    client = result.scalar_one_or_none()
                    
                    if not client:
                        bulk_tasks[task_id]["failed"] += 1
                        continue
                    
                    await process_call(client, use_demo_audio, session)
                    bulk_tasks[task_id]["processed"] += 1
                    
                except Exception as e:
                    logger.error(f"Ошибка при обработке клиента {client_id}: {e}")
                    bulk_tasks[task_id]["failed"] += 1
                    continue
            
            bulk_tasks[task_id]["status"] = "completed"
        
    except Exception as e:
        logger.error(f"Ошибка в фоновой задаче {task_id}: {e}")
        bulk_tasks[task_id]["status"] = "failed"
        bulk_tasks[task_id]["error"] = str(e)


@router.get("/process/bulk/{task_id}/status")
async def get_bulk_status(task_id: str):
    """
    Получает статус массовой обработки.
    """
    if task_id not in bulk_tasks:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    task = bulk_tasks[task_id]
    
    return {
        "task_id": task_id,
        "status": task["status"],
        "total": task["total"],
        "processed": task["processed"],
        "failed": task["failed"],
        "progress": (task["processed"] + task["failed"]) / task["total"] * 100 if task["total"] > 0 else 0
    }


@router.get("/audio/tts/{client_id}.wav")
async def get_tts_audio(client_id: int):
    """
    Отдает TTS аудио файл для клиента.
    """
    from fastapi.responses import FileResponse
    
    audio_path = Path(settings.AUDIO_STORAGE_PATH) / "tts" / f"{client_id}.wav"
    
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="TTS аудио файл не найден")
    
    return FileResponse(
        path=str(audio_path),
        media_type="audio/wav",
        filename=f"tts_{client_id}.wav"
    )


@router.get("/audio/response/{client_id}.wav")
async def get_response_audio(client_id: int):
    """
    Отдает аудио ответ клиента.
    """
    from fastapi.responses import FileResponse
    
    audio_path = Path(settings.AUDIO_STORAGE_PATH) / "responses" / f"{client_id}.wav"
    
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Аудио ответ не найден")
    
    return FileResponse(
        path=str(audio_path),
        media_type="audio/wav",
        filename=f"response_{client_id}.wav"
    )

