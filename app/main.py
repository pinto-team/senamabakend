from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.mongo import ensure_indexes
from app.routers.partners import router as partners_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler
    - Startup logic
    - Shutdown logic (if needed later)
    """
    # ---- Startup ----
    ensure_indexes()

    yield

    # ---- Shutdown ----
    # (اینجا اگر خواستی بعداً connection رو ببندی)


app = FastAPI(
    title="CRM Backend",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(partners_router)
