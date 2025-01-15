# user makes a POST /query { "message": "What's the weather?" }
import os
from urllib import request

import autogen

from api.agents.evaluation_agent import EvaluationAgent
from api.agents.question_agent import QuestionAgent


async def post_query():
  message = request.form.get("message")

  user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    code_execution_config=False,
    is_termination_msg=lambda message: True # Always True
  )
  question_assistant = QuestionAgent(
    name="weather_assistant",
    system_message="""You're a helpful assistant to set 3 questions for user.
    It need to be based on user job description""",
    llm_config=
      {
          "config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}],
      },
  )
  evaluation_assistant = EvaluationAgent(
      name="weather_assistant",
      system_message="""You're a helpful assistant to set 3 questions for user.
      It need to be based on user job description""",
      llm_config=
      {
          "config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}],
      },
  )

  groupchat = autogen.GroupChat(
    agents=[question_assistant, user_proxy, evaluation_assistant],
    messages=[]
  )
  validator = autogen.GroupChatManager(
    name="Manager",
    groupchat=groupchat,
    llm_config=
      {
          "config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}],
      },
  )

  await user_proxy.a_initiate_chat(validator, message=message)

  return groupchat.messages[-1]