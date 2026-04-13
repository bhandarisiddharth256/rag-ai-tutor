from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(query, context):
    try:
        prompt = f"""
            You are an AI tutor.

            Answer the question using ONLY the given context.

            Rules:
            - Be concise and clear (1–3 sentences max)
            - Do NOT add information not present in context
            - If answer is not found, say:
            "I could not find this in the document."

            Context:
            {context}

            Question:
            {query}

            Answer:
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # 🔥 best for you
            messages=[
                {"role": "system", "content": "You are a helpful AI tutor that answers strictly from given context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=100 
        )

        return response.choices[0].message.content

    except Exception as e:
        print("LLM Error:", e)
        return context[:500]