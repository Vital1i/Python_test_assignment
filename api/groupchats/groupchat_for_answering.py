# GroupChat setup
import autogen

from api.agents.evaluation_agent import evaluation_agent
from api.agents.initializer import initializer
from api.agents.validation_agent import validator
from api.agents_interactions.interactions_for_answers import state_transition_answer


groupchat_for_answering = autogen.GroupChat(
    agents=[initializer, evaluation_agent, validator],
    messages=[],
    max_round=20,
    speaker_selection_method=state_transition_answer,
)