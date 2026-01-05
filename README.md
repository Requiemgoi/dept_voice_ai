# DebtCall Automator - Система автоматизированного обзвона должников

Система для автоматизированного обзвона должников с использованием AI для распознавания речи и классификации ответов.

## 🏗️ Структура проекта

```
.
├── backend/          # FastAPI backend (НҰРЫМ)
│   ├── app/         # Основное приложение
│   ├── ml/          # ML модули (заглушки для АРМАНА Б)
│   ├── data/        # Данные (БД, аудио, файлы)
│   └── main.py      # Точка входа
├── frontend/         # Frontend приложение (будущее)
└── ml/               # ML модули (будущее - АРМАН Б)
```

## 🚀 Быстрый старт

### Backend (НҰРЫМ)

1. **Установка зависимостей:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Запуск сервера:**
```bash
# Windows
.\start_clean.bat

# Linux/Mac
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

3. **Проверка работы:**
- API документация: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## 📋 API Endpoints

### Загрузка данных
- `POST /api/v1/upload` - Загрузка Excel файла с клиентами

### Работа с клиентами
- `GET /api/v1/clients` - Список клиентов (с пагинацией)
- `GET /api/v1/clients/{id}` - Детали клиента с историей звонков

### Обработка звонков
- `POST /api/v1/process/{id}` - Обработка одного клиента
- `POST /api/v1/process/{id}/response` - Загрузка аудио ответа
- `POST /api/v1/process/bulk` - Массовая обработка
- `GET /api/v1/process/bulk/{task_id}/status` - Статус массовой обработки

### Экспорт
- `GET /api/v1/export` - Экспорт результатов в Excel

### Аудио файлы
- `GET /api/v1/audio/tts/{client_id}.wav` - TTS аудио
- `GET /api/v1/audio/response/{client_id}.wav` - Аудио ответ клиента

## 👥 Работа команды

### Для ML разработчика (АРМАН Б)

Место для вашего кода: `backend/ml/`

**Текущие заглушки:**
- `backend/ml/stt_engine.py` - Распознавание речи (STT)
- `backend/ml/classifier_engine.py` - Классификация ответов

**Интерфейсы функций:**

```python
# STT Engine
def recognize_audio(audio_path: str, lang: str = 'ru') -> tuple[str, str]:
    """
    Распознает речь из аудио файла.
    Returns: (транскрипт, обнаруженный язык)
    """
    pass

# Classifier Engine
def classify_response(transcript: str, lang: str = 'ru') -> tuple[str, dict]:
    """
    Классифицирует ответ клиента.
    Returns: (категория, метаданные с confidence)
    
    Категории:
    - promise: обещание погасить
    - refusal: отказ
    - question: вопрос
    - request_info: запрос информации
    - other: другое
    """
    pass
```

**Интеграция:**
Функции уже импортированы в `backend/app/core/call_pipeline.py`. Просто замените заглушки на реальную реализацию.

### Для Frontend разработчика

**API Base URL:** `http://localhost:8000`

**CORS:** Настроен для `http://localhost:5173` и `http://localhost:3000`

**Основные endpoints для работы:**
1. Загрузка Excel: `POST /api/v1/upload`
2. Список клиентов: `GET /api/v1/clients?page=1&page_size=20`
3. Обработка клиента: `POST /api/v1/process/{id}`
4. Загрузка ответа: `POST /api/v1/process/{id}/response`
5. Экспорт: `GET /api/v1/export`

**Примеры запросов:**
```javascript
// Получить список клиентов
fetch('http://localhost:8000/api/v1/clients?page=1&page_size=20')
  .then(res => res.json())
  .then(data => console.log(data));

// Загрузить Excel файл
const formData = new FormData();
formData.append('file', fileInput.files[0]);
fetch('http://localhost:8000/api/v1/upload', {
  method: 'POST',
  body: formData
});
```

## 🛠️ Технологии

### Backend
- FastAPI 0.109+
- SQLAlchemy 2.0+ (async)
- SQLite (aiosqlite)
- Pandas (для работы с Excel)
- Loguru (логирование)
- espeak-ng (TTS)

### ML (планируется)
- Speech-to-Text engine
- Text classification model

### Frontend (планируется)
- React/Vue/другое

## 📁 Структура данных

### Модель Client
- `id`, `fio`, `iin`, `creditor`, `amount`, `days_overdue`, `phone`
- `status`: pending, processing, awaiting_response, completed, failed
- `category`: promise, refusal, question, request_info, other
- `created_at`, `processed_at`

### Модель CallRecord
- `id`, `client_id`, `tts_text`, `tts_audio_path`, `response_audio_path`
- `transcript`, `detected_language`, `category`, `confidence`
- `call_metadata` (JSON), `created_at`

## 🔧 Настройка

### Переменные окружения (.env)
```env
DATABASE_URL=sqlite+aiosqlite:///./data/db/app.db
AUDIO_STORAGE_PATH=./data/audio
UPLOAD_PATH=./data/uploads
EXPORT_PATH=./data/exports
TTS_ENGINE=espeak-ng
```

## 📝 Формат Excel файла

Ожидаемые колонки:
- ФИО
- ИИН
- Кредитор
- Сумма
- Дни просрочки
- Телефон

## 🐛 Решение проблем

См. файлы:
- `backend/TROUBLESHOOTING.md` - Общие проблемы
- `backend/PORT_ISSUE.md` - Проблемы с портами
- `backend/DEBUG_CONNECTION.md` - Проблемы подключения
- `backend/INSTALL.md` - Проблемы установки

## 📄 Лицензия

[Указать лицензию]

## 👨‍💻 Команда

- **Backend:** НҰРЫМ
- **ML:** АРМАН Б
- **Frontend:** АРМАН А, МИРАС

