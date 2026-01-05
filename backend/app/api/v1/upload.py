from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
from loguru import logger
from app.api.deps import get_database
from app.config import settings
from app.utils.excel import read_excel_to_db

router = APIRouter()


@router.post("/upload")
async def upload_excel(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_database)
):
    """
    Загружает Excel файл, парсит его и сохраняет клиентов в БД.
    
    Ожидаемые колонки: ФИО, ИИН, Кредитор, Сумма, Дни просрочки, Телефон
    """
    try:
        # Проверяем расширение файла
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail="Поддерживаются только файлы Excel (.xlsx, .xls)"
            )
        
        # Сохраняем файл
        upload_dir = Path(settings.UPLOAD_PATH)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Файл загружен: {file_path}")
        
        # Парсим и сохраняем в БД
        added_count, error_count = await read_excel_to_db(str(file_path), db)
        
        return {
            "message": "Файл успешно обработан",
            "file_path": str(file_path),
            "added_count": added_count,
            "error_count": error_count
        }
        
    except ValueError as e:
        logger.error(f"Ошибка валидации: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка при загрузке файла: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка обработки файла: {str(e)}")

