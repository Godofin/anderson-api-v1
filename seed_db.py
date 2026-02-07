import os
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from musicbrainz_client import MusicBrainzClient

# Artistas sugeridos pelo usuário
INITIAL_ARTISTS = [
    # Internacionais
    "Coldplay", "Taylor Swift", "Metallica", "Red Hot Chili Peppers", 
    "Bruno Mars", "The Weeknd", "Foo Fighters", "Beyoncé",
    # Nacionais
    "Anitta", "Ivete Sangalo", "Ludmilla", "Caetano Veloso", 
    "Titãs", "Capital Inicial", "Alok", "Matuê", "Sepultura"
]

def seed():
    # Garantir que as tabelas existam
    models.Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    mb_client = MusicBrainzClient()
    
    print("Iniciando o seeding de artistas...")
    
    for artist_name in INITIAL_ARTISTS:
        # Verificar se o artista já existe
        existing = db.query(models.Artist).filter(models.Artist.name == artist_name).first()
        if existing:
            print(f"Artista {artist_name} já existe no banco.")
            continue
            
        print(f"Buscando {artist_name} na MusicBrainz...")
        info = mb_client.search_artist(artist_name)
        
        if info:
            new_artist = models.Artist(
                mbid=info["mbid"],
                name=info["name"],
                genre=info["genre"],
                image_url=mb_client.get_artist_image(info["mbid"]),
                is_popular=True
            )
            db.add(new_artist)
            db.commit()
            print(f"Adicionado: {info['name']} ({info['genre']})")
        else:
            # Fallback se não encontrar na MB
            new_artist = models.Artist(
                name=artist_name,
                is_popular=True
            )
            db.add(new_artist)
            db.commit()
            print(f"Adicionado (fallback): {artist_name}")
            
    db.close()
    print("Seeding concluído!")

if __name__ == "__main__":
    seed()
