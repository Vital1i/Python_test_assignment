import json
import autogen

from typing import Dict
from fastapi import FastAPI, HTTPException, Body, Depends
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from api.agents.initializer import initializer
from api.groupchats.groupchat_for_answering import groupchat_for_answering
from api.groupchats.groupchat_for_questions import groupchat_for_questions
from config.gpt_config import gpt4_config
from save_data_to_file import save_to_local
from utils.prepopulate import prepopulate_candidates
from .schemas import CandidateResponse
from .storage import get_db, create_all_tables
from .models import Candidate, InterviewLog, Question, InterviewLogQuestion


load_dotenv()


app = FastAPI()


# Initialize the chat
@app.post("/start_chat/{candidate_id}/")
async def start_chat(candidate_id: int, db: Session = Depends(get_db)):

    # Fetch candidate by ID
    candidate = (
        db.query(Candidate).filter(
            Candidate.candidate_id == candidate_id
        ).first()
    )
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate_job_title = candidate.job_title

    # Initialize chat to generate questions
    initializer_message = f"Job description: {candidate_job_title}"

    manager = autogen.GroupChatManager(
        groupchat=groupchat_for_questions, llm_config=gpt4_config
    )

    initializer.initiate_chat(manager, message=initializer_message)

    # Extract generated questions and split them into individual questions
    question_text = [
        msg["content"]
        for msg in groupchat_for_questions.messages
        if msg["name"] == "QuestionAgent"
    ]

    # Split each question into a list of questions by newline
    questions = []
    for text in question_text:
        # Split the text into individual questions
        questions.extend(text.split("\n"))

    # Create separate Question objects for each question
    question_objects = []
    for question_text in questions:
        question = Question(text=question_text)
        db.add(question)
        db.flush()  # Get the ID of the question after insertion
        question_objects.append(question)

    # Save the interview log to the database
    interview_log = InterviewLog(
        candidate_id=candidate.id,
        job_title=candidate_job_title,
        responses="[]",
        scores="[]",
        feedback="[]",
    )
    db.add(interview_log)
    db.commit()

    for question in question_objects:
        interview_log_question = InterviewLogQuestion(
            interview_log_id=interview_log.id, question_id=question.id
        )
        db.add(interview_log_question)

    db.commit()

    questions_data = {
        "questions": [{"id": q.id, "text": q.text} for q in question_objects]
    }
    file_name = (
        f"interview_{interview_log.id}_questions_candidate№{candidate_id}.json"
    )
    # Save the questions as a JSON file
    await save_to_local(file_name, questions_data)

    return {
        "message": "Questions generated successfully",
        "questions": [
            {"id": q.id, "text": q.text} for q in question_objects
        ],  # Include each question with its ID
        "interview_log_id": interview_log.id,
    }


# Continue the chat
@app.post("/continue_chat/{interview_log_id}/")
async def continue_chat(
    interview_log_id: int,
    responses: Dict[str, list[str]] = Body(...),
    db: Session = Depends(get_db),
):
    # Fetch the interview log based on interview_log_id
    interview_log = (
        db.query(InterviewLog).filter(
            InterviewLog.id == interview_log_id
        ).first()
    )
    if not interview_log:
        raise HTTPException(status_code=404, detail="Interview log not found")

    # Fetch the questions associated with this interview log
    interview_log_questions = (
        db.query(InterviewLogQuestion)
        .filter(InterviewLogQuestion.interview_log_id == interview_log_id)
        .all()
    )
    if not interview_log_questions:
        raise HTTPException(
            status_code=404, detail="No questions found for this interview log"
        )

    responses = responses["responses"]

    # Retrieve the question texts using the question_ids
    # from the InterviewLogQuestion table
    question_texts = []
    for interview_log_question in interview_log_questions:
        question = (
            db.query(Question)
            .filter(Question.id == interview_log_question.question_id)
            .first()
        )
        if question:
            question_texts.append(question.text)

    # Make sure we have questions available
    if not question_texts:
        raise HTTPException(status_code=404, detail="No valid questions found")

    # Format the user message by combining questions
    # and their respective responses
    user_message = ", ".join(
        [
            f"Response to question ('{question}'): {response}"
            for question, response in zip(question_texts, responses)
        ]
    )

    manager = autogen.GroupChatManager(
        groupchat=groupchat_for_answering, llm_config=gpt4_config
    )

    # Send the user responses along with the questions in the group chat
    initializer.initiate_chat(manager, message=user_message)

    # Run the group chat and get the final summary from the Validator agent
    final_summary = [
        msg["content"]
        for msg in groupchat_for_answering.messages
        if msg["name"] == "Validator"
    ][
        -1
    ]  # Get the last message from the Validator agent
    final_summary = final_summary.split("\n\n")

    # Save the responses and feedback to the interview log
    interview_log.responses = json.dumps(responses)

    file_name = f"interview_{interview_log_id}_data.json"
    await save_to_local(
        file_name, final_summary
    )  # Save the responses, feedback, and scores

    # Commit changes to the database
    db.commit()

    return {"message": "Interview completed", "summary": final_summary}


@app.on_event("startup")
async def startup_event():
    # Pre-populate the candidates in the database
    db = next(get_db())
    prepopulate_candidates(db)

    # Create tables if they don't exist yet
    create_all_tables()


@app.get("/candidates/", response_model=list[CandidateResponse])
async def get_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()
    return candidates


@app.get("/candidates/{candidate_id}/", response_model=CandidateResponse)
async def get_candidate(candidate_id: str, db: Session = Depends(get_db)):
    candidate = (
        db.query(Candidate).filter(
            Candidate.candidate_id == candidate_id
        ).first()
    )
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate
