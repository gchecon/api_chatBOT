import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from typing import List
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(organization=os.getenv('OPENAI_ORGANIZATION'))

app = FastAPI()


class Query(BaseModel):
    text: str
    max_tokens: int = 50
    temperature: float = 0.5


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: List[Message]


@app.post("/query/")
async def query_model(query: Query):
    try:
        response = client.completions.create(model="gpt-3.5-turbo",  # Ou o identificador atual para a GPT-4-turbo
                                             prompt=query.text,
                                             max_tokens=query.max_tokens,
                                             temperature=query.temperature)
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/")
async def chat(chat_requests: ChatRequest):
    try:
        response = client.chat.completions.create(
            model=chat_requests.model,
            messages=[message.dict() for message in chat_requests.messages]
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
