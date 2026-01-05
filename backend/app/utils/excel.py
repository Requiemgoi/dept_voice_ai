import pandas as pd
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from app.models.client import Client
from app.schemas.client import ClientCreate


async def read_excel_to_db(file_path: str, db: AsyncSession) -> tuple[int, int]:
    """
    Читает Excel файл и создает записи Client в БД.
    
    Ожидаемые колонки: ФИО, ИИН, Кредитор, Сумма, Дни просрочки, Телефон
    
    Returns:
        tuple: (количество успешно добавленных, количество ошибок)
    """
    try:
        df = pd.read_excel(file_path)
        
        # Нормализация названий колонок (убираем пробелы, приводим к нижнему регистру)
        df.columns = df.columns.str.strip().str.lower()
        
        # Маппинг возможных вариантов названий колонок (все ключи в нижнем регистре)
        column_mapping = {
            'фио': 'fio',
            'fio': 'fio',
            'name': 'fio',
            'клиент': 'fio',
            
            'иин': 'iin',
            'iin': 'iin',
            'id': 'iin',
            
            'кредитор': 'creditor',
            'creditor': 'creditor',
            'bank': 'creditor',
            
            'сумма': 'amount',
            'amount': 'amount',
            'debt': 'amount',
            'sum': 'amount',
            
            'дни просрочки': 'days_overdue',
            'days_overdue': 'days_overdue',
            'delay': 'days_overdue',
            'days': 'days_overdue',
            
            'телефон': 'phone',
            'phone': 'phone',
            'tel': 'phone',
            'mobile': 'phone'
        }
        
        # Переименовываем колонки
        df.rename(columns=column_mapping, inplace=True)
        
        # Проверяем наличие всех необходимых колонок
        required_columns = ['fio', 'iin', 'creditor', 'amount', 'days_overdue', 'phone']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}")
        
        # Удаляем пустые строки
        df = df.dropna(subset=required_columns)
        
        added_count = 0
        error_count = 0
        
        for _, row in df.iterrows():
            try:
                # Проверяем, существует ли клиент с таким ИИН
                existing = await db.execute(
                    Client.__table__.select().where(Client.iin == str(row['iin']))
                )
                if existing.fetchone():
                    logger.warning(f"Клиент с ИИН {row['iin']} уже существует, пропускаем")
                    error_count += 1
                    continue
                
                client = Client(
                    fio=str(row['fio']).strip(),
                    iin=str(row['iin']).strip(),
                    creditor=str(row['creditor']).strip(),
                    amount=float(row['amount']),
                    days_overdue=int(row['days_overdue']),
                    phone=str(row['phone']).strip(),
                    status='pending'
                )
                
                db.add(client)
                added_count += 1
                
            except Exception as e:
                logger.error(f"Ошибка при обработке строки {row.get('iin', 'unknown')}: {e}")
                error_count += 1
                continue
        
        await db.commit()
        logger.info(f"Успешно добавлено клиентов: {added_count}, ошибок: {error_count}")
        
        return added_count, error_count
        
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла: {e}")
        await db.rollback()
        raise


async def export_to_excel(clients: list[Client], output_path: str) -> str:
    """
    Экспортирует список клиентов в Excel файл с категориями в 7-й колонке.
    
    Args:
        clients: Список объектов Client
        output_path: Путь для сохранения файла
        
    Returns:
        str: Путь к сохраненному файлу
    """
    try:
        data = []
        for client in clients:
            data.append({
                'ФИО': client.fio,
                'ИИН': client.iin,
                'Кредитор': client.creditor,
                'Сумма': client.amount,
                'Дни просрочки': client.days_overdue,
                'Телефон': client.phone,
                'Категория': client.category or 'не обработано'
            })
        
        df = pd.DataFrame(data)
        
        # Создаем директорию если не существует
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        df.to_excel(output_path, index=False, engine='openpyxl')
        logger.info(f"Экспортировано {len(clients)} клиентов в {output_path}")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Ошибка при экспорте в Excel: {e}")
        raise

