from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime, date

class EventBase(BaseModel):
    image: str
    alt: str
    title: str
    date: str
    # Aceita string ou date para evitar erros de validação (422)
    date_event: Union[date, str]
    year: str
    description: str
    buttonText: str
    eventName: str
    cities: List[str] = []
    active_event: bool = True
    ecommerce_link: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "image": "https://exemplo.com/imagem.jpg",
                "alt": "Shows/Eventos",
                "title": "Excursão Incrível",
                "date": "20 a 22 de Novembro",
                "date_event": "2025-11-20",
                "year": "2025",
                "description": "Detalhes da viagem...",
                "buttonText": "Reservar",
                "eventName": "excursao-novembro",
                "cities": ["São Paulo", "Ubatuba"],
                "active_event": True,
                "ecommerce_link": "https://wa.me/..."
            }
        }

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    image: Optional[str] = None
    alt: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    # Permite str ou date na atualização também
    date_event: Optional[Union[date, str]] = None
    year: Optional[str] = None
    description: Optional[str] = None
    buttonText: Optional[str] = None
    eventName: Optional[str] = None
    cities: Optional[List[str]] = None
    active_event: Optional[bool] = None
    ecommerce_link: Optional[str] = None

class Event(EventBase):
    id: int

    class Config:
        from_attributes = True


class RatingCreate(BaseModel):
    event_name: str = Field(..., description="Nome do evento avaliado")
    reviewer_name: str = Field(..., description="Nome da pessoa que fez a avaliação")
    score: int = Field(..., ge=0, le=5, description="Nota de 0 a 5")
    comment: Optional[str] = Field(None, description="Comentários adicionais")

class Rating(RatingCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ===============================================
# --- NOVOS SCHEMAS: LINKTREE ---
# ===============================================

class LinktreeBase(BaseModel):
    name: str = Field(..., description="Nome da excursão")
    image_url: Optional[str] = Field(None, description="Link da imagem representativa")
    whatsapp_url: str = Field(..., description="Link do grupo do WhatsApp")
    active: bool = True
    event_date: Optional[Union[date, str]] = Field(None, description="Data da excursão")

class LinktreeCreate(LinktreeBase):
    pass

class LinktreeUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    whatsapp_url: Optional[str] = None
    active: Optional[bool] = None
    event_date: Optional[Union[date, str]] = None

class LinktreeResponse(LinktreeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True