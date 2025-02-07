from pydantic import BaseModel


class TrackRecommendation(BaseModel):
    message: str
    track_id: str
    track_name: str
    artists: str
