from enum import Enum

from pydantic import BaseModel

from src.ai.models import TrackRecommendation
from src.spotify.models import Track


# Request schema
class SimpleChatMessage(BaseModel):
    prompt: str


# Reponse schema
class ChatEventType(str, Enum):
    RECOMMENDATION = "recommendation"
    PLAY_TRACK = "play_track"


class ChatEvent(BaseModel):
    type: ChatEventType


class PlayTrackEvent(ChatEvent):
    type: ChatEventType = ChatEventType.PLAY_TRACK
    track: Track


class TrackRecommendationEvent(ChatEvent):
    type: ChatEventType = ChatEventType.RECOMMENDATION
    recommendation: TrackRecommendation
