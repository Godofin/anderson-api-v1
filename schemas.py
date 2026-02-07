from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, datetime

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: EmailStr
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    level: str
    total_shows: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Artist Schemas ---
class ArtistBase(BaseModel):
    name: str
    mbid: Optional[str] = None
    genre: Optional[str] = None
    image_url: Optional[str] = None
    is_popular: bool = False

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    id: int

    class Config:
        from_attributes = True

# --- ShowLog Schemas ---
class ShowLogBase(BaseModel):
    artist_id: int
    event_name: str
    venue_name: str
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    show_date: date
    rating: Optional[int] = None
    comment: Optional[str] = None
    media_url: Optional[str] = None
    favorite_song: Optional[str] = None
    companion: Optional[str] = None

class ShowLogCreate(ShowLogBase):
    pass

class ShowLog(ShowLogBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Stats Schemas ---
class FanStats(BaseModel):
    total_shows: int
    total_festivals: int
    most_seen_artist: Optional[str]
    predominant_genre: Optional[str]
    fan_level: str
