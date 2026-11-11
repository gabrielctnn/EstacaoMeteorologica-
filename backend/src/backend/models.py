from sqlalchemy import Column, Float, Integer, DateTime, ForeignKey, String
from datetime import datetime
from database import Base

class LeituraSensorModel(Base):
    # O __tablename__  é o nome exato da tabela no MySQL
    __tablename__ = "leituras_sensores" 
    id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, index=True, nullable=False)
    temperatura = Column(Float, nullable=True)
    umidade = Column(Float, nullable=True)
    valorAr = Column(Integer, nullable=False)
    luminosidade = Column(Float, nullable=False)
    precipitacao = Column(Float, nullable=False)
    pressao = Column(Float, nullable=False)
    qualidadeArStatus = Column(String(50), nullable=False) # <--- Coluna nova no banco

    
    # data e hora do registro
    criado_em = Column(DateTime, default=datetime.utcnow)