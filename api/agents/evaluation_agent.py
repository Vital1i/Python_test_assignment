import autogen
from config.gpt_config import gpt4_config

prompt = """You are the Evaluation Agent.
    Given a candidate's responses to questions,
    provide a score (1–5) and feedback for each response.
    If candidate do not know answer it is 1."""

evaluation_agent = autogen.AssistantAgent(
    name="EvaluationAgent",
    llm_config=gpt4_config,
    system_message=prompt,
)
