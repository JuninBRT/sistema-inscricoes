from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aluno import Aluno
from app.models.inscricao import Inscricao
from app.schemas.inscricao import InscricaoCreate, InscricaoComAlerta


router = APIRouter(prefix="/inscricoes", tags=["Inscrições"])


@router.post("/", response_model=InscricaoComAlerta)
def criar_inscricao(dados: InscricaoCreate, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.cpf == dados.cpf).first()

    aluno_ja_existia = aluno is not None
    historico_anterior = []

    if aluno:
        historico_anterior = list(aluno.inscricoes)
    else:
        aluno = Aluno(
            nome=dados.nome,
            cpf=dados.cpf,
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
        ano=dados.ano,
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


@router.get("/")
def listar_inscricoes(db: Session = Depends(get_db)):
    return db.query(Inscricao).all()