from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/db/app.db"
    AUDIO_STORAGE_PATH: str = "./data/audio"
    UPLOAD_PATH: str = "./data/uploads"
    EXPORT_PATH: str = "./data/exports"
    TTS_ENGINE: str = "espeak-ng"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Создаем необходимые директории
Path(settings.UPLOAD_PATH).mkdir(parents=True, exist_ok=True)
Path(settings.EXPORT_PATH).mkdir(parents=True, exist_ok=True)
Path(f"{settings.AUDIO_STORAGE_PATH}/tts").mkdir(parents=True, exist_ok=True)
Path(f"{settings.AUDIO_STORAGE_PATH}/responses").mkdir(parents=True, exist_ok=True)
Path("./data/db").mkdir(parents=True, exist_ok=True)

