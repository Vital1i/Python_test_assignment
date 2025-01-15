from api.agents.initializer import initializer
from api.agents.question_agent import question_agent


# State transition logic for asking questions
def state_transition_question(last_speaker, groupchat):
    messages = groupchat.messages

    if last_speaker is initializer:
        return question_agent
    elif last_speaker is question_agent:
        return None