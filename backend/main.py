from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import reading, writing, listening, speaking

app = FastAPI(title="IELTS Test Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reading.router)
app.include_router(writing.router)
app.include_router(listening.router)
app.include_router(speaking.router)
