# api/routes/candidate.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.models import Candidate
from utils.schemas import CandidateResponse, CandidateCreate
from utils.storage import get_db

router = APIRouter()


@router.get("/candidates", response_model=list[CandidateResponse])
async def get_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()
    return candidates


@router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: str, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.candidate_id == candidate_id).first()
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@router.post("/candidates", response_model=CandidateResponse)
async def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    new_candidate = Candidate(**candidate.dict())
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate
