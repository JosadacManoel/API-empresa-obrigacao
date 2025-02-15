from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from typing import Optional

class EmpresaModel(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cnpj = Column(String, unique=True, index=True)
    endereco = Column(String)
    email = Column(String)
    telefone = Column(String)

    obrigacoes = relationship("ObrigacaoAcessoriaModel", back_populates="empresa")


class ObrigacaoAcessoriaModel(Base):
    __tablename__ = "obrigacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    periodicidade = Column(String)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    empresa = relationship("EmpresaModel", back_populates="obrigacoes")


class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: Optional[str] = None


class EmpresaCreate(EmpresaBase):
    pass


class Empresa(EmpresaBase):
    id: int

    class Config:
        orm_mode = True


class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str


class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    pass

class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int
    empresa: Empresa

    class Config:
        orm_mode = True
