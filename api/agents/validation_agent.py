from autogen import AssistantAgent


class ValidationAgent(AssistantAgent):
    def validate_scores(self, scores: dict) -> str:
        prompt = f"Validate these scores and provide feedback:\n{scores}"
        return self.run(prompt)