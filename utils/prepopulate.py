from sqlalchemy.orm import Session
from utils.models import Candidate
from utils.storage import get_db


def prepopulate_candidates(db: Session):
    candidates_data = [
        {"candidate_id": "candidate_1", "name": "Alice Johnson", "email": "alice@example.com",
         "job_title": "Backend Developer"},
        {"candidate_id": "candidate_2", "name": "Bob Smith", "email": "bob@example.com",
         "job_title": "Frontend Developer"},
        {"candidate_id": "candidate_3", "name": "Charlie Lee", "email": "charlie@example.com",
         "job_title": "Data Scientist"},
        {"candidate_id": "candidate_4", "name": "Diana Moore", "email": "diana@example.com",
         "job_title": "Product Manager"},
        {"candidate_id": "candidate_5", "name": "Eve Davis", "email": "eve@example.com", "job_title": "QA Engineer"}
    ]

    for candidate in candidates_data:
        db_candidate = db.query(Candidate).filter(Candidate.candidate_id == candidate["candidate_id"]).first()
        if not db_candidate:
            db_candidate = Candidate(**candidate)
            db.add(db_candidate)
    db.commit()
    print("Pre-populated candidates.")
