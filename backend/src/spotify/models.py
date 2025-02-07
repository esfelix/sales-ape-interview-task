from typing import List, Optional

from pydantic import BaseModel, Field


class ExternalUrls(BaseModel):
    spotify: str = Field(..., description="The Spotify URL for the object.")


class SimplifiedArtist(BaseModel):
    id: str = Field(..., description="The Spotify ID for the artist.")
    name: str = Field(..., description="The name of the artist.")
    href: str = Field(..., description="API endpoint for artist details.")
    external_urls: ExternalUrls
    uri: str = Field(..., description="The Spotify URI for the artist.")


class Track(BaseModel):
    id: str = Field(..., description="Spotify ID for the track.")
    name: str = Field(..., description="Track name.")
    artists: List[SimplifiedArtist]
    duration_ms: int = Field(..., description="Track duration in milliseconds.", ge=0)
    external_urls: ExternalUrls
    popularity: int = Field(..., description="Popularity score (0-100).", ge=0, le=100)
    preview_url: Optional[str] = Field(None, description="URL for a 30-second preview.")
    uri: str = Field(..., description="Spotify URI for the track.")
