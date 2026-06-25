from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY


class AnswerGenerator:
    """
    Uses Gemini to generate answers from retrieved context.
    """

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.2,
        )

    def generate(self, question, context):
        """
        Generate final answer using retrieved context.
        """

        prompt = f"""
You are an AI assistant helping developers understand a codebase.

Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't know based on the codebase."

---

CONTEXT:
{context}

---

QUESTION:
{question}

---

Answer clearly and include file references if possible.
"""

        response = self.llm.invoke(prompt)
        return response.content