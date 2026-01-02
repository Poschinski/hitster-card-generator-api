from pydantic import BaseModel
from typing import List

class Song(BaseModel):
    name: str
    year: int
    artist: str
    link: str

class GenerateJsonRequest(BaseModel):
    playlist_url: str

class GenerateCardsRequest(BaseModel):
    songs: List[Song]