from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from loguru import logger
from app.api.deps import get_database
from app.models.call_record import CallRecord
from app.models.client import Client
from app.schemas.client import CallHistoryResponse, CallRecordWithClient, ClientResponse, CallRecordResponse

router = APIRouter()


@router.get("/history", response_model=CallHistoryResponse)
async def get_call_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: str = Query(None),
    db: AsyncSession = Depends(get_database)
):
    """
    Получает общую историю звонков с пагинацией.
    """
    try:
        # Базовый запрос с загрузкой клиента
        query = select(CallRecord).options(joinedload(CallRecord.client))
        count_query = select(func.count(CallRecord.id))
        
        if category:
            query = query.where(CallRecord.category == category)
            count_query = count_query.where(CallRecord.category == category)
        
        # Получаем общее количество
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Применяем пагинацию
        offset = (page - 1) * page_size
        query = query.order_by(CallRecord.created_at.desc()).offset(offset).limit(page_size)
        
        # Выполняем запрос
        result = await db.execute(query)
        records = result.scalars().unique().all()
        
        items = []
        for record in records:
            # Преобразуем в схему
            client_data = ClientResponse.model_validate(record.client)
            record_data = CallRecordResponse.model_validate(record)
            
            items.append(CallRecordWithClient(
                **record_data.model_dump(),
                client=client_data
            ))
            
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        return CallHistoryResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
    except Exception as e:
        logger.error(f"Ошибка при получении истории звонков: {e}")
        raise HTTPException(status_code=500, detail=str(e))
