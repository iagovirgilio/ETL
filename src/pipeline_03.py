"""Módulo para fazer requisições na API da Coinbase."""
from datetime import datetime
import os
import time
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, BitcoinPreco

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Cria o engine e a sessão
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def criar_tabela():
    """Cria a tabela bitcoin_precos no banco de dados."""
    Base.metadata.create_all(engine)
    print("Tabela criada com sucesso!")


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
    # Converte o timestamp Unix para um objeto datetime
    timestamp = datetime.now()  # Mantém como datetime

    resultado_transformacao = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp  # Usa datetime em vez de timestamp Unix
    }

    return resultado_transformacao


def salvar_dados_postgres(dados):
    """Salva os dados no banco de dados PostgreSQL."""
    session = Session()
    novo_registro = BitcoinPreco(**dados)
    session.add(novo_registro)
    session.commit()
    session.close()
    print(f"[{dados['timestamp']}] Dados salvos com sucesso!")


if __name__ == "__main__":
    criar_tabela()  # Chama a função para criar a tabela
    while True:
        try:
            dados_json = extract_dados_bitcoin()
            if dados_json:
                dados_transformados = transform_dados_bitcoin(dados_json)
                print("Dados tratados", dados_transformados)
                salvar_dados_postgres(dados_transformados)
            time.sleep(15)
        except KeyboardInterrupt:
            print("Pipeline interrompido pelo usuário.")
            break
        except requests.RequestException as e:
            print(f"Erro na requisição HTTP: {e}")
        except (ValueError, KeyError) as e:
            print(f"Erro ao processar dados: {e}")
