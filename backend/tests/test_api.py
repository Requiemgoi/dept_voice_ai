"""
Unit tests для API endpoints.

Запуск:
    pytest tests/test_api.py -v
"""

import pytest
import sys
from pathlib import Path

# Добавляем путь к backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRootEndpoint:
    """Тесты корневого endpoint."""
    
    def test_root_returns_service_info(self):
        """Тест корневого endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["service"] == "Voice AI API"
        assert data["version"] == "1.0.0"
        assert "endpoints" in data


class TestHealthEndpoint:
    """Тесты endpoint проверки здоровья."""
    
    def test_health_check(self):
        """Тест health check."""
        response = client.get("/api/voice/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] in ["healthy", "degraded", "unhealthy"]
        assert "models" in data
        assert "available_languages" in data
        assert "timestamp" in data
    
    def test_health_models_structure(self):
        """Тест структуры информации о моделях."""
        response = client.get("/api/voice/health")
        data = response.json()
        
        assert "ru" in data["models"]
        assert "kk" in data["models"]
        assert isinstance(data["models"]["ru"], bool)
        assert isinstance(data["models"]["kk"], bool)


class TestClassifyEndpoint:
    """Тесты endpoint классификации текста."""
    
    def test_classify_promise_ru(self):
        """Тест классификации обещания на русском."""
        response = client.post(
            "/api/voice/classify",
            json={"text": "Я заплачу завтра", "language": "ru"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["classification"]["category"] == "promise"
        assert data["classification"]["promised_date"] is not None
    
    def test_classify_ignore_ru(self):
        """Тест классификации отказа на русском."""
        response = client.post(
            "/api/voice/classify",
            json={"text": "Не буду платить, оставьте меня", "language": "ru"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["classification"]["category"] == "ignore"
    
    def test_classify_help_ru(self):
        """Тест классификации просьбы о помощи."""
        response = client.post(
            "/api/voice/classify",
            json={"text": "Нет денег, потерял работу", "language": "ru"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["classification"]["category"] == "help"
        assert data["classification"]["reason"] is not None
    
    def test_classify_auto_language(self):
        """Тест автоопределения языка."""
        response = client.post(
            "/api/voice/classify",
            json={"text": "Заплачу завтра обязательно", "language": "auto"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["detected_language"] == "ru"
    
    def test_classify_kazakh(self):
        """Тест классификации на казахском."""
        response = client.post(
            "/api/voice/classify",
            json={"text": "Ертең төлеймін", "language": "kk"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["classification"]["category"] == "promise"
    
    def test_classify_empty_text_error(self):
        """Тест ошибки при пустом тексте."""
        response = client.post(
            "/api/voice/classify",
            json={"text": "", "language": "ru"}
        )
        
        # Pydantic validation error
        assert response.status_code == 422
    
    def test_classify_response_structure(self):
        """Тест структуры ответа классификации."""
        response = client.post(
            "/api/voice/classify",
            json={"text": "Тестовый текст", "language": "ru"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "success" in data
        assert "request_id" in data
        assert "timestamp" in data
        assert "text" in data
        assert "detected_language" in data
        assert "classification" in data
        
        classification = data["classification"]
        assert "category" in classification
        assert "category_description" in classification
        assert "confidence" in classification
        assert "matched_keywords" in classification


class TestLanguagesEndpoint:
    """Тесты endpoint списка языков."""
    
    def test_get_languages(self):
        """Тест получения списка языков."""
        response = client.get("/api/voice/languages")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "languages" in data
        assert len(data["languages"]) == 2
        
        codes = [lang["code"] for lang in data["languages"]]
        assert "ru" in codes
        assert "kk" in codes
    
    def test_languages_structure(self):
        """Тест структуры информации о языках."""
        response = client.get("/api/voice/languages")
        data = response.json()
        
        for lang in data["languages"]:
            assert "code" in lang
            assert "name" in lang
            assert "available" in lang


class TestCategoriesEndpoint:
    """Тесты endpoint списка категорий."""
    
    def test_get_categories_ru(self):
        """Тест получения категорий на русском."""
        response = client.get("/api/voice/categories?language=ru")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "categories" in data
        assert len(data["categories"]) == 6
        
        codes = [cat["code"] for cat in data["categories"]]
        assert "promise" in codes
        assert "ignore" in codes
        assert "help" in codes
        assert "wrong_number" in codes
        assert "third_party" in codes
        assert "hangup" in codes
    
    def test_get_categories_kk(self):
        """Тест получения категорий на казахском."""
        response = client.get("/api/voice/categories?language=kk")
        
        assert response.status_code == 200
        data = response.json()
        
        # Проверяем что описания на казахском
        promise_cat = next(c for c in data["categories"] if c["code"] == "promise")
        assert "Төлеу" in promise_cat["description"]


class TestProcessVoiceEndpoint:
    """Тесты endpoint обработки голоса."""
    
    def test_process_voice_invalid_file_type(self):
        """Тест ошибки при неверном типе файла."""
        response = client.post(
            "/api/voice/process",
            files={"audio": ("test.mp3", b"fake audio content", "audio/mpeg")},
            data={"language": "ru"}
        )
        
        assert response.status_code == 400
    
    def test_process_voice_requires_file(self):
        """Тест требования файла."""
        response = client.post(
            "/api/voice/process",
            data={"language": "ru"}
        )
        
        assert response.status_code == 422  # Validation error


class TestErrorHandling:
    """Тесты обработки ошибок."""
    
    def test_404_not_found(self):
        """Тест 404 для несуществующего endpoint."""
        response = client.get("/api/voice/nonexistent")
        
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        """Тест 405 для неверного метода."""
        response = client.get("/api/voice/classify")
        
        assert response.status_code == 405


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
