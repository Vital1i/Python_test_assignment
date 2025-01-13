# api/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from utils.storage import get_db, create_all_tables
from utils.prepopulate import prepopulate_candidates  # Import the prepopulate function
from .routes.candidates import router as candidate_router  # Import candidate router

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Create tables if they don't exist yet
    create_all_tables()

    # Pre-populate candidates in the database
    db = next(get_db())
    prepopulate_candidates(db)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Interview System"}

# Register routes
app.include_router(candidate_router)  # Include the candidate router
