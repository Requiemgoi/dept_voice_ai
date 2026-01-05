"""
Простой генератор реальных аудио через gTTS.
Запустите: python simple_audio_gen.py
"""
import os
import sys
from pathlib import Path

# Добавляем пути
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    try:
        from gtts import gTTS
        from pydub import AudioSegment
        
        print("Starting audio generation...")
        
        # Пути
        test_dir = Path(__file__).parent.parent / "ml" / "test_audio"
        public_dir = Path(__file__).parent.parent.parent / "public" / "demo-audio"
        
        test_dir.mkdir(parents=True, exist_ok=True)
        public_dir.mkdir(parents=True, exist_ok=True)
        
        # Сценарии
        scenarios = {
            'ignore_ru': "Не буду платить, оставьте меня в покое!",
            'promise_ru': "Я заплачу завтра вечером, обязательно",
            'help_ru': "У меня нет денег, потерял работу, прошу рассрочку",
            'wrong_number_ru': "Вы ошиблись номером, я не знаю такого человека",
            'third_party_ru': "Это не его номер, передайте ему сообщение",
            'hangup_ru': "Алло? Не слышу вас!",
        }
        
        count = 0
        for name, text in scenarios.items():
            try:
                print(f"Generating {name}...")
                
                # MP3
                mp3_path = test_dir / f"{name}.mp3"
                tts = gTTS(text=text, lang='ru', slow=False)
                tts.save(str(mp3_path))
                
                # Convert to WAV 16kHz mono
                wav_path = test_dir / f"{name}.wav"
                audio = AudioSegment.from_mp3(str(mp3_path))
                audio = audio.set_frame_rate(16000).set_channels(1)
                audio.export(str(wav_path), format='wav')
                
                # Copy to public
                import shutil
                shutil.copy2(wav_path, public_dir / f"{name}.wav")
                
                # Cleanup
                mp3_path.unlink(missing_ok=True)
                
                print(f"  OK: {name}.wav")
                count += 1
                
            except Exception as e:
                print(f"  ERROR {name}: {e}")
        
        print(f"\nDone! Generated {count}/{len(scenarios)} files")
        print(f"Location: {test_dir}")
        
    except ImportError as e:
        print(f"ERROR: Missing library: {e}")
        print("Install: pip install gtts pydub")
        return 1
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
