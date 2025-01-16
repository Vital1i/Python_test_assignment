from api.agents.evaluation_agent import evaluation_agent
from api.agents.initializer import initializer
from api.agents.validation_agent import validator


# State transition logic for analyzing answering
def state_transition_answer(last_speaker, groupchat):

    if last_speaker is initializer:
        return evaluation_agent
    elif last_speaker is evaluation_agent:
        return validator
    elif last_speaker is validator:
        return None
