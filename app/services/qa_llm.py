# app/services/qa_llm.py
from google import genai
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_answer(context: str, question: str):
    prompt = f"""
You are an assistant answering questions using the provided context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text