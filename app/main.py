from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.partners import router as partners_router

app = FastAPI(root_path="/crm-api")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # یا ["*"] برای همه (فقط برای توسعه)
    allow_credentials=True,
    allow_methods=["*"],            # GET, POST, PUT, DELETE, ...
    allow_headers=["*"],
)

app.include_router(partners_router)
