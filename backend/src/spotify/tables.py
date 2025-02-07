from sqlmodel import Field, SQLModel


class AudioFeaturesTrack(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: int = Field(primary_key=True)
    track_id: str = Field(..., description="Spotify ID for the track.")
    track_name: str = Field(..., description="Track name.")
    artists: str = Field(
        ..., description="Comma-separated list of artists for the track."
    )
    album_name: str = Field(..., description="Album name the track belongs to.")
    popularity: int = Field(..., description="Popularity score of the track (0-100).")
    duration_ms: int = Field(..., description="Duration of the track in milliseconds.")
    explicit: bool = Field(
        ..., description="Indicates whether the track has explicit lyrics."
    )

    # Audio Features
    danceability: float = Field(
        ..., description="Describes how suitable a track is for dancing."
    )
    energy: float = Field(
        ..., description="A measure from 0.0 to 1.0 representing intensity and activity."
    )
    key: int = Field(
        ...,
        description="The key the track is in, using standard Pitch Class notation (0-11).",
    )
    loudness: float = Field(
        ..., description="Overall loudness of a track in decibels (dB)."
    )
    mode: int = Field(..., description="Indicates modality: 1 for major, 0 for minor.")
    speechiness: float = Field(..., description="Detects spoken words in a track.")
    acousticness: float = Field(
        ...,
        description="Confidence measure (0.0 to 1.0) of whether the track is acoustic.",
    )
    instrumentalness: float = Field(
        ..., description="Predicts whether a track contains no vocals."
    )
    liveness: float = Field(
        ..., description="Detects the presence of an audience in the recording."
    )
    valence: float = Field(
        ...,
        description="A measure from 0.0 to 1.0 indicating how positive or happy a track sounds.",
    )
    tempo: float = Field(
        ..., description="Estimated tempo of a track in beats per minute (BPM)."
    )
    time_signature: int = Field(
        ..., description="Estimated time signature (meter) of the track."
    )
    track_genre: str = Field(..., description="Genre of the track (if available).")
