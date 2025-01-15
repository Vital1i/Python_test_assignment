import autogen
from config.gpt_config import gpt4_config

question_agent = autogen.AssistantAgent(
    name="QuestionAgent",
    llm_config=gpt4_config,
    system_message="""You are the Question Agent. Given a job description, generate three interview questions to assess relevant skills. All question should be on theory.""",
)