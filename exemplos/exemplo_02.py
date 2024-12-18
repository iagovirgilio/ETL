"""Módulo para fazer requisições HTTP."""
import requests

URL = "https://jsonplaceholder.typicode.com/comments"
PARAMS = {"postId": 1}
resposta = requests.get(url=URL, params=PARAMS, timeout=5)
data = resposta.json()

print(f"Foram encontrados {len(data)} comentários.")
print(f"Erro: {resposta.status_code} - {resposta.text}")
