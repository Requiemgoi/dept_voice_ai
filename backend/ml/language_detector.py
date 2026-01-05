"""
Модуль определения языка текста (русский/казахский).

Использует специфичные казахские буквы и ключевые слова для определения языка.
"""

from typing import Literal

# Казахские буквы, отсутствующие в русском алфавите
KAZAKH_SPECIFIC_LETTERS = set('әғқңөұүһі')

# Ключевые слова для определения языка
KAZAKH_KEYWORDS = [
    'керек', 'емес', 'жоқ', 'қажет', 'болады', 'бар', 'мен', 'сен', 
    'төлеймін', 'аударамын', 'ертең', 'бүгін', 'апта', 'міндетті',
    'мүмкіндігім', 'ақша', 'қиын', 'жұмыс', 'көмектесіңіз',
    'басқа', 'адам', 'қате', 'нөмір', 'білмеймін', 'кім',
    'жеткізіңіз', 'туыс', 'алло', 'естімеймін', 'не',
    'қоңырау', 'шалмаңыз', 'артық'
]

RUSSIAN_KEYWORDS = [
    'не', 'буду', 'платить', 'заплачу', 'оплачу', 'завтра', 'сегодня',
    'через', 'дней', 'неделю', 'денег', 'работу', 'рассрочка',
    'ошиблись', 'номером', 'знаю', 'передайте', 'алло', 'слышу',
    'оставьте', 'звоните', 'интересует', 'хочу', 'могу', 'нет'
]


def detect_language(text: str) -> Literal['ru', 'kk', 'unknown']:
    """
    Определяет язык текста (русский или казахский).
    
    Args:
        text: Входной текст для анализа
        
    Returns:
        'ru' - русский язык
        'kk' - казахский язык  
        'unknown' - не удалось определить
    """
    if not text or not text.strip():
        return 'unknown'
    
    text_lower = text.lower()
    
    # Подсчет казахских специфичных букв
    kazakh_letter_count = sum(1 for char in text_lower if char in KAZAKH_SPECIFIC_LETTERS)
    
    # Если есть казахские специфичные буквы - это казахский
    if kazakh_letter_count > 0:
        return 'kk'
    
    # Подсчет ключевых слов
    kk_score = 0
    ru_score = 0
    
    words = text_lower.split()
    
    for word in words:
        # Очищаем слово от пунктуации
        clean_word = ''.join(c for c in word if c.isalpha())
        
        if any(kw in clean_word or clean_word in kw for kw in KAZAKH_KEYWORDS):
            kk_score += 1
            
        if any(kw in clean_word or clean_word in kw for kw in RUSSIAN_KEYWORDS):
            ru_score += 1
    
    # Определяем язык по большему score
    if kk_score > ru_score:
        return 'kk'
    elif ru_score > kk_score:
        return 'ru'
    elif ru_score > 0:
        # При равном счете, если есть русские слова - считаем русским
        return 'ru'
    
    return 'unknown'


def get_language_confidence(text: str) -> tuple[str, float]:
    """
    Определяет язык и уверенность в определении.
    
    Args:
        text: Входной текст
        
    Returns:
        Кортеж (язык, уверенность от 0.0 до 1.0)
    """
    if not text or not text.strip():
        return 'unknown', 0.0
    
    text_lower = text.lower()
    
    # Казахские буквы дают высокую уверенность
    kazakh_letter_count = sum(1 for char in text_lower if char in KAZAKH_SPECIFIC_LETTERS)
    if kazakh_letter_count > 0:
        confidence = min(0.5 + kazakh_letter_count * 0.1, 1.0)
        return 'kk', confidence
    
    # Подсчет ключевых слов
    words = text_lower.split()
    total_words = len(words)
    
    if total_words == 0:
        return 'unknown', 0.0
    
    kk_matches = 0
    ru_matches = 0
    
    for word in words:
        clean_word = ''.join(c for c in word if c.isalpha())
        if any(kw in clean_word or clean_word in kw for kw in KAZAKH_KEYWORDS):
            kk_matches += 1
        if any(kw in clean_word or clean_word in kw for kw in RUSSIAN_KEYWORDS):
            ru_matches += 1
    
    if kk_matches > ru_matches:
        confidence = min(0.5 + (kk_matches / total_words) * 0.5, 1.0)
        return 'kk', confidence
    elif ru_matches > kk_matches:
        confidence = min(0.5 + (ru_matches / total_words) * 0.5, 1.0)
        return 'ru', confidence
    elif ru_matches > 0:
        return 'ru', 0.5
    
    return 'unknown', 0.0
