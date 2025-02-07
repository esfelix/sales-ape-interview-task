from fastapi import Depends, HTTPException, Request
from sqlmodel import Session, select

from db import get_session
from session_store import UserSession


def authenticate(
    request: Request, db_session: Session = Depends(get_session)
) -> UserSession:
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(status_code=401, detail="Session token is required.")

    session_query = select(UserSession).where(UserSession.session_id == session_id)
    user_session = db_session.exec(session_query).first()

    if not user_session:
        raise HTTPException(
            status_code=401, detail="No session exists for the given token."
        )

    request.state.app_session = user_session
    return user_session
