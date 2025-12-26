Access to XMLHttpRequest at 'https://myproject-backend-7684.onrender.com/registerCollege' from origin 'https://fast-seats-app-frontend.vercel.app' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.Understand this error
index-yJ_Owmq5.js:13  POST https://myproject-backend-7684.onrender.com/registerCollege net::ERR_FAILED(import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import engine
from models import Base
from routes.auth_routes import router as auth_router

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fast-seats-app-frontend.vercel.app"  # ✅ NO trailing slash
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)

@app.get("/")
def health_check():
    return {"status": "FastSeats backend running"}
