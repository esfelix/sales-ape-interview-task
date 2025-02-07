from typing import Optional

from sqlmodel import Field, SQLModel


class UserSession(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    session_id: str = Field(primary_key=True)
    spotify_access_token: str
    chat_id: Optional[str] = None
