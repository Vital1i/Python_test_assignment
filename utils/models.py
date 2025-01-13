# utils/models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from .storage import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String, unique=True, index=True)  # Unique candidate ID
    name = Column(String, index=True)
    email = Column(String, index=True)
    job_title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    interviews = relationship("InterviewLog", back_populates="candidate")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)  # The text of the interview question
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    evaluations = relationship("Evaluation", back_populates="question")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    interview_log_id = Column(Integer, ForeignKey("interview_logs.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    score = Column(Integer)  # Score for this question response (e.g., 1 to 5)
    feedback = Column(Text)  # Feedback for the response

    # Relationships
    interview_log = relationship("InterviewLog", back_populates="evaluations")
    question = relationship("Question", back_populates="evaluations")


class InterviewLog(Base):
    __tablename__ = "interview_logs"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_title = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    questions = Column(Text)  # Store questions as JSON string
    responses = Column(Text)  # Store responses as JSON string
    scores = Column(Text)  # Store scores as JSON string
    feedback = Column(Text)  # Store feedback summary

    # Relationships
    candidate = relationship("Candidate", back_populates="interviews")
    evaluations = relationship("Evaluation", back_populates="interview_log")



