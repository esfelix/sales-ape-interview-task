from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.auth import router as auth_router
from src.api.routes.chat import router as chat_router
from src.db import init_db

app = FastAPI(title="SalesApe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()


app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the SalesApe Task API"}
