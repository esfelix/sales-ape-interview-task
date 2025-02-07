import os

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////data/salesape_task.db")

# Initialize database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# Ensure tables are created
def init_db():
    from spotify.tables import AudioFeaturesTrack  # noqa
    from session_store import UserSession  # noqa

    SQLModel.metadata.create_all(engine)


# Dependency to get DB session
def get_session():
    with Session(engine) as session:
        yield session
