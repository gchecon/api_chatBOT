from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

app = FastAPI()

class Query(BaseModel):
    text: str
    max_tokens: int = 50
    temperature: float = 0.5

@app.post("/query/")
async def query_model(query: Query):
    try:
        response = client.completions.create(model="gpt-3.5-turbo-16k",  # Ou o identificador atual para a GPT-4-turbo
        prompt=query.text,
        max_tokens=query.max_tokens,
        temperature=query.temperature)
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

