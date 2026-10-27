from sqlalchemy import Column, Float, Integer, DateTime
from datetime import datetime
from database import Base

class LeituraSensorModel(Base):
    # O __tablename__  é o nome exato da tabela no MySQL
    __tablename__ = "leituras_sensores"  # (Substitua pelo nome exato do BANCO)

    
    # Cada coluna aqui precisa corresponder exatamente ao BANCO, trocar pelo nomes exatos das colunas
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    temperatura = Column(Float, nullable=False)
    umidade = Column(Float, nullable=False)
    valorAr = Column(Integer, nullable=False)
    luminosidade = Column(Float, nullable=False)
    distancia = Column(Float, nullable=False)
    pressao = Column(Float, nullable=False)

    
    # Exemplo de data e hora do registro
    criado_em = Column(DateTime, default=datetime.utcnow)