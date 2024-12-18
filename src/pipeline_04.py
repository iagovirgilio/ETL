"""
Pipeline 04: Extração, transformação e salvamento de dados do Bitcoin.

Este módulo implementa um pipeline ETL para coletar dados de preços do Bitcoin
da API Coinbase e salvá-los em um banco de dados PostgreSQL.
"""
from datetime import datetime
from logging import getLogger, basicConfig
import logging
import os
import time
import requests

import logfire
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, BitcoinPreco

# Configuração Logfire
logfire.configure()
logfire_handler = logfire.LogfireLoggingHandler()  # Cria uma instância do handler
logfire_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))  # Define um formatador
basicConfig(handlers=[logfire_handler])  # Usa a instância do handler
logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logfire.instrument_requests()
logfire.instrument_sqlalchemy()

# Carregar variáveis de ambiente
load_dotenv()

# Lê as variáveis de ambiente
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Cria a sessão do SQLAlchemy
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
    logger.info("Dados salvos com sucesso no banco de dados")


if __name__ == "__main__":
    criar_tabela()  # Chama a função para criar a tabela
    while True:
        try:
            dados_json = extract_dados_bitcoin()
            if dados_json:
                dados_transformados = transform_dados_bitcoin(dados_json)
                logger.info("Dados transformados: %s", dados_transformados)
                salvar_dados_postgres(dados_transformados)
            time.sleep(15)
        except KeyboardInterrupt:
            logger.info("Pipeline interrompido pelo usuário.")
            break
        except requests.RequestException as e:
            logger.error("Erro na requisição HTTP: %s", e)
        except (ValueError, KeyError) as e:
            logger.error("Erro ao processar dados: %s", e)
