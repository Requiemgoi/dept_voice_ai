from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from loguru import logger
from datetime import datetime, timedelta
from app.api.deps import get_database
from app.models.call_record import CallRecord
from app.models.client import Client

router = APIRouter()


@router.get("/statistics")
async def get_statistics(db: AsyncSession = Depends(get_database)):
    """
    Получает общую статистику по обзвонам и клиентам.
    """
    try:
        # Статистика по клиентам
        clients_query = select(
            func.count(Client.id),
            func.count(Client.id).filter(Client.status == 'completed'),
            func.count(Client.id).filter(Client.status == 'processing'),
            func.count(Client.id).filter(Client.status == 'failed'),
            func.count(Client.id).filter(Client.status == 'pending')
        )
        clients_result = await db.execute(clients_query)
        total, completed, processing, failed, pending = clients_result.fetchone()

        # Статистика по категориям
        categories_query = select(
            CallRecord.category,
            func.count(CallRecord.id)
        ).group_by(CallRecord.category).where(CallRecord.category.isnot(None))
        categories_result = await db.execute(categories_query)
        categories_stats = {row[0]: row[1] for row in categories_result.fetchall()}

        # Статистика за последние 7 дней
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        daily_query = select(
            func.date(CallRecord.created_at).label('date'),
            func.count(CallRecord.id)
        ).where(CallRecord.created_at >= seven_days_ago).group_by('date').order_by('date')
        daily_result = await db.execute(daily_query)
        daily_stats = [{"date": str(row[0]), "count": row[1]} for row in daily_result.fetchall()]

        return {
            "summary": {
                "total_clients": total or 0,
                "completed": completed or 0,
                "processing": processing or 0,
                "failed": failed or 0,
                "pending": pending or 0,
                "success_rate": (completed / total * 100) if total and total > 0 else 0
            },
            "categories": categories_stats,
            "daily_activity": daily_stats
        }
    except Exception as e:
        logger.error(f"Ошибка при получении аналитики: {e}")
        raise HTTPException(status_code=500, detail=str(e))
