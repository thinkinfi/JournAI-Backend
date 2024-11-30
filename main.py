import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import trips, user
from app.database import init_db

app = FastAPI()

load_dotenv()

# CORS origins
origins = [os.getenv("FRONTEND_URL"), os.getenv("FRONTEND_URL1"), os.getenv("FRONTEND_URL2")]

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(trips.router)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to the TripSaathi API"}