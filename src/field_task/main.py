from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from field_task.database.database import initialize_database, close_database

@asynccontextmanager
async def lifespan_context(_: FastAPI):
    await initialize_database()
    yield
    await close_database()

app = FastAPI(
    title="Field Task App",
    description="Rest API",
    version="1.0.0",
    lifespan=lifespan_context,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["health"])
async def health():
    return {"message": "Api is working"}

