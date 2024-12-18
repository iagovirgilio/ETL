"""Módulo para fazer requisições HTTP."""
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
