from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Text, Enum, DateTime
from sqlalchemy.sql.schema import ForeignKey


from app.core.database import Base
from app.core.enums import PrioridadeChamado, SetorChamado, StatusChamado
from app.core.tempo import agora


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    numero_protocolo: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    titulo: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str] = mapped_column(Text(1000), nullable=False)
    status: Mapped[StatusChamado] = mapped_column(
        Enum(StatusChamado, native_enum=False, length=20), nullable=False
    )
    prioridade: Mapped[PrioridadeChamado | None] = mapped_column(
        Enum(PrioridadeChamado, native_enum=False, length=20), nullable=True
    )
    setor: Mapped[SetorChamado] = mapped_column(
        Enum(SetorChamado, native_enum=False, length=20), nullable=False
    )
    descricao_solucao: Mapped[str | None] = mapped_column(Text(1000), nullable=True)
    motivo_cancelamento: Mapped[str | None] = mapped_column(Text(1000), nullable=True)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=agora, nullable=False)
    data_atualizacao: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    solicitante_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    atendente_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
