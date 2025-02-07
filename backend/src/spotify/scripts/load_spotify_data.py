import os

import polars as pl
from sqlmodel import Session, SQLModel, create_engine, text

from src.session_store import UserSession
from src.spotify.tables import AudioFeaturesTrack

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////data/salesape_task.db")
CSV_PATH = "/src/spotify/spotify_tracks_top_10000.csv"

# Initialize database engine
engine = create_engine(DATABASE_URL)

# Drop the existing table (ensures schema updates)
with Session(engine) as session:
    session.execute(text("DROP TABLE IF EXISTS audiofeaturestrack"))
    session.execute(text("DROP TABLE IF EXISTS usersession"))

    session.commit()

# Recreate tables
SQLModel.metadata.create_all(engine)

# Insert new records
df = pl.read_csv(CSV_PATH)
with Session(engine) as session:
    session.bulk_save_objects(
        [AudioFeaturesTrack(**row) for row in df.iter_rows(named=True)]
    )
    session.commit()

print(
    f"Data refreshed with the latest schema for tables {AudioFeaturesTrack.__tablename__}, {UserSession.__tablename__}"
)
