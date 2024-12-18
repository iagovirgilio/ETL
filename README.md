# Exemplo de Requisição HTTP para a API da OpenAI

Este exemplo demonstra como fazer uma requisição HTTP para a API da OpenAI usando Python. O script utiliza a biblioteca `requests` para enviar uma solicitação POST e obter uma resposta de um modelo de linguagem.

## Pré-requisitos

- Python 3.x
- Biblioteca `requests`
- Biblioteca `python-dotenv` para carregar variáveis de ambiente de um arquivo `.env`

## Configuração

1. Instale as bibliotecas necessárias:
   ```bash
   pip install requests python-dotenv
   ```

2. Crie um arquivo `.env` na raiz do seu projeto e adicione sua chave de API da OpenAI:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Uso

O script faz uma requisição para a API da OpenAI com o modelo `gpt-3.5-turbo` e uma mensagem de exemplo. A resposta da API é impressa no console.

### Código de Exemplo

```python
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}

DATA = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "Você é um assistente virtual."},
        {"role": "user", "content": "Qual é a capital do Brasil?"}
    ]
}

resposta = requests.post(url=URL, headers=HEADERS, data=json.dumps(DATA), timeout=5)

data = resposta.json()

print("Resposta da API OpenAI:", data["choices"][0]["message"]["content"])
```

## Notas

- Certifique-se de que sua chave de API está correta e que você tem acesso à internet para que a requisição seja bem-sucedida.
- O tempo limite (`timeout`) para a requisição está definido como 5 segundos, mas pode ser ajustado conforme necessário.

## Licença

Este projeto é apenas um exemplo e não possui uma licença específica.
