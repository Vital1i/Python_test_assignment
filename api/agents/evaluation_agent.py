from autogen import AssistantAgent


class EvaluationAgent(AssistantAgent):
    def evaluate_responses(self, questions: list[str], responses: list[str]) -> dict:
        scores = []
        feedback = []
        for question, response in zip(questions, responses):
            prompt = f"Evaluate this response:\nQuestion: {question}\nResponse: {response}"
            result = self.run(prompt).splitlines()
            scores.append(int(result[0]))
            feedback.append(result[1])
        return {"scores": scores, "feedback": feedback}

