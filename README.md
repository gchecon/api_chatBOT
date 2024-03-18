Para criar uma API básica que comunica com a GPT-4-turbo da OpenAI, você pode utilizar o framework FastAPI por sua simplicidade e desempenho. Este exemplo demonstrará como configurar um endpoint simples que recebe um texto via POST, envia esse texto para a GPT-4-turbo, e retorna a resposta gerada. 

### Passos Preliminares:

1. Instale o FastAPI e Uvicorn (um servidor ASGI) para rodar sua aplicação. Você também precisará da biblioteca `openai` para comunicar com a GPT-4-turbo.
   
   ```bash
   pip install fastapi uvicorn openai
   ```

2. Crie um arquivo, por exemplo, `main.py`, e adicione o seguinte código. Lembre-se de substituir `"your_openai_api_key"` pela sua chave API da OpenAI.

### Código da API:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# Configuração da chave da API da OpenAI
openai.api_key = 'your_openai_api_key'

app = FastAPI()

class Query(BaseModel):
    text: str
    max_tokens: int = 50
    temperature: float = 0.5

@app.post("/query/")
async def query_model(query: Query):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Verifique se a GPT-4-turbo é "text-davinci-003" ou outro nome
            prompt=query.text,
            max_tokens=query.max_tokens,
            temperature=query.temperature
        )
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

```

### Instruções de Uso:

1. Execute a API localmente usando Uvicorn com o seguinte comando:
   
   ```bash
   uvicorn main:app --reload
   ```
   
   O argumento `--reload` faz com que o servidor reinicie automaticamente após mudanças no código. É útil durante o desenvolvimento, mas deve ser removido em ambientes de produção.

2. Com a API rodando, você pode testá-la usando uma ferramenta como o Insomnia ou Postman, fazendo uma requisição POST para `http://127.0.0.1:8000/query/` com um JSON no corpo da requisição, por exemplo:

   ```json
   {
     "text": "Quais são as principais notícias de hoje?",
     "max_tokens": 100,
     "temperature": 0.5
   }
   ```

3. A API enviará essa pergunta para a GPT-4-turbo e retornará a resposta gerada.

### Observações:

- **Segurança da API Key**: No exemplo acima, a chave API é inserida diretamente no código. Para uma aplicação real, é recomendado utilizar variáveis de ambiente ou sistemas de gerenciamento de segredos para armazenar chaves API.
- **Configuração do Modelo**: Verifique as últimas documentações da OpenAI para garantir que está utilizando o identificador correto do modelo e ajustar parâmetros conforme necessário.
- **Erros e Exceções**: A gestão de erros no código é básica. Em uma aplicação em produção, você deve expandir o tratamento de erros para cobrir casos específicos e possivelmente registrar esses erros para análise futura.

Com essas orientações, você pode começar a desenvolver sua API para interagir com a GPT-4-turbo e expandi-la conforme as necessidades do seu projeto.
