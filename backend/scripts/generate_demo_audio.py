#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для генерации демонстрационных WAV файлов через espeak-ng.

Генерирует аудио файлы для тестирования STT и классификатора.

Требования:
    - espeak-ng должен быть установлен в системе
    - Для Windows: установить через chocolatey или скачать с github
    - Для Linux: sudo apt install espeak-ng
    - Для macOS: brew install espeak-ng

Использование:
    python generate_demo_audio.py
"""

# Fix Windows console encoding for Unicode
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
import subprocess
import sys
from pathlib import Path

# Сценарии для генерации аудио
SCENARIOS = {
    # Русские сценарии
    'ignore_ru': {
        'text': "Не буду платить, оставьте меня в покое!",
        'lang': 'ru',
        'voice': 'ru'
    },
    'promise_ru': {
        'text': "Я заплачу завтра вечером, обязательно",
        'lang': 'ru',
        'voice': 'ru'
    },
    'help_ru': {
        'text': "У меня нет денег, потерял работу, прошу рассрочку",
        'lang': 'ru',
        'voice': 'ru'
    },
    'wrong_number_ru': {
        'text': "Вы ошиблись номером, я не знаю такого человека",
        'lang': 'ru',
        'voice': 'ru'
    },
    'third_party_ru': {
        'text': "Это не его номер, передайте ему сообщение",
        'lang': 'ru',
        'voice': 'ru'
    },
    'hangup_ru': {
        'text': "Алло? Не слышу вас!",
        'lang': 'ru',
        'voice': 'ru'
    },
    # Казахские сценарии
    'ignore_kk': {
        'text': "Төлемеймін, қоңырау шалмаңыз!",
        'lang': 'kk',
        'voice': 'ru'  # Используем русский голос как fallback
    },
    'promise_kk': {
        'text': "Ертең міндетті төлеймін",
        'lang': 'kk',
        'voice': 'ru'
    },
    'help_kk': {
        'text': "Ақшам жоқ, жұмыс жоғалттым",
        'lang': 'kk',
        'voice': 'ru'
    },
    'wrong_number_kk': {
        'text': "Қате нөмір, білмеймін кім бұл",
        'lang': 'kk',
        'voice': 'ru'
    },
    'third_party_kk': {
        'text': "Ол емес, жеткізіңіз хабарды",
        'lang': 'kk',
        'voice': 'ru'
    },
    'hangup_kk': {
        'text': "Алло? Естімеймін сізді!",
        'lang': 'kk',
        'voice': 'ru'
    },
}

# Пути для сохранения
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
TEST_AUDIO_DIR = PROJECT_ROOT / "ml" / "test_audio"
PUBLIC_DEMO_DIR = PROJECT_ROOT.parent / "public" / "demo-audio"


def check_espeak_ng() -> bool:
    """Проверяет наличие espeak-ng в системе."""
    try:
        result = subprocess.run(
            ['espeak-ng', '--version'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def generate_wav(text: str, output_path: Path, voice: str = 'ru', rate: int = 150) -> bool:
    """
    Генерирует WAV файл с помощью espeak-ng.
    
    Args:
        text: Текст для синтеза
        output_path: Путь для сохранения WAV файла
        voice: Голос/язык для espeak-ng
        rate: Скорость речи (слов в минуту)
        
    Returns:
        True если успешно, False иначе
    """
    try:
        # Создаем директорию если не существует
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Генерируем временный файл с более высоким sample rate
        temp_path = output_path.with_suffix('.temp.wav')
        
        # espeak-ng команда
        cmd = [
            'espeak-ng',
            '-v', voice,
            '-s', str(rate),
            '-w', str(temp_path),
            text
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"  [ERROR] espeak-ng failed: {result.stderr}")
            return False
        
        # Конвертируем в 16kHz mono с помощью ffmpeg или sox если доступны
        if convert_audio(temp_path, output_path):
            temp_path.unlink(missing_ok=True)
            return True
        else:
            # Если конвертация не удалась, используем как есть
            temp_path.rename(output_path)
            return True
            
    except Exception as e:
        print(f"  [ERROR] Failed to generate audio: {e}")
        return False


def convert_audio(input_path: Path, output_path: Path) -> bool:
    """
    Конвертирует аудио в 16kHz mono WAV.
    
    Пробует использовать ffmpeg или sox.
    """
    # Пробуем ffmpeg
    try:
        cmd = [
            'ffmpeg', '-y', '-i', str(input_path),
            '-ar', '16000',
            '-ac', '1',
            '-acodec', 'pcm_s16le',
            str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    
    # Пробуем sox
    try:
        cmd = [
            'sox', str(input_path),
            '-r', '16000',
            '-c', '1',
            '-b', '16',
            str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    
    return False


def generate_silent_wav(output_path: Path, duration_ms: int = 1000) -> bool:
    """
    Генерирует тихий WAV файл (placeholder).
    
    Используется когда espeak-ng недоступен.
    """
    import struct
    import wave
    
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        sample_rate = 16000
        num_samples = int(sample_rate * duration_ms / 1000)
        
        with wave.open(str(output_path), 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            # Генерируем тишину (нули)
            silence = struct.pack('<' + 'h' * num_samples, *([0] * num_samples))
            wav_file.writeframes(silence)
        
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to generate silent WAV: {e}")
        return False


def main():
    """Основная функция генерации демо-аудио."""
    print("=== Demo Audio Generator ===")
    print(f"Test audio dir: {TEST_AUDIO_DIR}")
    print(f"Public demo dir: {PUBLIC_DEMO_DIR}")
    print("")
    
    # Проверяем espeak-ng
    has_espeak = check_espeak_ng()
    if has_espeak:
        print("[OK] espeak-ng found")
    else:
        print("[WARNING] espeak-ng not found!")
        print("         Installing: ")
        print("         - Linux: sudo apt install espeak-ng")
        print("         - macOS: brew install espeak-ng")
        print("         - Windows: choco install espeak-ng")
        print("")
        print("         Generating placeholder (silent) WAV files instead...")
    
    print("")
    
    # Создаем директории
    TEST_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_DEMO_DIR.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_count = len(SCENARIOS)
    
    for scenario_name, config in SCENARIOS.items():
        print(f"Generating: {scenario_name}")
        # Safely print text (truncate and handle encoding)
        text_preview = config['text'][:40]
        try:
            print(f"  Text: {text_preview}...")
        except UnicodeEncodeError:
            print(f"  Text: [Unicode text for {config['lang']}]")
        
        # Пути для сохранения
        test_path = TEST_AUDIO_DIR / f"{scenario_name}.wav"
        public_path = PUBLIC_DEMO_DIR / f"{scenario_name}.wav"
        
        if has_espeak:
            success = generate_wav(
                text=config['text'],
                output_path=test_path,
                voice=config['voice']
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
    
    if not has_espeak:
        print("")
        print("NOTE: Generated placeholder files. Install espeak-ng for real audio.")
    
    return 0 if success_count == total_count else 1


if __name__ == '__main__':
    sys.exit(main())
