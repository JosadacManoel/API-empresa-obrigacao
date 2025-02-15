from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="C:/Users/josad/projetos/api-empresa-obrigacao/.env")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL is None:
    print("DATABASE_URL não encontrado, usando SQLite para testes.")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

print(f'DATABASE_URL = {SQLALCHEMY_DATABASE_URL}')

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    
    print("Criando as tabelas no banco de dados de teste...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")
