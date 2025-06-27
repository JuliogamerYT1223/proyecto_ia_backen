from decouple import config
from fastapi import APIRouter
from models.message import Message
import openai

chatbot = APIRouter()

client = openai.OpenAI(api_key=config("OPENAI_API_KEY"),base_url="https://api.deepseek.com")

@chatbot.post("/chatbot")
@chatbot.options("/chatbot")
def chatbot_response(msg: Message):
    try:
        completion = client.chat.completions.create(
            
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un asistente de restaurante."},
                {"role": "user", "content": msg.message}
            ],
            temperature=0.7,
            max_tokens=250,
        )

        response_text = completion.choices[0].message.content
        return {"response": response_text}

    except Exception as e:
        return {"response": f"Ocurrió un error: {str(e)}"}
