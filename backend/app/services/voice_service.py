from groq import Groq
from app.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate_ai_response(message: str):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a professional healthcare receptionist."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return completion.choices[0].message.content