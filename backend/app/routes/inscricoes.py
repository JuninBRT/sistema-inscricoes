from datetime import datetime
import re

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aluno import Aluno
from app.models.inscricao import Inscricao
from app.schemas.inscricao import (
    ConsultaInscricoesResponse,
    InscricaoCreate,
    InscricaoComAlerta,
)


router = APIRouter(prefix="/inscricoes", tags=["Inscrições"])


def normalizar_cpf(cpf: str) -> str:
    return re.sub(r"\D", "", cpf or "")


def montar_historico(aluno: Aluno) -> list[Inscricao]:
    return sorted(
        aluno.inscricoes,
        key=lambda inscricao: inscricao.criado_em or datetime.min,
        reverse=True,
    )


@router.post("/", response_model=InscricaoComAlerta)
def criar_inscricao(dados: InscricaoCreate, db: Session = Depends(get_db)):
    cpf = normalizar_cpf(dados.cpf)

    if not dados.nome.strip():
        raise HTTPException(status_code=400, detail="Nome é obrigatório")

    if not cpf:
        raise HTTPException(status_code=400, detail="CPF é obrigatório")

    if not dados.projeto.strip():
        raise HTTPException(status_code=400, detail="Projeto é obrigatório")

    if not dados.curso.strip():
        raise HTTPException(status_code=400, detail="Curso é obrigatório")

    aluno = db.query(Aluno).filter(Aluno.cpf == cpf).first()

    aluno_ja_existia = aluno is not None
    historico_anterior = []

    if aluno:
        historico_anterior = montar_historico(aluno)
        aluno.nome = dados.nome
        aluno.email = dados.email or aluno.email
        aluno.telefone = dados.telefone or aluno.telefone
    else:
        aluno = Aluno(
            nome=dados.nome,
            cpf=cpf,
            email=dados.email,
            telefone=dados.telefone,
        )
        db.add(aluno)
        db.commit()
        db.refresh(aluno)

    inscricao = Inscricao(
        aluno_id=aluno.id,
        projeto=dados.projeto,
        curso=dados.curso,
        ano=dados.ano or datetime.now().year,
        respostas=dados.respostas,
        status="inscrito",
    )

    db.add(inscricao)
    db.commit()
    db.refresh(inscricao)

    return {
        "inscricao": inscricao,
        "aluno_ja_existia": aluno_ja_existia,
        "historico_anterior": historico_anterior,
    }


@router.get("/consulta", response_model=ConsultaInscricoesResponse)
def consultar_inscricoes(
    nome: str | None = Query(default=None),
    cpf: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    cpf_normalizado = normalizar_cpf(cpf or "")
    nome_normalizado = (nome or "").strip()

    if not cpf_normalizado and not nome_normalizado:
        raise HTTPException(
            status_code=400,
            detail="Informe nome ou CPF para consultar inscrições anteriores",
        )

    consulta = db.query(Aluno)

    if cpf_normalizado:
        consulta = consulta.filter(Aluno.cpf == cpf_normalizado)

    if nome_normalizado:
        consulta = consulta.filter(Aluno.nome.ilike(f"%{nome_normalizado}%"))

    alunos = consulta.limit(20).all()

    return {
        "resultados": [
            {"aluno": aluno, "historico": montar_historico(aluno)}
            for aluno in alunos
        ]
    }


@router.get("/")
def listar_inscricoes(db: Session = Depends(get_db)):
    return db.query(Inscricao).all()
