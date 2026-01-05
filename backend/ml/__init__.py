"""
ML модули для распознавания речи и классификации ответов должников.

Modules:
    - stt_engine: Speech-to-Text с использованием Vosk
    - classifier_engine: Rule-based классификация ответов
    - language_detector: Определение языка (русский/казахский)
"""

from .language_detector import detect_language
from .classifier_engine import classify_response, extract_date_from_text
from .stt_engine import recognize_audio

__all__ = [
    'detect_language',
    'classify_response',
    'extract_date_from_text',
    'recognize_audio',
]
