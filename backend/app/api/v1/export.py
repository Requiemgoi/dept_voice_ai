from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
from loguru import logger
from datetime import datetime
from app.api.deps import get_database
from app.models.client import Client
from app.utils.excel import export_to_excel
from app.config import settings

router = APIRouter()


@router.get("/export")
async def export_clients(
    status: str = Query(None),
    category: str = Query(None),
    db: AsyncSession = Depends(get_database)
):
    """
    Экспортирует клиентов в Excel файл.
    
    Query параметры:
    - status: фильтр по статусу (опционально)
    - category: фильтр по категории (опционально)
    """
    try:
        # Строим запрос
        query = select(Client)
        
        if status:
            query = query.where(Client.status == status)
        
        if category:
            query = query.where(Client.category == category)
        
        query = query.order_by(Client.created_at.desc())
        
        # Получаем клиентов
        result = await db.execute(query)
        clients = result.scalars().all()
        
        if not clients:
            raise HTTPException(status_code=404, detail="Клиенты не найдены")
        
        # Генерируем имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"clients_export_{timestamp}.xlsx"
        output_path = Path(settings.EXPORT_PATH) / filename
        
        # Экспортируем
        await export_to_excel(clients, str(output_path))
        
        return FileResponse(
            path=str(output_path),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при экспорте: {e}")
        raise HTTPException(status_code=500, detail=str(e))

