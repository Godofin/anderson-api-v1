from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
import schemas

router = APIRouter()

# --- ARTISTS ---
@router.get("/artists", response_model=List[schemas.Artist], tags=["Artists"])
async def get_artists(filter: str = "All", db: Session = Depends(get_db)):
    """Retorna a lista de artistas (GigDex). Filtros: All, Popular."""
    query = db.query(models.Artist)
    if filter == "Popular":
        query = query.filter(models.Artist.is_popular == True)
    return query.all()

@router.get("/artists/{artist_id}", response_model=schemas.Artist, tags=["Artists"])
async def get_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(models.Artist).filter(models.Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artista não encontrado")
    return artist

# --- SHOW LOGS (CHECK-IN) ---
@router.post("/shows", response_model=schemas.ShowLog, status_code=status.HTTP_201_CREATED, tags=["Shows"])
async def create_show_log(show_data: schemas.ShowLogCreate, user_id: int = 1, db: Session = Depends(get_db)):
    """Registra um novo show (Check-in). Default user_id=1 para teste."""
    new_show = models.ShowLog(**show_data.model_dump(), user_id=user_id)
    db.add(new_show)
    
    # Atualizar estatísticas do usuário
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.total_shows += 1
        # Lógica simples de nível
        if user.total_shows > 50: user.level = "Headliner"
        elif user.total_shows > 10: user.level = "Roadie"
        
    db.commit()
    db.refresh(new_show)
    return new_show

@router.get("/shows", response_model=List[schemas.ShowLog], tags=["Shows"])
async def get_user_shows(user_id: int = 1, db: Session = Depends(get_db)):
    """Retorna todos os shows registrados pelo usuário."""
    return db.query(models.ShowLog).filter(models.ShowLog.user_id == user_id).order_by(models.ShowLog.show_date.desc()).all()

# --- MAP & STATS ---
@router.get("/stats/{user_id}", response_model=schemas.FanStats, tags=["Stats"])
async def get_fan_stats(user_id: int, db: Session = Depends(get_db)):
    """Calcula estatísticas do perfil do fã."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Artista mais visto
    most_seen = db.query(models.Artist.name, func.count(models.ShowLog.id).label('total'))\
        .join(models.ShowLog)\
        .filter(models.ShowLog.user_id == user_id)\
        .group_by(models.Artist.name)\
        .order_by(func.count(models.ShowLog.id).desc())\
        .first()
        
    # Gênero predominante
    pred_genre = db.query(models.Artist.genre, func.count(models.ShowLog.id))\
        .join(models.ShowLog)\
        .filter(models.ShowLog.user_id == user_id)\
        .group_by(models.Artist.genre)\
        .order_by(func.count(models.ShowLog.id).desc())\
        .first()

    return {
        "total_shows": user.total_shows,
        "total_festivals": db.query(models.ShowLog).filter(models.ShowLog.user_id == user_id).count(), # Simplificado
        "most_seen_artist": most_seen[0] if most_seen else "Nenhum ainda",
        "predominant_genre": pred_genre[0] if pred_genre else "Nenhum ainda",
        "fan_level": user.level
    }

# --- AUTH (SIMPLIFICADO) ---
@router.post("/users", response_model=schemas.User, tags=["Auth"])
async def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Em um app real, usaríamos hash de senha
    db_user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=user_data.password, # Apenas para exemplo
        avatar_url=user_data.avatar_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
