import os
import uuid

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlmodel import Session, select

from db import get_session
from session_store import UserSession

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")
REDIRECT_URI = f"{BACKEND_BASE_URL}/auth/spotify/callback"

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/spotify/connect")
async def spotify_login():
    scope = "user-read-private user-read-email user-library-read"
    url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={SPOTIFY_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={scope}"
        f"&show_dialog=true"
    )
    return RedirectResponse(url=url)


@router.get("/spotify/callback")
async def spotify_callback(code: str, db_session: Session = Depends(get_session)):
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(token_url, data=data)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Spotify token exchange failed")
        tokens = resp.json()

    access_token = tokens["access_token"]
    session_id = str(uuid.uuid4())

    new_session = UserSession(session_id=session_id, spotify_access_token=access_token)
    db_session.add(new_session)
    db_session.commit()

    response = RedirectResponse(url=f"{FRONTEND_BASE_URL}")
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response


@router.get("/spotify/me")
async def spotify_me(request: Request, db_session: Session = Depends(get_session)):
    session_id = request.cookies.get("session_id")

    if not session_id:
        return JSONResponse({"logged_in": False}, status_code=401)

    session_query = select(UserSession).where(UserSession.session_id == session_id)
    user_session = db_session.exec(session_query).first()

    if not user_session:
        return JSONResponse({"logged_in": False}, status_code=401)

    if user_session.chat_id:
        user_session.chat_id = None
        db_session.add(user_session)
        db_session.commit()

    return JSONResponse({"logged_in": True})


@router.get("/clear-chat")
async def refresh_session(request: Request, db_session: Session = Depends(get_session)):
    session_id = request.cookies.get("session_id")

    if not session_id:
        return {"message": "No session found"}

    session_query = select(UserSession).where(UserSession.session_id == session_id)
    user_session = db_session.exec(session_query).first()

    if user_session:
        user_session.chat_id = None
        db_session.add(user_session)
        db_session.commit()

    return {"message": "Session refreshed"}
