"""
Модуль для классификации ответов клиентов.
Заглушка до реализации от АРМАНА Б.
"""
from loguru import logger


def classify_response(transcript: str, lang: str = 'ru') -> tuple[str, dict]:
    """
    Классифицирует ответ клиента на категории.
    
    Args:
        transcript: Транскрипт ответа клиента
        lang: Язык транскрипта
        
    Returns:
        tuple: (категория, метаданные с confidence)
        
    Категории:
        - promise: обещание погасить
        - refusal: отказ
        - question: вопрос
        - request_info: запрос информации
        - other: другое
    """
    logger.info(f"Классификация ответа: {transcript[:50]}... (язык: {lang})")
    
    # Заглушка - возвращаем тестовую категорию
    # TODO: Реализовать реальную классификацию
    
    category = 'promise'
    metadata = {
        'confidence': 0.85,
        'lang': lang,
        'transcript_length': len(transcript)
    }
    
    return category, metadata


def extract_date_from_text(text: str) -> str | None:
    """
    Извлекает дату из текста (обещание оплатить).
    
    Args:
        text: Текст для анализа
        
    Returns:
        Дата в формате YYYY-MM-DD или None
    """
    logger.info(f"Извлечение даты из текста: {text[:50]}...")
    
    # Заглушка - возвращаем None
    # TODO: Реализовать извлечение дат с помощью NLP/регулярных выражений
    
    return None
