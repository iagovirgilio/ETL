"""Módulo para fazer requisições HTTP."""
import requests

URL = "https://jsonplaceholder.typicode.com/posts/1"
resposta = requests.get(URL, timeout=5)
data = resposta.json()

print(data)
