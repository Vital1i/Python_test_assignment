import time
import random
from fastapi import FastAPI, HTTPException, Body, Depends, Query
import os
from dotenv import load_dotenv
import autogen
from sqlalchemy.orm import Session
import json
from utils.models import Candidate, InterviewLog, Question, InterviewLogQuestion
from utils.prepopulate import prepopulate_candidates
from utils.schemas import CandidateResponse
from utils.storage import get_db, create_all_tables

load_dotenv()

app = FastAPI()
# Define LLM configuration
gpt4_config = {
    "cache_seed": int(time.time()) + random.randint(1, 1000),  # Change the cache_seed for different trials
    "temperature": 0.7,
    "config_list": [
        {"model": "gpt-3.5-turbo", "api_key": os.environ.get("OPENAI_API_KEY")}
    ],
    "timeout": 120,
}

# Define agents
initializer = autogen.UserProxyAgent(
    name="Init",
    code_execution_config={
        "use_docker": False
    },
)

question_agent = autogen.AssistantAgent(
    name="QuestionAgent",
    llm_config=gpt4_config,
    system_message="""You are the Question Agent. Given a job description, generate three interview questions to assess relevant skills. All question should be on theory.""",
)

evaluation_agent = autogen.AssistantAgent(
    name="EvaluationAgent",
    llm_config=gpt4_config,
    system_message="""You are the Evaluation Agent. Given a candidate's responses to questions, provide a score (1–5) and feedback for each response. If candidate do not know answer it is 1.""",
)

validator = autogen.AssistantAgent(
    name="Validator",
    llm_config=gpt4_config,
    system_message="""
You are the Validation Agent. Your tasks are as follows:
1. Review the scores and feedback provided by the Evaluation Agent.
2. Confirm or adjust the scores based on the responses and feedback.
3. Generate a concise summary report that includes:
   - The interview questions
   - The candidate's responses
   - The scores for each response
   - Feedback for each response
4. Generate overall conclusion of interview
5. Ensure the report is clear, professional, and free of errors.
"""
)


def state_transition_question(last_speaker, groupchat):
    messages = groupchat.messages

    if last_speaker is initializer:
        # Init --> Question Agent
        return question_agent
    elif last_speaker is question_agent:
        # Question Agent --> Evaluation Agent
        return None


# State transition logic
def state_transition_answer(last_speaker, groupchat):
    messages = groupchat.messages

    if last_speaker is initializer:
        # Init --> Question Agent
        return evaluation_agent
    elif last_speaker is evaluation_agent:
        # Evaluation Agent --> Validator
        return validator
    elif last_speaker is validator:
        # Validator --> End
        return None


# GroupChat setup

groupchat = autogen.GroupChat(
    agents=[initializer, evaluation_agent, validator],
    messages=[],
    max_round=20,
    speaker_selection_method=state_transition_answer,
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)


# Initialize the chat
@app.post("/start_task/{candidate_id}")
async def start_task(candidate_id: int, db: Session = Depends(get_db)):
    try:
        # Fetch candidate by ID
        candidate = db.query(Candidate).filter(Candidate.candidate_id == candidate_id).first()
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        candidate_job_title = candidate.job_title

        # Initialize chat to generate questions
        initializer_message = f"Job description: {candidate_job_title}"

        groupchat_getting_messages = autogen.GroupChat(
            agents=[initializer, question_agent],
            messages=[],
            max_round=20,
            speaker_selection_method=state_transition_question,
        )

        manager1 = autogen.GroupChatManager(groupchat=groupchat_getting_messages, llm_config=gpt4_config)

        initializer.initiate_chat(
            manager1, message=initializer_message
        )

        # Extract generated questions and split them into individual questions
        question_text = [
            msg["content"] for msg in groupchat_getting_messages.messages if msg["name"] == "QuestionAgent"
        ]

        # Split each question into a list of questions by newline
        questions = []
        for text in question_text:
            questions.extend(text.split("\n"))  # Split the text into individual questions

        # Create separate Question objects for each question
        question_objects = []
        for question_text in questions:
            question = Question(text=question_text)
            db.add(question)
            db.flush()  # Get the ID of the question after insertion
            question_objects.append(question)

        # Save the interview log to the database
        interview_log = InterviewLog(
            candidate_id=candidate.id,  # Link interview to candidate
            job_title=candidate_job_title,
            responses="[]",  # Placeholder for responses
            scores="[]",  # Placeholder for scores
            feedback="[]",  # Placeholder for feedback
        )
        db.add(interview_log)
        db.commit()
        print(interview_log.id)
        for question in question_objects:
            interview_log_question = InterviewLogQuestion(
                interview_log_id=interview_log.id,
                question_id=question.id
            )
            db.add(interview_log_question)

        db.commit()

        # Return the generated questions and interview log details
        return {
            "message": "Questions generated successfully",
            "questions": [{"id": q.id, "text": q.text} for q in question_objects],  # Include each question with its ID
            "interview_log_id": interview_log.id
        }
    except Exception as e:
        db.rollback()  # Rollback in case of any errors
        raise HTTPException(status_code=404, detail=str(e))


# Continue the chat
@app.post("/continue_chat/{interview_log_id}")
async def continue_chat(interview_log_id: int, db: Session = Depends(get_db)):
    try:
        # Fetch the interview log based on interview_log_id
        interview_log = db.query(InterviewLog).filter(InterviewLog.id == interview_log_id).first()
        if not interview_log:
            raise HTTPException(status_code=404, detail="Interview log not found")

        print(interview_log_id)
        print([i.interview_log_id for i in db.query(InterviewLogQuestion).all()])
        # Fetch the questions associated with this interview log
        interview_log_questions = db.query(InterviewLogQuestion).filter(InterviewLogQuestion.interview_log_id == interview_log_id).all()
        if not interview_log_questions:
            raise HTTPException(status_code=404, detail="No questions found for this interview log")

        # Retrieve the question texts using the question_ids from the InterviewLogQuestion table
        question_texts = []
        for interview_log_question in interview_log_questions:
            question = db.query(Question).filter(Question.id == interview_log_question.question_id).first()
            if question:
                question_texts.append(question.text)

        # Make sure we have questions available
        if not question_texts:
            raise HTTPException(status_code=404, detail="No valid questions found")

        # Example responses (replace with actual responses as needed)
        responses = [
            "Django is a full-stack framework with built-in features, while Flask is lightweight and more flexible.",
            "ORM in Django provides an abstraction layer to interact with the database using Python objects.",
            "Using select_related and prefetch_related helps optimize database queries in Django."
        ]

        # Format the user message by combining questions and their respective responses
        user_message = ", ".join([f"Response to question ('{question}'): {response}"
                                  for question, response in zip(question_texts, responses)])

        # Send the user responses along with the questions in the group chat
        initializer.initiate_chat(manager, message=user_message)

        # Run the group chat and get the final summary from the Validator agent
        final_summary = [
            msg["content"] for msg in groupchat.messages if msg["name"] == "Validator"
        ][-1]  # Get the last message from the Validator agent
        print(groupchat.messages)
        final_summary = final_summary.split('\n\n')

        # Save the responses and feedback to the interview log
        interview_log.responses = json.dumps(responses)
        interview_log.scores = json.dumps(
            [
                int(msg["content"].split(":")[1].strip())  # Assuming scores follow a specific pattern
                for msg in groupchat.messages
                if msg["name"] == "Evaluator"
            ]
        )
        interview_log.feedback = json.dumps(
            [
                msg["content"]
                for msg in groupchat.messages
                if msg["name"] == "Evaluator"
            ]
        )

        # Commit changes to the database
        db.commit()

        return {"message": "Interview completed", "summary": final_summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@app.get("/candidates/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: str, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.candidate_id == candidate_id).first()
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate
