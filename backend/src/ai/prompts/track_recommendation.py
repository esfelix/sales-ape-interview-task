import json

from src.spotify.tables import AudioFeaturesTrack


def get_messages(
    candidate_tracks: list[AudioFeaturesTrack], chat_history: list[dict]
) -> list:
    metadata = {
        field: desc.description for field, desc in AudioFeaturesTrack.model_fields.items()
    }

    messages = [
        {
            "role": "system",
            "content": (
                "Listen to the user and determine the most appropriate song for the user from the list enclosed in triple backticks.\n"
                "You are a helpful music recommender assistant.\n"
                "Listen to the user and determine the most appropriate song for the user "
                "from the provided list.\n"
                "Consider how the user is feeling, their circumstances, preferences, goals, and request.\n"
                "Return the recommended track along with a short, empathetic message suggesting the song.\n"
                "Consider past recommendations and feedback from the user."
                f"Candidate songs ```{json.dumps([song.dict() for song in candidate_tracks], indent=2)}```\n"
                f"Metadata for the song fields: {json.dumps(metadata, indent=2)}\n"
            ),
        },
        *chat_history,
    ]
    return messages
