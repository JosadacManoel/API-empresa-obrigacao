from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:JMF%4023demaio@localhost:5432/empresa_obrigacao_db"

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Conexão com o banco de dados bem-sucedida!")
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)
