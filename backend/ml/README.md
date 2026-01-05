# ML модули

Этот раздел предназначен для ML разработчика (АРМАН Б).

## Текущие заглушки

### `stt_engine.py`
Модуль для распознавания речи (Speech-to-Text).

**Функция:**
```python
def recognize_audio(audio_path: str, lang: str = 'ru') -> tuple[str, str]:
    """
    Распознает речь из аудио файла.
    
    Args:
        audio_path: Путь к аудио файлу
        lang: Предполагаемый язык (ru, kk, en)
        
    Returns:
        tuple: (транскрипт, обнаруженный язык)
    """
```

**Требования:**
- Поддержка форматов: .wav, .mp3, .ogg, .m4a
- Поддержка языков: русский, казахский, английский
- Возврат обнаруженного языка

### `classifier_engine.py`
Модуль для классификации ответов клиентов.

**Функция:**
```python
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
```

**Требования:**
- Классификация на 5 категорий
- Возврат confidence score
- Поддержка русского и казахского языков

## Интеграция

Функции уже импортированы в `app/core/call_pipeline.py`:

```python
from ml.stt_engine import recognize_audio
from ml.classifier_engine import classify_response
```

Просто замените заглушки на реальную реализацию - интеграция уже готова!

## Тестирование

После реализации можно протестировать через API:
1. Загрузите клиентов через `/api/v1/upload`
2. Запустите обработку через `/api/v1/process/{id}`
3. Загрузите аудио ответ через `/api/v1/process/{id}/response`
4. Проверьте результат в `/api/v1/clients/{id}`

## Зависимости

Добавьте необходимые ML библиотеки в `backend/requirements.txt`:
- torch / tensorflow
- transformers
- librosa / soundfile (для аудио)
- и другие по необходимости

