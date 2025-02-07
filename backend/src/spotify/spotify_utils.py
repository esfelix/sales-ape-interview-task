import httpx
from fastapi import HTTPException

from src.spotify.models import Track


def fetch_spotify_track(track_id: str, spotify_access_token: str) -> Track:
    headers = {"Authorization": f"Bearer {spotify_access_token}"}
    with httpx.Client() as client:
        r = client.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)

        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)

    return Track.model_validate(r.json(), from_attributes=True)
