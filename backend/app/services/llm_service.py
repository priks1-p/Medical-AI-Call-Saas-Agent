from groq import Groq
from app.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def ask_ai(system_prompt, user_message):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.choices[0].message.content