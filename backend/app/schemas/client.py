from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ClientBase(BaseModel):
    fio: str
    iin: str
    creditor: str
    amount: float
    days_overdue: int
    phone: str


class ClientCreate(ClientBase):
    pass


class CallRecordResponse(BaseModel):
    id: int
    tts_text: Optional[str] = None
    tts_audio_path: Optional[str] = None
    response_audio_path: Optional[str] = None
    transcript: Optional[str] = None
    detected_language: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    call_metadata: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ClientResponse(BaseModel):
    id: int
    fio: str
    iin: str
    creditor: str
    amount: float
    days_overdue: int
    phone: str
    status: str
    category: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ClientDetail(ClientResponse):
    call_records: List[CallRecordResponse] = []


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class ClientListResponse(BaseModel):
    items: List[ClientResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class CallRecordWithClient(CallRecordResponse):
    client: ClientResponse


class CallHistoryResponse(BaseModel):
    items: List[CallRecordWithClient]
    total: int
    page: int
    page_size: int
    total_pages: int

