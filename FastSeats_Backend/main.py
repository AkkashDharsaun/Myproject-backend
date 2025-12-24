from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from database import engine
from models import Base
from routes.auth_routes import router as auth_router

# Load env
load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url if frontend_url else "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router)

# 🔥 HEALTH CHECK (RENDER NEEDS THIS)
@app.get("/")
def health_check():
    return {"status": "FastSeats backend running"}

