from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    level = Column(String, default="Groupie") # Groupie, Roadie, Headliner
    total_shows = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    shows = relationship("ShowLog", back_populates="user")

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    mbid = Column(String, unique=True, index=True, nullable=True) # MusicBrainz ID
    name = Column(String, index=True, nullable=False)
    genre = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    is_popular = Column(Boolean, default=False)
    
    shows = relationship("ShowLog", back_populates="artist")

class ShowLog(Base):
    __tablename__ = "show_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    artist_id = Column(Integer, ForeignKey("artists.id"))
    event_name = Column(String, nullable=False) # Nome do Festival ou Turnê
    venue_name = Column(String, nullable=False) # Local
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    show_date = Column(Date, nullable=False)
    rating = Column(Integer, nullable=True) # 1-5 estrelas
    comment = Column(Text, nullable=True)
    media_url = Column(String, nullable=True) # Foto ou vídeo curto
    favorite_song = Column(String, nullable=True)
    companion = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="shows")
    artist = relationship("Artist", back_populates="shows")
