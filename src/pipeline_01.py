"""Módulo para fazer requisições na API da Coinbase."""
from datetime import datetime
import time
import requests
from tinydb import TinyDB


def extract_dados_bitcoin():
    """Extrai os dados do Bitcoin."""
    url = "https://api.coinbase.com/v2/prices/spot"
    resposta = requests.get(url=url, timeout=5)
    dados = resposta.json()
    return dados


def transform_dados_bitcoin(dados):
    """Transforma os dados do Bitcoin."""
    valor = dados["data"]["amount"]
    criptomoeda = dados["data"]["base"]
    moeda = dados["data"]["currency"]
    timestamp = datetime.now().timestamp()

    resultado_transformacao = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }

    return resultado_transformacao


def salvar_dados_tinydb(dados, db_name="bitcoin.json"):
    """Salva os dados no banco de dados TinyDB."""
    db = TinyDB(db_name)
    db.insert(dados)
    print("Dados salvos com sucesso!")


if __name__ == "__main__":
    while True:
        dados_json = extract_dados_bitcoin()
        dados_transformados = transform_dados_bitcoin(dados_json)
        salvar_dados_tinydb(dados_transformados)
        time.sleep(15)
