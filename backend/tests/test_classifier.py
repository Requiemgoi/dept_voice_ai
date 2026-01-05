"""
Unit tests для классификатора ответов должников.

Запуск:
    pytest tests/test_classifier.py -v
"""

import pytest
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Добавляем путь к ml модулю
sys.path.insert(0, str(Path(__file__).parent.parent))

from ml.classifier_engine import (
    classify_response,
    extract_date_from_text,
    get_category_description,
)


class TestClassifyResponseRussian:
    """Тесты классификации на русском языке."""
    
    def test_promise_ru(self):
        """Тест обещания оплаты на русском."""
        text = "Я заплачу завтра вечером"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'promise'
        assert 'promised_date' in meta
        assert meta['promised_date'] is not None
        assert meta['confidence'] > 0
    
    def test_promise_with_date(self):
        """Тест обещания с конкретной датой."""
        text = "Оплачу через 3 дня обязательно"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'promise'
        expected_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        assert meta['promised_date'] == expected_date
    
    def test_ignore_ru(self):
        """Тест отказа от оплаты на русском."""
        text = "Не буду платить, оставьте меня"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'ignore'
        assert 'matched_keywords' in meta
        assert len(meta['matched_keywords']) > 0
    
    def test_ignore_annoyed(self):
        """Тест раздраженного отказа."""
        text = "Надоели уже, не звоните мне больше"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'ignore'
    
    def test_help_ru(self):
        """Тест просьбы о помощи на русском."""
        text = "У меня нет денег, потерял работу"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'help'
        assert 'reason' in meta
        assert meta['reason'] is not None
    
    def test_help_with_installment_request(self):
        """Тест просьбы о рассрочке."""
        text = "Нет возможности заплатить сразу, прошу рассрочку"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'help'
        assert meta['reason'] is not None
    
    def test_wrong_number_ru(self):
        """Тест неправильного номера на русском."""
        text = "Вы ошиблись номером, я не знаю такого человека"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'wrong_number'
    
    def test_wrong_number_variant(self):
        """Тест варианта неправильного номера."""
        text = "Это не мой номер, такого здесь нет"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'wrong_number'
    
    def test_third_party_ru(self):
        """Тест третьего лица на русском."""
        text = "Это не его номер, передайте ему сообщение"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'third_party'
    
    def test_third_party_relative(self):
        """Тест родственника."""
        text = "Его нет дома, я родственник"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'third_party'
    
    def test_hangup_ru(self):
        """Тест проблем со связью на русском."""
        text = "Алло? Не слышу вас!"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'hangup'
    
    def test_hangup_short(self):
        """Тест короткого ответа."""
        text = "Что?"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'hangup'


class TestClassifyResponseKazakh:
    """Тесты классификации на казахском языке."""
    
    def test_promise_kk(self):
        """Тест обещания оплаты на казахском."""
        text = "Ертең міндетті төлеймін"
        category, meta = classify_response(text, 'kk')
        
        assert category == 'promise'
        assert 'promised_date' in meta
    
    def test_ignore_kk(self):
        """Тест отказа на казахском."""
        text = "Төлемеймін, қоңырау шалмаңыз"
        category, meta = classify_response(text, 'kk')
        
        assert category == 'ignore'
    
    def test_help_kk(self):
        """Тест просьбы о помощи на казахском."""
        text = "Ақшам жоқ, жұмыс жоғалттым"
        category, meta = classify_response(text, 'kk')
        
        assert category == 'help'
        assert meta['reason'] is not None
    
    def test_wrong_number_kk(self):
        """Тест неправильного номера на казахском."""
        text = "Қате нөмір, білмеймін"
        category, meta = classify_response(text, 'kk')
        
        assert category == 'wrong_number'
    
    def test_third_party_kk(self):
        """Тест третьего лица на казахском."""
        text = "Ол емес, туыс"
        category, meta = classify_response(text, 'kk')
        
        assert category == 'third_party'
    
    def test_hangup_kk(self):
        """Тест проблем со связью на казахском."""
        text = "Алло, естімеймін"
        category, meta = classify_response(text, 'kk')
        
        assert category == 'hangup'


class TestEdgeCases:
    """Тесты граничных случаев."""
    
    def test_empty_text(self):
        """Тест пустого текста."""
        text = ""
        category, meta = classify_response(text, 'ru')
        
        assert category == 'hangup'
        assert meta['confidence'] == 1.0
    
    def test_whitespace_only(self):
        """Тест текста только из пробелов."""
        text = "   \t\n  "
        category, meta = classify_response(text, 'ru')
        
        assert category == 'hangup'
    
    def test_no_keywords_found(self):
        """Тест текста без ключевых слов."""
        text = "Добрый день, как дела?"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'hangup'
        assert meta['confidence'] == 0.5
    
    def test_mixed_keywords(self):
        """Тест текста с ключевыми словами разных категорий."""
        text = "Я заплачу, но нет денег сейчас"
        category, meta = classify_response(text, 'ru')
        
        # При смешанных ключевых словах должна быть выбрана какая-то категория (не hangup)
        assert category != 'hangup'
        assert len(meta['matched_keywords']) > 0
    
    def test_case_insensitive(self):
        """Тест нечувствительности к регистру."""
        text = "НЕ БУДУ ПЛАТИТЬ!"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'ignore'
    
    def test_partial_match(self):
        """Тест частичного совпадения."""
        text = "Мне не интересны ваши предложения"
        category, meta = classify_response(text, 'ru')
        
        assert category == 'ignore'


class TestExtractDateFromText:
    """Тесты извлечения даты из текста."""
    
    def test_today_ru(self):
        """Тест 'сегодня'."""
        text = "Заплачу сегодня"
        date = extract_date_from_text(text, 'ru')
        
        expected = datetime.now().strftime('%Y-%m-%d')
        assert date == expected
    
    def test_tomorrow_ru(self):
        """Тест 'завтра'."""
        text = "Оплачу завтра"
        date = extract_date_from_text(text, 'ru')
        
        expected = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        assert date == expected
    
    def test_in_n_days_ru(self):
        """Тест 'через N дней'."""
        text = "Переведу через 5 дней"
        date = extract_date_from_text(text, 'ru')
        
        expected = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        assert date == expected
    
    def test_in_week_ru(self):
        """Тест 'через неделю'."""
        text = "Заплачу через неделю"
        date = extract_date_from_text(text, 'ru')
        
        expected = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        assert date == expected
    
    def test_today_kk(self):
        """Тест 'бүгін' (сегодня по-казахски)."""
        text = "Бүгін төлеймін"
        date = extract_date_from_text(text, 'kk')
        
        expected = datetime.now().strftime('%Y-%m-%d')
        assert date == expected
    
    def test_tomorrow_kk(self):
        """Тест 'ертең' (завтра по-казахски)."""
        text = "Ертең аударамын"
        date = extract_date_from_text(text, 'kk')
        
        expected = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        assert date == expected
    
    def test_no_date(self):
        """Тест текста без даты."""
        text = "Когда-нибудь заплачу"
        date = extract_date_from_text(text, 'ru')
        
        assert date is None
    
    def test_empty_text(self):
        """Тест пустого текста."""
        date = extract_date_from_text("", 'ru')
        assert date is None
        
        date = extract_date_from_text(None, 'ru')
        assert date is None


class TestCategoryDescription:
    """Тесты описаний категорий."""
    
    def test_descriptions_ru(self):
        """Тест описаний на русском."""
        assert get_category_description('promise', 'ru') == 'Обещание оплаты'
        assert get_category_description('ignore', 'ru') == 'Отказ от оплаты'
        assert get_category_description('help', 'ru') == 'Просьба о помощи'
    
    def test_descriptions_kk(self):
        """Тест описаний на казахском."""
        assert get_category_description('promise', 'kk') == 'Төлеу уәдесі'
        assert get_category_description('ignore', 'kk') == 'Төлемнен бас тарту'


class TestMetadata:
    """Тесты метаданных классификации."""
    
    def test_metadata_structure(self):
        """Тест структуры метаданных."""
        text = "Заплачу завтра"
        category, meta = classify_response(text, 'ru')
        
        assert 'confidence' in meta
        assert 'matched_keywords' in meta
        assert 'promised_date' in meta
        assert 'reason' in meta
        
        assert isinstance(meta['confidence'], float)
        assert isinstance(meta['matched_keywords'], list)
    
    def test_confidence_range(self):
        """Тест диапазона уверенности."""
        text = "Заплачу завтра обязательно скоро"
        category, meta = classify_response(text, 'ru')
        
        assert 0.0 <= meta['confidence'] <= 1.0
    
    def test_matched_keywords_not_empty(self):
        """Тест что matched_keywords не пуст при совпадении."""
        text = "Не буду платить, надоели"
        category, meta = classify_response(text, 'ru')
        
        assert len(meta['matched_keywords']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
