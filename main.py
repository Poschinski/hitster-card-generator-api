from hitster_card_creator import generate_songs_json, generate_hitster_cards_from_json, upload_file_to_supabase
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(title="Hitster Card Generator API")

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

# =============================================================================
# API MODELS
# =============================================================================

class Song(BaseModel):
    name: str
    year: int
    artist: str
    link: str

class GenerateJsonRequest(BaseModel):
    playlist_url: str

class GenerateCardsRequest(BaseModel):
    songs: List[Song]

@app.post("/generate-json")
def generate_json(req: GenerateJsonRequest):
    try:
        songs = generate_songs_json(
            req.playlist_url,
            SPOTIFY_CLIENT_ID,
            SPOTIFY_CLIENT_SECRET
        )
        return {"songs": songs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-cards")
def generate_cards(req: GenerateCardsRequest):
    try:
        temp_dir, pdf_path = generate_hitster_cards_from_json(req.songs)

        job_id = os.path.basename(temp_dir)

        pdf_url = upload_file_to_supabase(
            pdf_path,
            f"{job_id}/cards.pdf"
        )

        image_urls = []
        for file in os.listdir(temp_dir):
            if file.endswith(".png"):
                local = os.path.join(temp_dir, file)
                remote = f"{job_id}/{file}"
                url = upload_file_to_supabase(local, remote)
                image_urls.append(url)

        return {
            "job_id": job_id,
            "pdf_url": pdf_url,
            "image_urls": image_urls
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))