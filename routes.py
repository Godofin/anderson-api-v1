from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session

# Importações locais
from database import get_db
import models
import schemas

router = APIRouter()

# ===============================================
# --- ROTAS DE EVENTOS ---
# ===============================================

# --- ROTA POST (CRIAÇÃO DE EVENTO) ---
@router.post("/events", response_model=schemas.Event, status_code=status.HTTP_201_CREATED, tags=["Events"])
async def create_event(event_data: schemas.EventCreate, db: Session = Depends(get_db)):
    """ Cria um novo evento no banco de dados Postgres. """
    try:
        # Cria a instância do modelo SQL
        new_event = models.Event(**event_data.model_dump())
        db.add(new_event)
        db.commit()
        db.refresh(new_event) # Atualiza com o ID gerado
        return new_event
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar evento: {str(e)}")

# --- ROTAS GET (LEITURA DE EVENTOS) ---
@router.get("/events", response_model=List[schemas.Event], tags=["Events"])
async def get_active_events(db: Session = Depends(get_db)):
    """ Retorna todos os eventos ATIVOS. """
    try:
        events = db.query(models.Event).filter(models.Event.active_event == True).order_by(models.Event.id).all()
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/all", response_model=List[schemas.Event], tags=["Events"])
async def get_all_events(db: Session = Depends(get_db)):
    """ Retorna TODOS os eventos, ativos e inativos. """
    try:
        events = db.query(models.Event).order_by(models.Event.id).all()
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/{event_id}", response_model=schemas.Event, tags=["Events"])
async def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    """ Retorna um evento específico pelo seu ID numérico. """
    try:
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not event:
             raise HTTPException(status_code=404, detail=f"Evento com id {event_id} não encontrado.")
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar evento: {e}")

# --- ROTA PUT (EDIÇÃO DE EVENTO) ---
@router.put("/events/{event_id}", response_model=schemas.Event, tags=["Events"])
async def update_event(event_id: int, event_update: schemas.EventUpdate, db: Session = Depends(get_db)):
    """ Atualiza um evento existente. """
    try:
        # Busca o evento existente
        db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not db_event:
            raise HTTPException(status_code=404, detail=f"Evento com id {event_id} não encontrado.")
        
        # Atualiza os campos
        update_data = event_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_event, key, value)
        
        db.commit()
        db.refresh(db_event)
        return db_event
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTA DELETE (EXCLUSÃO DE EVENTO) ---
@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Events"])
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    """ Deleta um evento. """
    try:
        db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not db_event:
            raise HTTPException(status_code=404, detail="Evento não encontrado.")
        
        db.delete(db_event)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ===============================================
# --- NOVAS ROTAS DE RATING ---
# ===============================================

# --- ROTA POST (CRIAÇÃO DE RATING) ---
@router.post("/ratings", response_model=schemas.Rating, status_code=status.HTTP_201_CREATED, tags=["Ratings"])
async def create_rating(rating_data: schemas.RatingCreate, db: Session = Depends(get_db)):
    """ Cadastra uma nova avaliação (rating) para um evento. """
    if not 0 <= rating_data.score <= 5:
        raise HTTPException(status_code=400, detail="A nota deve ser um valor inteiro entre 0 e 5.")

    try:
        new_rating = models.Rating(**rating_data.model_dump())
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return new_rating
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar avaliação: {str(e)}")


# --- ROTA GET (LEITURA DE TODOS OS RATINGS) ---
@router.get("/ratings", response_model=List[schemas.Rating], tags=["Ratings"])
async def get_all_ratings(db: Session = Depends(get_db)):
    """ Retorna todas as avaliações cadastradas. """
    try:
        ratings = db.query(models.Rating).order_by(models.Rating.created_at.desc()).all()
        return ratings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- ROTA GET (LEITURA DE RATINGS POR EVENTO) ---
@router.get("/ratings/event/{event_name}", response_model=List[schemas.Rating], tags=["Ratings"])
async def get_ratings_by_event(event_name: str, db: Session = Depends(get_db)):
    """ Retorna todas as avaliações para um evento específico. """
    try:
        ratings = db.query(models.Rating).filter(models.Rating.event_name == event_name).order_by(models.Rating.created_at.desc()).all()
        return ratings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar avaliações: {str(e)}")