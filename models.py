from pydantic import BaseModel, validator
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from pydantic import field_validator

@field_validator('cnpj')
def validar_cnpj(cls, v):
    if len(v) != 14:
        raise ValueError("CNPJ deve ter 14 caracteres")
    return v

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str | None = None

    class Config:
        from_attributes = True

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int

    class Config:
        from_attributes = True

class EmpresaDB(Base):
    __tablename__ = 'empresas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=True)  

    obrigacoes = relationship("ObrigacaoAcessoriaDB", back_populates="empresa")

    def __repr__(self):
        return f"<Empresa(id={self.id}, nome={self.nome}, cnpj={self.cnpj})>"

class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    empresa_id: int

class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int
    empresa: Empresa

    class Config:
        from_attributes = True

class ObrigacaoAcessoriaDB(Base):
    __tablename__ = 'obrigacoes_acessoria'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    periodicidade = Column(String, nullable=False)
    empresa_id = Column(Integer, ForeignKey('empresas.id'), nullable=False)

    empresa = relationship("EmpresaDB", back_populates="obrigacoes")

    def __repr__(self):
        return f"<ObrigacaoAcessoria(id={self.id}, nome={self.nome}, periodicidade={self.periodicidade})>"
