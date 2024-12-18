"""Módulo para definir a estrutura do banco de dados."""
from datetime import datetime
from sqlalchemy import Column, Float, String, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BitcoinPreco(Base):
    """Classe para definir a estrutura da tabela bitcoin_precos."""

    __tablename__ = "bitcoin_precos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False)
    criptomoeda = Column(String, nullable=False)
    moeda = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
