"""
Модуль для распознавания речи (Speech-to-Text).
Заглушка до реализации от АРМАНА Б.
"""
from loguru import logger


def recognize_audio(audio_path: str, lang: str = 'ru') -> tuple[str, str]:
    """
    Распознает речь из аудио файла.
    
    Args:
        audio_path: Путь к аудио файлу
        lang: Предполагаемый язык (ru, kk, en)
        
    Returns:
        tuple: (транскрипт, обнаруженный язык)
    """
    logger.info(f"STT обработка: {audio_path} (язык: {lang})")
    
    # Заглушка - возвращаем тестовый транскрипт
    # TODO: Реализовать реальное распознавание речи
    test_transcript = "Тестовый транскрипт ответа клиента"
    
    return test_transcript, lang

