from sqlalchemy.orm import Session
from utils.models import Candidate
from utils.storage import get_db


def prepopulate_candidates(db: Session):
    candidates_data = [
        {"candidate_id": "1", "name": "Alice Johnson", "email": "alice@example.com",
         "job_title": "Junior Python Backend Developer"},
        {"candidate_id": "2", "name": "Bob Smith", "email": "bob@example.com",
         "job_title": "Junior React Frontend Developer"},
        {"candidate_id": "3", "name": "Charlie Lee", "email": "charlie@example.com",
         "job_title": "Data Scientist"},
        {"candidate_id": "4", "name": "Diana Moore", "email": "diana@example.com",
         "job_title": "Product Manager"},
        {"candidate_id": "5", "name": "Eve Davis", "email": "eve@example.com",
         "job_title": "Junior QA Engineer"}
    ]

    for candidate in candidates_data:
        db_candidate = db.query(Candidate).filter(Candidate.candidate_id == candidate["candidate_id"]).first()
        if not db_candidate:
            db_candidate = Candidate(**candidate)
            db.add(db_candidate)
    db.commit()
    print("Pre-populated candidates.")
