from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from loguru import logger
from app.api.deps import get_database
from app.models.client import Client
from app.models.call_record import CallRecord
from app.schemas.client import (
    ClientResponse,
    ClientDetail,
    ClientListResponse,
    PaginationParams
)

router = APIRouter()


@router.get("/clients", response_model=ClientListResponse)
async def get_clients(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    db: AsyncSession = Depends(get_database)
):
    """
    Получает список клиентов с пагинацией.
    
    Query параметры:
    - page: номер страницы (начиная с 1)
    - page_size: размер страницы (1-100)
    - status: фильтр по статусу (опционально)
    """
    try:
        # Строим запрос
        query = select(Client)
        count_query = select(func.count(Client.id))
        
        if status:
            query = query.where(Client.status == status)
            count_query = count_query.where(Client.status == status)
        
        # Получаем общее количество
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Применяем пагинацию
        offset = (page - 1) * page_size
        query = query.order_by(Client.created_at.desc()).offset(offset).limit(page_size)
        
        # Выполняем запрос
        result = await db.execute(query)
        clients = result.scalars().all()
        
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        return ClientListResponse(
            items=[ClientResponse.model_validate(client) for client in clients],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
    except Exception as e:
        logger.error(f"Ошибка при получении списка клиентов: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clients/{client_id}", response_model=ClientDetail)
async def get_client_detail(
    client_id: int,
    db: AsyncSession = Depends(get_database)
):
    """
    Получает детальную информацию о клиенте с историей звонков.
    """
    try:
        # Получаем клиента
        result = await db.execute(select(Client).where(Client.id == client_id))
        client = result.scalar_one_or_none()
        
        if not client:
            raise HTTPException(status_code=404, detail=f"Клиент с ID {client_id} не найден")
        
        # Получаем записи звонков
        result = await db.execute(
            select(CallRecord)
            .where(CallRecord.client_id == client_id)
            .order_by(CallRecord.created_at.desc())
        )
        call_records = result.scalars().all()
        
        from app.schemas.client import CallRecordResponse
        
        return ClientDetail(
            **ClientResponse.model_validate(client).model_dump(),
            call_records=[CallRecordResponse.model_validate(cr) for cr in call_records]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении клиента {client_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

