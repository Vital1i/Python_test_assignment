import autogen

from config.gpt_config import gpt4_config

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