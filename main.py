from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, create_tables
from models import Empresa, EmpresaCreate, ObrigacaoAcessoria, ObrigacaoAcessoriaCreate, EmpresaDB, ObrigacaoAcessoriaDB
from typing import List

create_tables()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/empresas/", response_model=Empresa)
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    
    if not empresa.telefone:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Telefone é obrigatório"
        )

    db_empresa_existente = db.query(EmpresaDB).filter(EmpresaDB.cnpj == empresa.cnpj).first()
    if db_empresa_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CNPJ já cadastrado"
        )

    db_empresa = EmpresaDB(
        nome=empresa.nome,
        cnpj=empresa.cnpj,
        endereco=empresa.endereco,
        email=empresa.email,
        telefone=empresa.telefone
    )
    try:
        db.add(db_empresa)
        db.commit()  
        db.refresh(db_empresa)  
    except IntegrityError:
        db.rollback()  
        raise HTTPException(status_code=500, detail="Erro ao salvar no banco de dados")
    
    return db_empresa  

@app.get("/empresas/", response_model=List[Empresa])
def get_empresas(db: Session = Depends(get_db)):
    empresas = db.query(EmpresaDB).all()
    return empresas

@app.post("/obrigacoes/", response_model=ObrigacaoAcessoria)
def create_obrigacao(obrigacao: ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_obrigacao = ObrigacaoAcessoriaDB(
        nome=obrigacao.nome, 
        periodicidade=obrigacao.periodicidade, 
        empresa_id=obrigacao.empresa_id
    )
    try:
        db.add(db_obrigacao)
        db.commit()
        db.refresh(db_obrigacao)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar obrigação")
    return db_obrigacao
