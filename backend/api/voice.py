"""
API endpoints для обработки голосовых звонков.

Объединяет STT (распознавание речи) и классификатор ответов должников.
"""

import os
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Literal

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from pydantic import BaseModel, Field

from ml.stt_engine import stt_engine, STTEngineError, ModelNotFoundError, AudioFormatError
from ml.classifier_engine import classify_response, get_category_description, Category
from ml.language_detector import detect_language, get_language_confidence

router = APIRouter(prefix="/api/voice", tags=["voice"])


# ============ Pydantic Models ============

class ClassificationResult(BaseModel):
    """Результат классификации ответа."""
    category: Category
    category_description: str
    confidence: float
    matched_keywords: list[str]
    promised_date: Optional[str] = None
    reason: Optional[str] = None


class VoiceProcessingResult(BaseModel):
    """Результат полной обработки голосового сообщения."""
    success: bool
    request_id: str
    timestamp: str
    
    # STT результаты
    transcript: str
    detected_language: str
    language_confidence: float
    
    # Классификация
    classification: ClassificationResult
    
    # Метаданные
    processing_time_ms: Optional[float] = None
    audio_duration_sec: Optional[float] = None


class TextClassificationRequest(BaseModel):
    """Запрос на классификацию текста."""
    text: str = Field(..., min_length=1, description="Текст для классификации")
    language: Literal['ru', 'kk', 'auto'] = Field(
        default='auto',
        description="Язык текста (ru, kk, или auto для автоопределения)"
    )


class TextClassificationResult(BaseModel):
    """Результат классификации текста."""
    success: bool
    request_id: str
    timestamp: str
    
    # Входные данные
    text: str
    detected_language: str
    
    # Классификация
    classification: ClassificationResult


class HealthStatus(BaseModel):
    """Статус здоровья сервиса."""
    status: Literal['healthy', 'degraded', 'unhealthy']
    timestamp: str
    version: str = "1.0.0"
    
    # Доступность моделей
    models: dict[str, bool]
    available_languages: list[str]


class ErrorResponse(BaseModel):
    """Ответ с ошибкой."""
    success: bool = False
    error: str
    error_code: str
    request_id: str
    timestamp: str


# ============ Helper Functions ============

def generate_request_id() -> str:
    """Генерирует уникальный ID запроса."""
    return str(uuid.uuid4())[:8]


def get_timestamp() -> str:
    """Возвращает текущую метку времени в ISO формате."""
    return datetime.utcnow().isoformat() + "Z"


# ============ API Endpoints ============

@router.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Проверка состояния сервиса.
    
    Возвращает информацию о доступности моделей и статусе сервиса.
    """
    models_status = {
        'ru': stt_engine.is_model_available('ru'),
        'kk': stt_engine.is_model_available('kk')
    }
    
    available_languages = stt_engine.get_available_languages()
    
    # Определяем общий статус
    if all(models_status.values()):
        status = 'healthy'
    elif any(models_status.values()):
        status = 'degraded'
    else:
        status = 'unhealthy'
    
    return HealthStatus(
        status=status,
        timestamp=get_timestamp(),
        models=models_status,
        available_languages=available_languages
    )


@router.post(
    "/process",
    response_model=VoiceProcessingResult,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid audio format"},
        500: {"model": ErrorResponse, "description": "Processing error"}
    }
)
async def process_voice(
    audio: UploadFile = File(..., description="WAV файл (16kHz, mono, 16-bit)"),
    language: Literal['ru', 'kk', 'auto'] = Form(
        default='auto',
        description="Язык распознавания (ru, kk, или auto)"
    )
):
    """
    Обрабатывает голосовое сообщение: STT + классификация.
    
    Принимает WAV файл и возвращает распознанный текст с классификацией.
    
    **Требования к аудио:**
    - Формат: WAV
    - Sample rate: 16000 Hz
    - Channels: 1 (mono)
    - Bit depth: 16-bit
    
    **Поддерживаемые языки:**
    - ru: Русский
    - kk: Казахский
    - auto: Автоматическое определение
    """
    request_id = generate_request_id()
    start_time = datetime.utcnow()
    
    # Проверяем тип файла
    if not audio.filename or not audio.filename.lower().endswith('.wav'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": "Требуется WAV файл",
                "error_code": "INVALID_FILE_TYPE",
                "request_id": request_id,
                "timestamp": get_timestamp()
            }
        )
    
    # Сохраняем временный файл
    temp_dir = tempfile.gettempdir()
    temp_path = Path(temp_dir) / f"voice_{request_id}.wav"
    
    try:
        # Записываем загруженный файл
        content = await audio.read()
        with open(temp_path, 'wb') as f:
            f.write(content)
        
        # STT распознавание
        if language == 'auto':
            transcript, detected_lang = stt_engine.recognize_auto_detect(str(temp_path))
        else:
            transcript, detected_lang = stt_engine.recognize_audio(str(temp_path), language)
        
        # Определяем уверенность в языке
        if transcript:
            _, lang_confidence = get_language_confidence(transcript)
        else:
            lang_confidence = 0.0
        
        # Классификация
        category, metadata = classify_response(transcript, detected_lang)
        category_desc = get_category_description(category, detected_lang)
        
        # Вычисляем время обработки
        processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        return VoiceProcessingResult(
            success=True,
            request_id=request_id,
            timestamp=get_timestamp(),
            transcript=transcript,
            detected_language=detected_lang,
            language_confidence=round(lang_confidence, 2),
            classification=ClassificationResult(
                category=category,
                category_description=category_desc,
                confidence=metadata.get('confidence', 0.0),
                matched_keywords=metadata.get('matched_keywords', []),
                promised_date=metadata.get('promised_date'),
                reason=metadata.get('reason')
            ),
            processing_time_ms=round(processing_time, 2)
        )
        
    except ModelNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "success": False,
                "error": str(e),
                "error_code": "MODEL_NOT_FOUND",
                "request_id": request_id,
                "timestamp": get_timestamp()
            }
        )
    except AudioFormatError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": str(e),
                "error_code": "INVALID_AUDIO_FORMAT",
                "request_id": request_id,
                "timestamp": get_timestamp()
            }
        )
    except STTEngineError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": str(e),
                "error_code": "STT_ERROR",
                "request_id": request_id,
                "timestamp": get_timestamp()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": f"Внутренняя ошибка: {str(e)}",
                "error_code": "INTERNAL_ERROR",
                "request_id": request_id,
                "timestamp": get_timestamp()
            }
        )
    finally:
        # Удаляем временный файл
        if temp_path.exists():
            try:
                os.unlink(temp_path)
            except Exception:
                pass


@router.post(
    "/classify",
    response_model=TextClassificationResult,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"}
    }
)
async def classify_text(request: TextClassificationRequest):
    """
    Классифицирует текстовый ответ должника.
    
    Используется когда текст уже распознан или введен вручную.
    
    **Категории:**
    - ignore: Отказ от оплаты
    - promise: Обещание оплаты
    - help: Просьба о помощи/рассрочке
    - wrong_number: Неправильный номер
    - third_party: Третье лицо
    - hangup: Проблемы со связью
    """
    request_id = generate_request_id()
    
    try:
        # Определяем язык
        if request.language == 'auto':
            detected_lang = detect_language(request.text)
            if detected_lang == 'unknown':
                detected_lang = 'ru'  # По умолчанию русский
        else:
            detected_lang = request.language
        
        # Классификация
        category, metadata = classify_response(request.text, detected_lang)
        category_desc = get_category_description(category, detected_lang)
        
        return TextClassificationResult(
            success=True,
            request_id=request_id,
            timestamp=get_timestamp(),
            text=request.text,
            detected_language=detected_lang,
            classification=ClassificationResult(
                category=category,
                category_description=category_desc,
                confidence=metadata.get('confidence', 0.0),
                matched_keywords=metadata.get('matched_keywords', []),
                promised_date=metadata.get('promised_date'),
                reason=metadata.get('reason')
            )
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": f"Ошибка классификации: {str(e)}",
                "error_code": "CLASSIFICATION_ERROR",
                "request_id": request_id,
                "timestamp": get_timestamp()
            }
        )


@router.get("/languages")
async def get_supported_languages():
    """
    Возвращает список поддерживаемых языков.
    """
    return {
        "languages": [
            {
                "code": "ru",
                "name": "Русский",
                "available": stt_engine.is_model_available('ru')
            },
            {
                "code": "kk", 
                "name": "Қазақша",
                "available": stt_engine.is_model_available('kk')
            }
        ]
    }


@router.get("/categories")
async def get_categories(language: Literal['ru', 'kk'] = 'ru'):
    """
    Возвращает список категорий классификации с описаниями.
    """
    categories: list[Category] = ['ignore', 'promise', 'help', 'wrong_number', 'third_party', 'hangup']
    
    return {
        "categories": [
            {
                "code": cat,
                "description": get_category_description(cat, language)
            }
            for cat in categories
        ]
    }
