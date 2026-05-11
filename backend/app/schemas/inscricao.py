from pydantic import BaseModel, EmailStr
from typing import Optional


class InscricaoCreate(BaseModel):
    nome: str
    cpf: str
    email: Optional[str] = None
    telefone: Optional[str] = None

    projeto: str
    curso: str
    ano: int


class InscricaoResponse(BaseModel):
    id: int
    aluno_id: int
    projeto: str
    curso: str
    ano: int
    status: str

    class Config:
        from_attributes = True


class HistoricoInscricao(BaseModel):
    projeto: str
    curso: str
    ano: int
    status: str

    class Config:
        from_attributes = True


class InscricaoComAlerta(BaseModel):
    inscricao: InscricaoResponse
    aluno_ja_existia: bool
    historico_anterior: list[HistoricoInscricao]