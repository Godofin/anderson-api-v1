from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Date
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String, nullable=True)
    alt = Column(String, nullable=True)
    title = Column(String, nullable=True)
    date = Column(String, nullable=True)
    
    # CORREÇÃO: Usar 'Date' do SQLAlchemy para alinhar com o banco Postgres
    # O primeiro argumento "date_event" garante que mapeia para a coluna correta (snake_case)
    date_event = Column("date_event", Date, nullable=True)
    
    year = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    
    # Mapeamentos snake_case do banco para variáveis camelCase do Python
    buttonText = Column("button_text", String, nullable=True)
    eventName = Column("event_name", String, nullable=True)
    
    cities = Column(ARRAY(String), default=[])
    active_event = Column(Boolean, default=True)
    ecommerce_link = Column(String, nullable=True)

class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    reviewer_name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# ===============================================
# --- NOVO MODELO: LINKTREE ---
# ===============================================
class Linktree(Base):
    __tablename__ = "linktree_links"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)            # Nome da excursão
    image_url = Column(String, nullable=True)        # Link da imagem
    whatsapp_url = Column(String, nullable=False)    # Link do grupo do whatsapp
    active = Column(Boolean, default=True)           # Para ativar/desativar facilmente
    event_date = Column(Date, nullable=True)         # NOVA COLUNA: Data do evento
    created_at = Column(DateTime(timezone=True), server_default=func.now())