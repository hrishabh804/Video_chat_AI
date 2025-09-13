import openai
from . import config

# Configure OpenAI API key
openai.api_key = config.OPENAI_API_KEY

class AIService:
    def __init__(self, job_role: str):
        self.job_role = job_role
        self.question_index = 0
        self.questions = [
            "Tell me about yourself.",
            f"Why are you interested in the {self.job_role} role?",
            "Describe your experience with a challenging project.",
            "What are your greatest strengths and weaknesses?",
            "Where do you see yourself in 5 years?",
            "Do you have any questions for me?"
        ]

    def get_initial_question(self) -> str:
        """
        Returns the first question of the interview.
        """
        self.question_index = 0
        return self.questions[0]

    async def get_next_question(self, user_response: str) -> str:
        """
        Generates the next question based on the user's response.
        For now, it just moves to the next question in the list.
        """
        # Simple scoring based on response length
        score = len(user_response.split())

        # In a real scenario, you would use GPT-4 for dynamic follow-ups
        # For example:
        # completion = await openai.ChatCompletion.acreate(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system", "content": f"You are an interviewer for a {self.job_role} role."},
        #         {"role": "user", "content": f"My previous answer was: {user_response}. Ask a follow-up question."}
        #     ]
        # )
        # next_question = completion.choices[0].message.content

        self.question_index += 1
        if self.question_index < len(self.questions):
            return self.questions[self.question_index]
        else:
            return "Thank you for your time. The interview is now complete."

    def calculate_score(self, responses: list) -> dict:
        """
        Calculates a simple score based on the length of responses.
        """
        total_words = sum(len(r.split()) for r in responses)
        average_words = total_words / len(responses) if responses else 0
        return {"total_words": total_words, "average_words_per_response": average_words}
