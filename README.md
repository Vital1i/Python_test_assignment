# Python Test Assignment

## Overview
This project demonstrates a FastAPI-based application for managing candidate interviews, generating interview questions, and assessing candidate responses. The application provides a seamless workflow for evaluating candidates and storing interview data.

## Features
- RESTful APIs for managing candidates and interviews.
- Automated generation of interview questions based on candidate job titles.
- Assessment of candidate responses with detailed evaluation summaries.
- Persistent storage of interview data.

---

## Getting Started

### Prerequisites
Ensure you have Python 3.10+ installed on your system.

### Installation

Follow these steps to install and run the application on Windows and macOS.

---

#### **Windows Installation**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Vital1i/Python_test_assignment
   cd Python_test_assignment
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` File**
   Create a `.env` file in the project root and add your `OPENAI_API_KEY`:
   ```plaintext
   OPENAI_API_KEY=<your_openai_api_key>
   ```
   You can obtain your OpenAI API key by following the instructions [here](https://platform.openai.com/signup/).

5. **Apply Migrations**
   Apply the generated migration to create the database schema:
   ```bash
   alembic upgrade head
   ```

6. **Run the Application**
   ```bash
   uvicorn api.main:app --port=8000 --reload
   ```

7. **Access API Documentation**
   Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the API endpoints.

---

#### **macOS Installation**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Vital1i/Python_test_assignment
   cd Python_test_assignment
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Alembic for Database Migrations**
   ```bash
   pip install alembic
   ```

5. **Create a `.env` File**
   Create a `.env` file in the project root and add your `OPENAI_API_KEY`:
   ```plaintext
   OPENAI_API_KEY=<your_openai_api_key>
   ```
   You can obtain your OpenAI API key by following the instructions [here](https://platform.openai.com/signup/).

6. **Initialize Alembic**
   Set up Alembic for database migrations:
   ```bash
   alembic init migrations
   ```

7. **Configure Alembic**
   Update the `alembic.ini` file to set the `sqlalchemy.url` to your database URL (e.g., `sqlite:///./database.db`).

8. **Generate Initial Migration**
   Create a migration script to generate the tables:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

9. **Apply Migrations**
   Apply the generated migration to create the database schema:
   ```bash
   alembic upgrade head
   ```

10. **Run the Application**
   ```bash
   python3 -m uvicorn api.main:app --port=8000 --reload
   ```

11. **Access API Documentation**
   Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the API endpoints.

---



### Notes

- Ensure you have `Python 3.10` or newer installed on your system.
- If you encounter any issues with permissions, try running commands with `sudo` (macOS) or as Administrator (Windows).
- To stop the application, press `Ctrl+C` in the terminal where the server is running.


## Usage

### 1. View Existing Candidates
Five pre-inserted candidates are available with IDs ranging from `1` to `5`. Use the `Get Candidates` endpoint to view their data.

### 2. Generate Interview Questions
To generate interview questions for a candidate:
- Use the `start_task` endpoint with the candidate's `id`.
- Example response:
   ```json
   {
     "message": "Questions generated successfully",
     "questions": [
       {
         "id": 145,
         "text": "1. Can you explain the difference between supervised and unsupervised learning in machine learning? Can you provide examples of when each type of learning would be used in a data science project?"
       },
       {
         "id": 146,
         "text": "2. How would you approach feature selection and engineering in a machine learning project? Can you discuss the importance of selecting the right features and how it can impact the model's performance?"
       },
       {
         "id": 147,
         "text": "3. When evaluating the performance of a machine learning model, what metrics would you consider and why? How would you interpret these metrics to make decisions about model improvement or deployment?"
       }
     ],
     "interview_log_id": 56
   }
   ```

### 3. Assess Candidate Responses
To evaluate the candidate's responses:
- Use the `continue_chat` endpoint with the `interview_log_id` and the candidate's responses in this format:
   ```json
   {
     "responses": [
       "1. Supervised learning is a type of machine learning where the model is trained on a labeled dataset...",
       "2. Feature selection and engineering are critical steps in a machine learning project...",
       "3. When evaluating the performance of a machine learning model, metrics depend on the task..."
     ]
   }
   ```

  - Example evaluation response:
     ```json
    {
        "message": "Interview completed",
        "summary": [
        "## Summary Report:",
        "### Interview Questions:\n1. **Can you explain the difference between supervised and unsupervised learning in machine learning? Can you provide examples of when each type of learning would be used in a data science project?**\n2. **How would you approach feature selection and engineering in a machine learning project? Can you discuss the importance of selecting the right features and how it can impact the model's performance?**\n3. **When evaluating the performance of a machine learning model, what metrics would you consider and why? How would you interpret these metrics to make decisions about model improvement or deployment?**",
        "### Candidate's Responses and Scores:\n1. The candidate provided a clear explanation of supervised and unsupervised learning with relevant examples.  \n   **Score: 5/5**  \n   *Feedback: The response demonstrated a strong understanding of the concepts.*",
        "2. The candidate elaborated on feature selection and engineering, emphasizing their importance and impact on model performance.  \n   **Score: 5/5**  \n   *Feedback: The response was comprehensive and highlighted specific techniques and benefits.*",
        "3. The candidate showcased a good understanding of performance evaluation metrics, their relevance, and interpretation for model decisions.  \n   **Score: 5/5**  \n   *Feedback: The response correctly identified common metrics and their significance.*",
        "### Overall Conclusion:\nThe candidate displayed a solid grasp of fundamental machine learning concepts, methodologies, and evaluation metrics. Their explanations were thorough, showcasing a strong understanding of the subject matter. The candidate's responses were articulate, demonstrating proficiency in explaining complex concepts. Based on the responses provided, the candidate would be a valuable asset in a data science role requiring expertise in machine learning principles.",
        "The candidate is highly recommended for further consideration in the data science position based on their excellent performance during the interview."
        ]
    }
   ```

### 4. Access Interview Data
- Questions: Stored in the `interviews` folder as `interview_{interview.id}_questions_candidate№{candidate.id}.json`.
- Evaluations: Stored as `interview_{interview.id}_data.json`.

## Folder Structure
- `api/`: Contains the main FastAPI application files.
- `api/models.py`: Defines database models for candidates, questions, and interviews.
- `api/schemas.py`: Includes data validation and response models.
- `utils/prepopulate.py`: Utility script for database population of starting data.
- `interviews/`: Stores interview questions and evaluation logs.
- `api/agents/`: Includes agents for generating questions and evaluating answers
- `api/agents_interactions/`: Includes how agents communicate between each others in each case
- `api/groupchats/`: Include configurations for agents in each case
- `api/config/`: Include configuration of LLM.

## Short Write-Up

### Approach
- **MAIN IDEA**: Approach of two different endpoints: one for generating questions, one for evaluating answers was justified by modular implementation of the task.
### Key Design Decisions
- **AutoGen**: Used for configuring agents and managing the logic for generating questions and evaluating responses. I chose it cause it give the opportunity to quickly configure agents and their communication.
- **OPEN AI GPT**: Utilized as the LLM for generating interview questions and assessing responses.
### Challenges and Solutions
- **Prompt Engineering**: Crafting effective prompts for GPT API to generate relevant questions was an iterative process. It was very important to give a strict rules for agents so that returned predictable result's structure

---