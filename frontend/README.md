# Frontend приложение

Этот раздел предназначен для Frontend разработчика.

## API Backend

**Base URL:** `http://localhost:8000`

**CORS:** Настроен для `http://localhost:5173` и `http://localhost:3000`

## Основные endpoints

### 1. Загрузка Excel файла
```http
POST /api/v1/upload
Content-Type: multipart/form-data

Body: file (Excel файл)
Response: {
  "message": "Файл успешно обработан",
  "file_path": "...",
  "added_count": 10,
  "error_count": 0
}
```

### 2. Получить список клиентов
```http
GET /api/v1/clients?page=1&page_size=20&status=pending

Response: {
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

### 3. Получить детали клиента
```http
GET /api/v1/clients/{id}

Response: {
  "id": 1,
  "fio": "...",
  "status": "pending",
  "category": null,
  "call_records": [...]
}
```

### 4. Обработать клиента
```http
POST /api/v1/process/{id}?use_demo_audio=false

Response: {
  "status": "awaiting_response",
  "client_id": 1,
  "tts_audio_url": "/api/v1/audio/tts/1.wav"
}
```

### 5. Загрузить аудио ответ
```http
POST /api/v1/process/{id}/response
Content-Type: multipart/form-data

Body: file (аудио файл)
Response: {
  "status": "completed",
  "transcript": "...",
  "category": "promise",
  "confidence": 0.85
}
```

### 6. Массовая обработка
```http
POST /api/v1/process/bulk
Content-Type: application/json

Body: {
  "client_ids": [1, 2, 3],  // опционально
  "use_demo_audio": false
}

Response: {
  "task_id": "uuid",
  "status": "started",
  "total": 10
}
```

### 7. Статус массовой обработки
```http
GET /api/v1/process/bulk/{task_id}/status

Response: {
  "status": "processing",
  "total": 10,
  "processed": 5,
  "failed": 0,
  "progress": 50.0
}
```

### 8. Экспорт результатов
```http
GET /api/v1/export?status=completed&category=promise

Response: Excel файл (download)
```

### 9. Получить TTS аудио
```http
GET /api/v1/audio/tts/{client_id}.wav

Response: Audio file (wav)
```

## Примеры использования

### JavaScript/TypeScript

```typescript
const API_BASE = 'http://localhost:8000/api/v1';

// Загрузка файла
async function uploadExcel(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData
  });
  
  return response.json();
}

// Получить клиентов
async function getClients(page = 1, pageSize = 20) {
  const response = await fetch(
    `${API_BASE}/clients?page=${page}&page_size=${pageSize}`
  );
  return response.json();
}

// Обработать клиента
async function processClient(clientId: number) {
  const response = await fetch(
    `${API_BASE}/process/${clientId}`,
    { method: 'POST' }
  );
  return response.json();
}

// Загрузить аудио ответ
async function uploadResponse(clientId: number, audioFile: File) {
  const formData = new FormData();
  formData.append('file', audioFile);
  
  const response = await fetch(
    `${API_BASE}/process/${clientId}/response`,
    {
      method: 'POST',
      body: formData
    }
  );
  
  return response.json();
}
```

## Статусы клиентов

- `pending` - Ожидает обработки
- `processing` - В процессе обработки
- `awaiting_response` - Ожидает аудио ответ
- `completed` - Обработка завершена
- `failed` - Ошибка при обработке

## Категории ответов

- `promise` - Обещание погасить
- `refusal` - Отказ
- `question` - Вопрос
- `request_info` - Запрос информации
- `other` - Другое

## Рекомендуемый стек

- React / Vue / Angular
- Axios / Fetch API
- React Query / SWR (для кэширования)
- Material-UI / Ant Design (UI компоненты)

## Структура (пример для React)

```
frontend/
├── src/
│   ├── components/
│   │   ├── ClientList.tsx
│   │   ├── ClientCard.tsx
│   │   ├── UploadForm.tsx
│   │   └── AudioPlayer.tsx
│   ├── services/
│   │   └── api.ts
│   ├── hooks/
│   │   └── useClients.ts
│   └── App.tsx
└── package.json
```

