# utils/schemas.py
from pydantic import BaseModel
from datetime import datetime


class CandidateBase(BaseModel):
    candidate_id: str
    name: str
    email: str
    job_title: str


class CandidateCreate(CandidateBase):
    pass


class CandidateResponse(CandidateBase):
    created_at: datetime

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    text: str


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class EvaluationBase(BaseModel):
    score: int
    feedback: str


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationResponse(EvaluationBase):
    id: int
    interview_log_id: int
    question_id: int

    class Config:
        orm_mode = True


class InterviewLogBase(BaseModel):
    job_title: str
    questions: str  # Store as JSON string
    responses: str  # Store as JSON string
    scores: str  # Store as JSON string
    feedback: str  # Store feedback summary


class InterviewLogCreate(InterviewLogBase):
    pass


class InterviewLogResponse(InterviewLogBase):
    id: int
    candidate_id: int
    timestamp: datetime

    class Config:
        orm_mode = True