from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

load_dotenv() #Carrega o arquivo .env para carregar as senhas do banco
url_banco = os.getenv("DATABASE_URL") #puxa o dado de acesso do banco
Base = declarative_base()

# O Engine (Conexao BACK->BANCO): Gerencia a conexão física com o banco usando  url_banco
connect_args = {"check_same_thread": False} if "sqlite" in url_banco else {} 
engine = create_engine(url_banco, connect_args=connect_args) #cria o nosso  


# SessionLocal (Sessão): A fábrica que abre e fecha conexões temporárias
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência para injetar a sessão nas rotas do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()