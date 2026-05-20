from typing import Any

from pydantic import BaseModel, ConfigDict


class InscricaoCreate(BaseModel):
    nome: str
    cpf: str
    email: str | None = None
    telefone: str | None = None

    projeto: str
    curso: str
    ano: int | None = None
    respostas: dict[str, Any] | None = None


class FromAttributesModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class InscricaoResponse(FromAttributesModel):
    id: int
    aluno_id: int
    projeto: str
    curso: str
    ano: int
    status: str
    respostas: dict[str, Any] | None = None


class HistoricoInscricao(FromAttributesModel):
    projeto: str
    curso: str
    ano: int
    status: str
    respostas: dict[str, Any] | None = None


class InscricaoComAlerta(BaseModel):
    inscricao: InscricaoResponse
    aluno_ja_existia: bool
    historico_anterior: list[HistoricoInscricao]


class AlunoConsulta(FromAttributesModel):
    id: int
    nome: str
    cpf: str
    email: str | None = None
    telefone: str | None = None


class AlunoComHistorico(BaseModel):
    aluno: AlunoConsulta
    historico: list[HistoricoInscricao]


class ConsultaInscricoesResponse(BaseModel):
    resultados: list[AlunoComHistorico]
