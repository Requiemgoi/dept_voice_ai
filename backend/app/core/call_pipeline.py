from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger
from app.models.client import Client
from app.models.call_record import CallRecord
from app.core.tts import generate_tts
from ml.stt_engine import recognize_audio
from ml.classifier_engine import classify_response


async def process_call(
    client: Client,
    use_demo_audio: bool,
    db: AsyncSession
) -> dict:
    """
    Обрабатывает звонок клиенту: генерирует TTS, ожидает ответ, обрабатывает через STT и классификатор.
    
    Args:
        client: Объект Client
        use_demo_audio: Использовать ли демо аудио файлы
        db: Сессия БД
        
    Returns:
        dict: Статус обработки и информация
    """
    try:
        # Генерируем текст для TTS
        tts_text = (
            f"Здравствуйте, {client.fio}. "
            f"Это служба взыскания {client.creditor}. "
            f"У вас задолженность {client.amount} тенге, "
            f"просроченная на {client.days_overdue} дней. "
            f"Когда планируете погасить?"
        )
        
        # Обновляем статус клиента
        client.status = 'processing'
        await db.commit()
        
        # Генерируем TTS аудио
        tts_audio_path = await generate_tts(tts_text, 'ru', client.id)
        
        # Создаем запись о звонке
        call_record = CallRecord(
            client_id=client.id,
            tts_text=tts_text,
            tts_audio_path=tts_audio_path
        )
        db.add(call_record)
        await db.commit()
        await db.refresh(call_record)
        
        if use_demo_audio:
            # Используем демо аудио для тестирования
            logger.info(f"Используется демо аудио для клиента {client.id}")
            # Здесь можно добавить логику для использования предзаписанных файлов
            # Пока просто возвращаем статус
            return {
                "status": "demo_mode",
                "client_id": client.id,
                "call_record_id": call_record.id,
                "tts_audio_path": tts_audio_path,
                "message": "Демо режим активирован"
            }
        else:
            # Возвращаем статус ожидания ответа
            client.status = 'awaiting_response'
            await db.commit()
            
            return {
                "status": "awaiting_response",
                "client_id": client.id,
                "call_record_id": call_record.id,
                "tts_audio_url": f"/api/v1/audio/tts/{client.id}.wav",
                "message": "TTS аудио готово, ожидается ответ клиента"
            }
            
    except Exception as e:
        logger.error(f"Ошибка при обработке звонка для клиента {client.id}: {e}")
        client.status = 'failed'
        await db.commit()
        raise


async def process_response_audio(
    client_id: int,
    response_audio_path: str,
    db: AsyncSession
) -> dict:
    """
    Обрабатывает полученный аудио ответ от клиента.
    
    Args:
        client_id: ID клиента
        response_audio_path: Путь к аудио файлу ответа
        db: Сессия БД
        
    Returns:
        dict: Результаты обработки
    """
    try:
        # Получаем клиента
        result = await db.execute(select(Client).where(Client.id == client_id))
        client = result.scalar_one_or_none()
        
        if not client:
            raise ValueError(f"Клиент с ID {client_id} не найден")
        
        # Получаем последнюю запись звонка
        result = await db.execute(
            select(CallRecord)
            .where(CallRecord.client_id == client_id)
            .order_by(CallRecord.created_at.desc())
        )
        call_record = result.scalar_one_or_none()
        
        if not call_record:
            raise ValueError(f"Запись звонка для клиента {client_id} не найдена")
        
        # Обновляем путь к аудио ответа
        call_record.response_audio_path = response_audio_path
        
        # Вызываем STT
        logger.info(f"Обработка аудио через STT: {response_audio_path}")
        transcript, detected_language = recognize_audio(response_audio_path)
        call_record.transcript = transcript
        call_record.detected_language = detected_language
        
        # Вызываем классификатор
        logger.info(f"Классификация ответа: {transcript[:50]}...")
        category, metadata = classify_response(transcript, detected_language)
        call_record.category = category
        call_record.confidence = metadata.get('confidence', 0.0)
        call_record.call_metadata = metadata
        
        # Обновляем статус клиента
        client.status = 'completed'
        client.category = category
        client.processed_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(call_record)
        
        logger.info(f"Обработка завершена для клиента {client_id}: категория={category}")
        
        return {
            "status": "completed",
            "client_id": client_id,
            "call_record_id": call_record.id,
            "transcript": transcript,
            "detected_language": detected_language,
            "category": category,
            "confidence": call_record.confidence,
            "metadata": metadata
        }
        
    except Exception as e:
        logger.error(f"Ошибка при обработке ответа для клиента {client_id}: {e}")
        await db.rollback()
        raise

