import subprocess
import asyncio
from pathlib import Path
from loguru import logger
from app.config import settings




async def generate_tts(text: str, lang: str, client_id: int) -> str:
    """
    Генерирует TTS аудио файл используя Edge-TTS (Neural) с фоллбэком на pyttsx3.
    """
    output_path = Path(settings.AUDIO_STORAGE_PATH) / "tts" / f"{client_id}.wav"
    output_path.parent.mkdir(parents=True, exist_ok=True) # Ensure dir exists!
    
    try:
        # Попытка 1: Edge-TTS (Neural High Quality)
        import edge_tts
        
        # Выбираем голос
        voice = "ru-RU-SvetlanaNeural" if lang in ['ru', 'kk', 'kz'] else "en-US-JennyNeural"
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(output_path))
        
        logger.info(f"TTS (Edge-Neural) аудио создано: {output_path}")
        return str(output_path)
        
    except Exception as e:
        logger.warning(f"Edge-TTS failed ({e}), trying fallback to pyttsx3...")
        
        # Попытка 2: pyttsx3 (System Offline)
        try:
             await asyncio.to_thread(_generate_tts_sync, text, lang, output_path)
             logger.info(f"TTS (System-Offline) аудио создано: {output_path}")
             return str(output_path)
        except Exception as e2:
             logger.error(f"All TTS engines failed. Pyttsx3 error: {e2}")
             return generate_dummy_audio(client_id, output_path)

def _generate_tts_sync(text: str, lang: str, output_path: Path):
    """Синхронная функция для генерации TTS через pyttsx3."""
    import pyttsx3
    
    engine = pyttsx3.init()
    
    # Пытаемся найти подходящий голос
    voices = engine.getProperty('voices')
    target_voice = None
    
    # Ищем русский голос
    if lang in ['ru', 'kk', 'kz']:
        for voice in voices:
            if 'ru' in voice.id.lower() or 'russian' in voice.name.lower():
                target_voice = voice.id
                break
    
    # Если не нашли, используем первый попавшийся
    if target_voice:
        engine.setProperty('voice', target_voice)
    
    engine.setProperty('rate', 150)
    engine.save_to_file(text, str(output_path))
    engine.runAndWait()

def generate_dummy_audio(client_id: int, output_path: Path) -> str:
    """Генерирует 'тихий' WAV файл как заглушку."""
    import wave
    import math
    import struct

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Параметры аудио
        sample_rate = 44100
        duration_seconds = 2.0
        frequency = 440.0
        
        # Генерируем 2 секунды синусоиды (чтобы было слышно, что это тест)
        with wave.open(str(output_path), 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
            wav_file.setframerate(sample_rate)
            
            num_samples = int(sample_rate * duration_seconds)
            
            # Если нужен просто "beep"
            data = []
            for i in range(num_samples):
                # Простая синусоида
                value = int(32767.0 * 0.5 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
                data.append(struct.pack('<h', value))
            
            wav_file.writeframes(b''.join(data))
            
        logger.info(f"Сгенерировано Dummy TTS аудио: {output_path}")
        return str(output_path)
        
    except Exception as e:
        logger.error(f"Не удалось создать даже dummy audio: {e}")
        raise

