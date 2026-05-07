from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.database import Base


class Inscricao(Base):
    __tablename__ = "inscricoes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id"), nullable=False)

    projeto: Mapped[str] = mapped_column(String(100), nullable=False)
    curso: Mapped[str] = mapped_column(String(255), nullable=False)
    ano: Mapped[int] = mapped_column(nullable=False)

    status: Mapped[str] = mapped_column(String(50), default="inscrito")
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    aluno = relationship("Aluno", back_populates="inscricoes")