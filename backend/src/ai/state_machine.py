import os

from burr.core import ApplicationBuilder
from burr.core.action import when
from burr.core.application import Application
from burr.core.persistence import SQLLitePersister

from session_store import UserSession
from src.ai.nodes import ai_recommendation, fetch_recommended_track, human_input

db_path = os.getenv("DB_PATH", "/data/salesape_task.db")

state_persister = SQLLitePersister(db_path=db_path, table_name="agent_state")
state_persister.initialize()


def build_app(user_session: UserSession) -> Application:
    app_builder = (
        ApplicationBuilder()
        .with_actions(
            human_input,
            ai_recommendation,
            fetch_recommended_track.bind(user_session=user_session),
        )
        .with_transitions(
            (
                "human_input",
                "fetch_recommended_track",
                when(prompt="play"),
            ),
            ("human_input", "ai_recommendation"),
            ("ai_recommendation", "human_input"),
        )
        .with_state_persister(state_persister)
        .with_identifiers(app_id=user_session.chat_id)
        .initialize_from(
            initializer=state_persister,
            resume_at_next_action=True,
            default_state={"chat_history": [], "prompt": None, "recommended_track": None},
            default_entrypoint="human_input",
        )
    )
    return app_builder.build()
