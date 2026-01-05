"""
Unit tests для STT Engine (Speech-to-Text).

Запуск:
    pytest tests/test_stt.py -v

Примечание:
    Для полного тестирования необходимы:
    - Установленный vosk
    - Загруженные модели (scripts/download_models.sh)
    - Тестовые WAV файлы (scripts/generate_demo_audio.py)
"""

import pytest
import sys
import wave
import struct
import tempfile
from pathlib import Path

# Добавляем путь к ml модулю
sys.path.insert(0, str(Path(__file__).parent.parent))

from ml.stt_engine import (
    STTEngine,
    STTEngineError,
    ModelNotFoundError,
    AudioFormatError,
    SAMPLE_RATE,
    CHANNELS,
    MODELS_DIR,
    MODEL_PATHS
)


# Фикстуры
@pytest.fixture
def temp_wav_file():
    """Создает временный WAV файл для тестов."""
    def _create_wav(duration_ms: int = 1000, sample_rate: int = 16000, channels: int = 1):
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_path = Path(temp_file.name)
        temp_file.close()
        
        num_samples = int(sample_rate * duration_ms / 1000)
        
        with wave.open(str(temp_path), 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            # Генерируем простой сигнал
            samples = [int(32767 * 0.1 * ((i % 100) / 50 - 1)) for i in range(num_samples)]
            wav_file.writeframes(struct.pack('<' + 'h' * num_samples, *samples))
        
        return temp_path
    
    return _create_wav


@pytest.fixture
def stt_engine():
    """Создает экземпляр STT Engine."""
    # Сбрасываем singleton для изоляции тестов
    STTEngine._instance = None
    return STTEngine()


class TestSTTEngineInit:
    """Тесты инициализации STT Engine."""
    
    def test_singleton_pattern(self):
        """Тест паттерна Singleton."""
        STTEngine._instance = None
        engine1 = STTEngine()
        engine2 = STTEngine()
        
        assert engine1 is engine2
    
    def test_models_dict_initialized(self, stt_engine):
        """Тест инициализации словаря моделей."""
        assert hasattr(stt_engine, '_models')
        assert 'ru' in stt_engine._models
        assert 'kk' in stt_engine._models
    
    def test_model_paths_defined(self):
        """Тест определения путей к моделям."""
        assert 'ru' in MODEL_PATHS
        assert 'kk' in MODEL_PATHS
        assert 'vosk-model-small-ru' in str(MODEL_PATHS['ru'])
        assert 'vosk-model-small-kz' in str(MODEL_PATHS['kk'])


class TestAudioValidation:
    """Тесты валидации аудио файлов."""
    
    def test_valid_wav_file(self, stt_engine, temp_wav_file):
        """Тест чтения корректного WAV файла."""
        wav_path = temp_wav_file(duration_ms=500)
        
        try:
            audio_data, sample_rate = stt_engine._read_audio_file(str(wav_path))
            assert len(audio_data) > 0
            assert sample_rate == 16000
        finally:
            wav_path.unlink(missing_ok=True)
    
    def test_file_not_found(self, stt_engine):
        """Тест несуществующего файла."""
        with pytest.raises(FileNotFoundError):
            stt_engine._read_audio_file("/nonexistent/path/audio.wav")
    
    def test_wrong_extension(self, stt_engine, tmp_path):
        """Тест неправильного расширения файла."""
        mp3_file = tmp_path / "audio.mp3"
        mp3_file.touch()
        
        with pytest.raises(AudioFormatError) as excinfo:
            stt_engine._read_audio_file(str(mp3_file))
        
        assert "WAV" in str(excinfo.value)
    
    def test_wrong_channels(self, stt_engine, temp_wav_file):
        """Тест файла с неправильным числом каналов."""
        wav_path = temp_wav_file(channels=2)  # Stereo
        
        try:
            with pytest.raises(AudioFormatError) as excinfo:
                stt_engine._read_audio_file(str(wav_path))
            
            assert "mono" in str(excinfo.value).lower()
        finally:
            wav_path.unlink(missing_ok=True)
    
    def test_wrong_sample_rate(self, stt_engine, temp_wav_file):
        """Тест файла с неправильной частотой дискретизации."""
        wav_path = temp_wav_file(sample_rate=44100)  # CD quality
        
        try:
            with pytest.raises(AudioFormatError) as excinfo:
                stt_engine._read_audio_file(str(wav_path))
            
            assert "16000" in str(excinfo.value)
        finally:
            wav_path.unlink(missing_ok=True)


class TestLanguageSupport:
    """Тесты поддержки языков."""
    
    def test_supported_languages(self, stt_engine):
        """Тест списка поддерживаемых языков."""
        # Метод должен вернуть только языки с доступными моделями
        available = stt_engine.get_available_languages()
        assert isinstance(available, list)
    
    def test_invalid_language(self, stt_engine, temp_wav_file):
        """Тест неподдерживаемого языка."""
        wav_path = temp_wav_file()
        
        try:
            with pytest.raises((ValueError, ModelNotFoundError)):
                stt_engine.recognize_audio(str(wav_path), lang='xx')
        finally:
            wav_path.unlink(missing_ok=True)
    
    def test_model_availability_check(self, stt_engine):
        """Тест проверки доступности модели."""
        # Метод не должен выбрасывать исключение
        ru_available = stt_engine.is_model_available('ru')
        kk_available = stt_engine.is_model_available('kk')
        
        assert isinstance(ru_available, bool)
        assert isinstance(kk_available, bool)


class TestRecognition:
    """Тесты распознавания (требуют загруженных моделей)."""
    
    @pytest.mark.skipif(
        not MODEL_PATHS['ru'].exists(),
        reason="Russian model not installed"
    )
    def test_recognize_russian(self, stt_engine, temp_wav_file):
        """Тест распознавания русской речи."""
        wav_path = temp_wav_file(duration_ms=1000)
        
        try:
            text, lang = stt_engine.recognize_audio(str(wav_path), 'ru')
            
            assert isinstance(text, str)
            assert lang == 'ru'
        finally:
            wav_path.unlink(missing_ok=True)
    
    @pytest.mark.skipif(
        not MODEL_PATHS['kk'].exists(),
        reason="Kazakh model not installed"
    )
    def test_recognize_kazakh(self, stt_engine, temp_wav_file):
        """Тест распознавания казахской речи."""
        wav_path = temp_wav_file(duration_ms=1000)
        
        try:
            text, lang = stt_engine.recognize_audio(str(wav_path), 'kk')
            
            assert isinstance(text, str)
            assert lang == 'kk'
        finally:
            wav_path.unlink(missing_ok=True)
    
    @pytest.mark.skipif(
        not any(p.exists() for p in MODEL_PATHS.values()),
        reason="No models installed"
    )
    def test_auto_detect(self, stt_engine, temp_wav_file):
        """Тест автоматического определения языка."""
        wav_path = temp_wav_file(duration_ms=1000)
        
        try:
            text, lang = stt_engine.recognize_auto_detect(str(wav_path))
            
            assert isinstance(text, str)
            assert lang in ['ru', 'kk']
        finally:
            wav_path.unlink(missing_ok=True)


class TestErrorHandling:
    """Тесты обработки ошибок."""
    
    def test_model_not_found_error(self, stt_engine, temp_wav_file):
        """Тест ошибки отсутствующей модели."""
        wav_path = temp_wav_file()
        
        # Убеждаемся что модель не загружена
        stt_engine._models['ru'] = None
        
        # Если модель не существует на диске - должна быть ошибка
        if not MODEL_PATHS['ru'].exists():
            try:
                with pytest.raises(ModelNotFoundError):
                    stt_engine.recognize_audio(str(wav_path), 'ru')
            finally:
                wav_path.unlink(missing_ok=True)
        else:
            wav_path.unlink(missing_ok=True)
            pytest.skip("Model exists on disk")
    
    def test_audio_format_error_message(self, stt_engine, temp_wav_file):
        """Тест информативности сообщений об ошибках."""
        wav_path = temp_wav_file(sample_rate=8000)
        
        try:
            with pytest.raises(AudioFormatError) as excinfo:
                stt_engine._read_audio_file(str(wav_path))
            
            error_msg = str(excinfo.value)
            assert "16000" in error_msg or "Hz" in error_msg
        finally:
            wav_path.unlink(missing_ok=True)


class TestWrapperFunctions:
    """Тесты функций-оберток."""
    
    def test_recognize_audio_wrapper_exists(self):
        """Тест существования функции-обертки."""
        from ml.stt_engine import recognize_audio
        assert callable(recognize_audio)
    
    def test_recognize_auto_wrapper_exists(self):
        """Тест существования функции автоопределения."""
        from ml.stt_engine import recognize_auto
        assert callable(recognize_auto)
    
    def test_stt_engine_singleton_export(self):
        """Тест экспорта singleton."""
        from ml.stt_engine import stt_engine
        assert stt_engine is not None
        assert isinstance(stt_engine, STTEngine)


class TestConstants:
    """Тесты констант."""
    
    def test_sample_rate(self):
        """Тест частоты дискретизации."""
        assert SAMPLE_RATE == 16000
    
    def test_channels(self):
        """Тест количества каналов."""
        assert CHANNELS == 1
    
    def test_models_dir(self):
        """Тест директории моделей."""
        assert MODELS_DIR is not None
        assert 'models' in str(MODELS_DIR)


# Интеграционные тесты с реальными аудио файлами
class TestIntegration:
    """Интеграционные тесты с демо-файлами."""
    
    TEST_AUDIO_DIR = Path(__file__).parent.parent / "ml" / "test_audio"
    
    @pytest.mark.skipif(
        not (TEST_AUDIO_DIR / "promise_ru.wav").exists(),
        reason="Demo audio files not generated"
    )
    @pytest.mark.skipif(
        not MODEL_PATHS['ru'].exists(),
        reason="Russian model not installed"
    )
    def test_recognize_promise_ru(self, stt_engine):
        """Тест распознавания обещания на русском."""
        audio_path = self.TEST_AUDIO_DIR / "promise_ru.wav"
        
        text, lang = stt_engine.recognize_audio(str(audio_path), 'ru')
        
        assert isinstance(text, str)
        assert lang == 'ru'
        # Текст может не совпадать идеально из-за качества TTS
    
    @pytest.mark.skipif(
        not (TEST_AUDIO_DIR / "ignore_ru.wav").exists(),
        reason="Demo audio files not generated"
    )
    @pytest.mark.skipif(
        not MODEL_PATHS['ru'].exists(),
        reason="Russian model not installed"
    )
    def test_recognize_ignore_ru(self, stt_engine):
        """Тест распознавания отказа на русском."""
        audio_path = self.TEST_AUDIO_DIR / "ignore_ru.wav"
        
        text, lang = stt_engine.recognize_audio(str(audio_path), 'ru')
        
        assert isinstance(text, str)
        assert lang == 'ru'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
