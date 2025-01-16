import autogen
from api.agents.initializer import initializer
from api.agents.question_agent import question_agent
from api.agents_interactions.interaction_for_questions import (
    state_transition_question)

groupchat_for_questions = autogen.GroupChat(
    agents=[initializer, question_agent],
    messages=[],
    max_round=20,
    speaker_selection_method=state_transition_question,
)
