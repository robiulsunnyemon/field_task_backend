from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from field_task.database.database import initialize_database, close_database
from field_task.auth.routers.auth_routers import router as auth_router
from field_task.auth.routers.user_routes import user_router
from field_task.task.routers.task_routes import router as task_router

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



app.include_router(auth_router,prefix="/api/v1")
app.include_router(user_router,prefix="/api/v1")
app.include_router(task_router,prefix="/api/v1")
