from autogen.agentchat import AssistantAgent, GroupChat


# Define the Question Agent
class QuestionAgent(AssistantAgent):
    def generate_questions(self, job_description: str) -> list[str]:
        prompt = f"Generate three interview questions based on this job description:\n{job_description}"
        response = self.send(prompt)
        return response.splitlines()