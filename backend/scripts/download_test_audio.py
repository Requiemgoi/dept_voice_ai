#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для генерации простых тестовых WAV файлов с записанным текстом.
Использует gTTS (Google Text-to-Speech) - работает через интернет.

Требования:
    pip install gtts

Использование:
    python download_test_audio.py
"""

import sys
from pathlib import Path

print("=== Google TTS Audio Generator ===")

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False
    print("[ERROR] gTTS not installed!")
    print("Install: pip install gtts")
    sys.exit(1)

try:
    from pydub import AudioSegment
    HAS_PYDUB = True
except ImportError:
    HAS_PYDUB = False
    print("[WARNING] pydub not installed, audio conversion may fail")

# Пути
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
TEST_AUDIO_DIR = PROJECT_ROOT / "ml" / "test_audio"
PUBLIC_DEMO_DIR = PROJECT_ROOT.parent / "public" / "demo-audio"

# Сценарии
SCENARIOS = {
    'ignore_ru': "Не буду платить, оставьте меня в покое!",
    'promise_ru': "Я заплачу завтра вечером, обязательно",
    'help_ru': "У меня нет денег, потерял работу, прошу рассрочку",
    'wrong_number_ru': "Вы ошиблись номером, я не знаю такого человека",
    'third_party_ru': "Это не его номер, передайте ему сообщение",
    'hangup_ru': "Алло? Не слышу вас!",
    'ignore_kk': "Төлемеймін, қоңырау шалмаңыз!",
    'promise_kk': "Ертең міндетті төлеймін",
    'help_kk': "Ақшам жоқ, жұмыс жоғалттым",
    'wrong_number_kk': "Қате нөмір, білмеймін",
    'third_party_kk': "Ол емес, жеткізіңіз",
    'hangup_kk': "Алло? Естімеймін!",
}

def generate_audio(text: str, output_path: Path, lang: str = 'ru') -> bool:
    """Генерирует WAV через gTTS."""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Генерируем MP3 через gTTS
        temp_mp3 = output_path.with_suffix('.temp.mp3')
        
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(str(temp_mp3))
        
        # Конвертируем в WAV 16kHz mono
        if HAS_PYDUB:
            audio = AudioSegment.from_mp3(str(temp_mp3))
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(str(output_path), format='wav')
            temp_mp3.unlink(missing_ok=True)
            return True
        else:
            print(f"  [WARNING] pydub not available, keeping MP3")
            temp_mp3.rename(output_path.with_suffix('.mp3'))
            return False
            
    except Exception as e:
        print(f"  [ERROR] Failed: {e}")
        return False

def main():
    print(f"Output dirs:")
    print(f"  - {TEST_AUDIO_DIR}")
    print(f"  - {PUBLIC_DEMO_DIR}")
    print("")
    
    TEST_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_DEMO_DIR.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    
    for name, text in SCENARIOS.items():
        lang = 'ru' if 'ru' in name else 'ru'  # gTTS doesn't support Kazakh well
        
        print(f"[{name}] Generating...")
        
        test_path = TEST_AUDIO_DIR / f"{name}.wav"
        public_path = PUBLIC_DEMO_DIR / f"{name}.wav"
        
        if generate_audio(text, test_path, lang):
            print(f"  ✓ {test_path.name}")
            success_count += 1
            
            # Копируем
            import shutil
            shutil.copy2(test_path, public_path)
            print(f"  ✓ {public_path.name}")
        else:
            print(f"  ✗ Failed")
    
    print(f"\n=== Done: {success_count}/{len(SCENARIOS)} ===")
    return 0 if success_count == len(SCENARIOS) else 1

if __name__ == '__main__':
    sys.exit(main())
