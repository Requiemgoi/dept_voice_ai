#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интерактивный тестер STT и классификатора.
Записывает ваш голос с микрофона, распознает речь и классифицирует ответ.

Требования:
    pip install sounddevice scipy

Использование:
    python test_voice_live.py
"""

import sys
import wave
import struct
from pathlib import Path
from datetime import datetime

print("=" * 60)
print("🎤 ИНТЕРАКТИВНЫЙ ТЕСТЕР STT И КЛАССИФИКАТОРА")
print("=" * 60)
print()

# Добавляем путь к ml модулю
sys.path.insert(0, str(Path(__file__).parent.parent))

# Проверяем зависимости
try:
    import sounddevice as sd
    import numpy as np
    from scipy.io import wavfile
    HAS_RECORDING = True
except ImportError:
    HAS_RECORDING = False
    print("❌ ОШИБКА: Библиотеки для записи не установлены!")
    print("   Установите: pip install sounddevice scipy")
    print()
    sys.exit(1)

# Импортируем ML модули
try:
    from ml import recognize_audio, classify_response, detect_language
    from ml.stt_engine import stt_engine
except ImportError as e:
    print(f"❌ ОШИБКА: Не удалось загрузить ML модули: {e}")
    sys.exit(1)

# Параметры записи
SAMPLE_RATE = 16000  # Hz
CHANNELS = 1  # Mono
DURATION = 5  # секунд
RECORDINGS_DIR = Path(__file__).parent.parent / "ml" / "recordings"

def record_audio(duration: int = DURATION) -> np.ndarray:
    """Записывает аудио с микрофона."""
    print(f"🎙️  Запись {duration} секунд...")
    print("   Говорите СЕЙЧАС!")
    print()
    
    try:
        # Записываем
        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int16'
        )
        sd.wait()  # Ждем окончания записи
        
        print("✓ Запись завершена!")
        return audio
        
    except Exception as e:
        print(f"❌ Ошибка записи: {e}")
        return None

def save_wav(audio: np.ndarray, filename: str) -> Path:
    """Сохраняет аудио в WAV файл."""
    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = RECORDINGS_DIR / f"{timestamp}_{filename}.wav"
    
    wavfile.write(str(filepath), SAMPLE_RATE, audio)
    
    return filepath

def test_microphone():
    """Тестирует микрофон."""
    print("🔧 Проверка микрофона...")
    try:
        devices = sd.query_devices()
        default_input = sd.query_devices(kind='input')
        print(f"✓ Микрофон найден: {default_input['name']}")
        return True
    except Exception as e:
        print(f"❌ Ошибка микрофона: {e}")
        return False

def main():
    """Основная функция."""
    
    # Проверяем микрофон
    if not test_microphone():
        return 1
    
    print()
    print("=" * 60)
    
    # Проверяем доступность моделей
    available_langs = stt_engine.get_available_languages()
    if not available_langs:
        print("❌ ОШИБКА: Модели Vosk не найдены!")
        print("   Запустите: bash scripts/download_models.sh")
        return 1
    
    print(f"✓ Модели загружены: {', '.join(available_langs)}")
    print()
    print("=" * 60)
    print()
    
    while True:
        print("Выберите действие:")
        print("  1 - Записать голос и протестировать (Русский)")
        print("  2 - Записать голос и протестировать (Казахский)")
        print("  3 - Записать голос с автоопределением языка")
        print("  4 - Изменить длительность записи")
        print("  0 - Выход")
        print()
        
        choice = input("Ваш выбор: ").strip()
        print()
        
        if choice == '0':
            print("👋 До свидания!")
            break
            
        elif choice == '4':
            try:
                new_duration = int(input("Введите длительность (секунды): "))
                if 1 <= new_duration <= 30:
                    global DURATION
                    DURATION = new_duration
                    print(f"✓ Длительность установлена: {DURATION} сек")
                else:
                    print("⚠️  Используйте значение от 1 до 30")
            except ValueError:
                print("❌ Неверное значение")
            print()
            continue
            
        elif choice in ['1', '2', '3']:
            # Определяем язык
            if choice == '1':
                lang = 'ru'
                print("🇷🇺 Режим: Русский язык")
            elif choice == '2':
                lang = 'kk'
                print("🇰🇿 Режим: Казахский язык")
            else:
                lang = 'auto'
                print("🌐 Режим: Автоопределение языка")
            
            print()
            
            # Записываем
            audio = record_audio(DURATION)
            
            if audio is None:
                continue
            
            # Сохраняем
            wav_path = save_wav(audio, "test")
            print(f"💾 Сохранено: {wav_path.name}")
            print()
            
            # Распознаем
            print("🔍 Распознавание речи...")
            try:
                if lang == 'auto':
                    text, detected_lang = stt_engine.recognize_auto_detect(str(wav_path))
                    print(f"✓ Определен язык: {detected_lang.upper()}")
                    lang = detected_lang
                else:
                    text, _ = recognize_audio(str(wav_path), lang)
                
                print()
                print("=" * 60)
                print("📝 РЕЗУЛЬТАТ РАСПОЗНАВАНИЯ:")
                print(f"   {text}")
                print("=" * 60)
                print()
                
                if not text or not text.strip():
                    print("⚠️  Речь не распознана. Попробуйте:")
                    print("   - Говорить громче")
                    print("   - Ближе к микрофону")
                    print("   - Проверить работу микрофона")
                    print()
                    continue
                
                # Классифицируем
                print("🏷️  Классификация ответа...")
                category, metadata = classify_response(text, lang)
                
                print()
                print("=" * 60)
                print("📊 РЕЗУЛЬТАТ КЛАССИФИКАЦИИ:")
                print(f"   Категория: {category.upper()}")
                print(f"   Уверенность: {metadata['confidence']:.0%}")
                
                if metadata['matched_keywords']:
                    print(f"   Ключевые слова: {', '.join(metadata['matched_keywords'])}")
                
                if category == 'promise' and metadata.get('promised_date'):
                    print(f"   📅 Обещанная дата: {metadata['promised_date']}")
                
                if category == 'help' and metadata.get('reason'):
                    print(f"   📋 Причина: {metadata['reason']}")
                
                print("=" * 60)
                print()
                
                # Интерпретация
                interpretations = {
                    'ignore': '❌ Должник отказывается платить',
                    'promise': '✅ Должник обещает оплатить',
                    'help': '🆘 Должник просит помощь/рассрочку',
                    'wrong_number': '☎️  Неправильный номер',
                    'third_party': '👤 Третье лицо',
                    'hangup': '📞 Проблемы со связью / неясно'
                }
                
                print(f"💡 {interpretations.get(category, category)}")
                print()
                
            except Exception as e:
                print(f"❌ Ошибка обработки: {e}")
                import traceback
                traceback.print_exc()
                print()
            
        else:
            print("❌ Неверный выбор")
            print()
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        print("👋 Прервано пользователем")
        sys.exit(0)
