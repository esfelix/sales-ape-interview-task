from burr.core import State, action
from openai import OpenAI

from session_store import UserSession
from spotify.spotify_utils import fetch_spotify_track
from src.ai.models import TrackRecommendation
from src.ai.prompts import track_recommendation as track_recommendation_prompt

client = OpenAI()


@action(reads=[], writes=["chat_history", "prompt"])
def human_input(state: State, prompt: str) -> tuple[dict, State]:
    chat_item = {"content": prompt, "role": "user"}
    state = state.update(prompt=prompt).append(chat_history=chat_item)
    return ({"prompt": prompt}, state)


@action(reads=["chat_history"], writes=["recommended_track", "chat_history"])
def ai_recommendation(state: State, candidate_tracks: list) -> tuple[dict, State]:
    chat_history = state["chat_history"]

    messages = list(
        track_recommendation_prompt.get_messages(
            candidate_tracks=candidate_tracks, chat_history=chat_history
        )
    )

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format=TrackRecommendation,
    )

    track_recommendation = completion.choices[0].message.parsed
    state = state.update(recommended_track=track_recommendation.track_id).append(
        chat_history={"role": "assistant", "content": track_recommendation.message}
    )
    return ({"recommendation": track_recommendation}, state)


@action(reads=["recommended_track"], writes=[])
def fetch_recommended_track(
    state: State, user_session: UserSession
) -> tuple[dict, State]:
    track_id = state["recommended_track"]

    track = fetch_spotify_track(track_id, user_session.spotify_access_token)

    return ({"track": track}, state)
