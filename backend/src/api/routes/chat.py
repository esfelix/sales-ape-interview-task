import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.sql.expression import func
from sqlmodel import Session as DBSession
from sqlmodel import select

from ai.state_machine import build_app as build_state_machine_app
from api.auth_utils import authenticate
from api.schemas import (
    PlayTrackEvent,
    SimpleChatMessage,
    TrackRecommendation,
    TrackRecommendationEvent,
)
from db import get_session as get_db_session
from session_store import UserSession
from spotify.models import Track
from spotify.tables import AudioFeaturesTrack

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/")
async def chat_endpoint(
    request: Request,
    chat_message: SimpleChatMessage,
    user_session: UserSession = Depends(authenticate),
    db_session: DBSession = Depends(get_db_session),
) -> TrackRecommendationEvent | PlayTrackEvent:
    # Select 20 random songs for recommendation
    candidate_tracks = db_session.exec(
        select(AudioFeaturesTrack).order_by(func.random()).limit(30)
    ).all()

    if not candidate_tracks:
        raise HTTPException(status_code=404, detail="No tracks found")

    # Ensure a chat_id exists for the current session
    if user_session.chat_id is None:
        user_session.chat_id = str(uuid.uuid4())
        db_session.add(user_session)
        db_session.commit()

    # Initialize state machine
    state_machine_app = build_state_machine_app(user_session=user_session)

    inputs = {"prompt": chat_message.prompt, "candidate_tracks": candidate_tracks}

    while True:
        action, result, state = state_machine_app.run(
            halt_after=["ai_recommendation", "fetch_recommended_track"],
            inputs=inputs,
        )
        if action.name == "ai_recommendation":
            recommendation: TrackRecommendation = result["recommendation"]
            return TrackRecommendationEvent(recommendation=recommendation)

        if action.name == "fetch_recommended_track":
            track: Track = result["track"]
            return PlayTrackEvent(track=track)
