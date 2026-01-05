"""
API модуль для обработки голосовых звонков.

Endpoints:
    - POST /api/voice/process - Обработка аудио файла (STT + классификация)
    - POST /api/voice/classify - Классификация текста
    - GET /api/voice/health - Проверка состояния сервиса
"""

from .voice import router as voice_router

__all__ = ['voice_router']
