"""Módulo para fazer requisições HTTP."""
import requests

URL = "https://api.coinbase.com/v2/prices/spot"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "MinhaAplicacao/1.0"
}
PARAMS = {
    "currency": "USD"
}

resposta = requests.get(url=URL, params=PARAMS, headers=HEADERS, timeout=5)
data = resposta.json()

print("Preço do Bitcoin em USD:", data["data"]["amount"])
