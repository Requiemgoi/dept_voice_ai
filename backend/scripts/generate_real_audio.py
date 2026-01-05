#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для генерации РЕАЛЬНЫХ демонстрационных WAV файлов через pyttsx3.

Использует pyttsx3 для Windows (работает offline без дополнительных зависимостей).

Требования:
    pip install pyttsx3 pydub

Использование:
    python generate_real_audio.py
"""

import sys
import wave
import struct
from pathlib import Path
from typing import Optional

print("=== Real Audio Generator ===")
print("Loading libraries...")

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False
    print("[WARNING] pyttsx3 not installed!")

try:
    from pydub import AudioSegment
    HAS_PYDUB = True
except ImportError:
    HAS_PYDUB = False
    print("[WARNING] pydub not installed, will skip conversion")

# Пути для сохранения
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
TEST_AUDIO_DIR = PROJECT_ROOT / "ml" / "test_audio"
PUBLIC_DEMO_DIR = PROJECT_ROOT.parent / "public" / "demo-audio"

# Сценарии для генерации аудио
SCENARIOS = {
    # Русские сценарии
    'ignore_ru': {
        'text': "Не буду платить, оставьте меня в покое!",
        'lang': 'ru'
    },
    'promise_ru': {
        'text': "Я заплачу завтра вечером, обязательно",
        'lang': 'ru'
    },
    'help_ru': {
        'text': "У меня нет денег, потерял работу, прошу рассрочку",
        'lang': 'ru'
    },
    'wrong_number_ru': {
        'text': "Вы ошиблись номером, я не знаю такого человека",
        'lang': 'ru'
    },
    'third_party_ru': {
        'text': "Это не его номер, передайте ему сообщение",
        'lang': 'ru'
    },
    'hangup_ru': {
        'text': "Алло? Не слышу вас!",
        'lang': 'ru'
    },
    # Казахские сценарии (используем русский TTS)
    'ignore_kk': {
        'text': "Төлемеймін, қоңырау шалмаңыз!",
        'lang': 'ru'  # Fallback to Russian voice
    },
    'promise_kk': {
        'text': "Ертең міндетті төлеймін",
        'lang': 'ru'
    },
    'help_kk': {
        'text': "Ақшам жоқ, жұмыс жоғалттым",
        'lang': 'ru'
    },
    'wrong_number_kk': {
        'text': "Қате нөмір, білмеймін кім бұл",
        'lang': 'ru'
    },
    'third_party_kk': {
        'text': "Ол емес, жеткізіңіз хабарды",
        'lang': 'ru'
    },
    'hangup_kk': {
        'text': "Алло? Естімеймін сізді!",
        'lang': 'ru'
    },
}


def generate_with_pyttsx3(text: str, output_path: Path, rate: int = 150) -> bool:
    """
    Генерирует WAV файл с помощью pyttsx3.
    
    Args:
        text: Текст для синтеза
        output_path: Путь для сохранения WAV файла
        rate: Скорость речи
        
    Returns:
        True если успешно, False иначе
    """
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Создаем временный файл
        temp_path = output_path.with_suffix('.temp.wav')
        
        # Инициализируем движок
        engine = pyttsx3.init()
        
        # Настройки
        engine.setProperty('rate', rate)
        
        # Пробуем найти русский голос
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'ru' in voice.id.lower() or 'russian' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        # Генерируем аудио
        engine.save_to_file(text, str(temp_path))
        engine.runAndWait()
        
        # Конвертируем в 16kHz mono если доступен pydub
        if HAS_PYDUB and temp_path.exists():
            audio = AudioSegment.from_wav(str(temp_path))
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(str(output_path), format='wav')
            temp_path.unlink(missing_ok=True)
            return True
        elif temp_path.exists():
            # Без pydub - просто переименуем
            temp_path.rename(output_path)
            print(f"  [WARNING] Audio not converted to 16kHz mono (install pydub)")
            return True
            
        return False
        
    except Exception as e:
        print(f"  [ERROR] pyttsx3 generation failed: {e}")
        return False


def generate_silent_wav(output_path: Path, duration_ms: int = 1000) -> bool:
    """
    Генерирует тихий WAV файл (placeholder).
    """
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        sample_rate = 16000
        num_samples = int(sample_rate * duration_ms / 1000)
        
        with wave.open(str(output_path), 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            # Генерируем тишину
            silence = struct.pack('<' + 'h' * num_samples, *([0] * num_samples))
            wav_file.writeframes(silence)
        
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to generate silent WAV: {e}")
        return False


def main():
    """Основная функция генерации демо-аудио."""
    print(f"Test audio dir: {TEST_AUDIO_DIR}")
    print(f"Public demo dir: {PUBLIC_DEMO_DIR}")
    print("")
    
    # Проверяем pyttsx3
    if HAS_PYTTSX3:
        print("[OK] pyttsx3 found - will generate real audio")
    else:
        print("[WARNING] pyttsx3 not found!")
        print("         Install: pip install pyttsx3 pydub")
        print("")
        
        response = input("Generate silent placeholder files instead? [y/N]: ")
        if response.lower() != 'y':
            print("Installation command:")
            print("  pip install pyttsx3 pydub")
            return 1
    
    print("")
    
    # Создаем директории
    TEST_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_DEMO_DIR.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_count = len(SCENARIOS)
    
    for scenario_name, config in SCENARIOS.items():
        print(f"Generating: {scenario_name}")
        text_preview = config['text'][:50]
        print(f"  Text: {text_preview}...")
        
        # Пути для сохранения
        test_path = TEST_AUDIO_DIR / f"{scenario_name}.wav"
        public_path = PUBLIC_DEMO_DIR / f"{scenario_name}.wav"
        
        if HAS_PYTTSX3:
            success = generate_with_pyttsx3(
                text=config['text'],
                output_path=test_path
            )
        else:
            success = generate_silent_wav(test_path)
        
        if success:
            print(f"  [OK] {test_path}")
            success_count += 1
            
            # Копируем в public директорию
            try:
                import shutil
                shutil.copy2(test_path, public_path)
                print(f"  [OK] {public_path}")
            except Exception as e:
                print(f"  [WARNING] Could not copy to public: {e}")
        else:
            print(f"  [FAILED] {test_path}")
        
        print("")
    
    print(f"=== Generation Complete: {success_count}/{total_count} files ===")
    
    if not HAS_PYTTSX3:
        print("")
        print("NOTE: Generated placeholder files. Install pyttsx3 for real audio:")
        print("  pip install pyttsx3 pydub")
    
    return 0 if success_count == total_count else 1


if __name__ == '__main__':
    sys.exit(main())
