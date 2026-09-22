from sqlalchemy import select
from sqlalchemy.orm import Session

from typing import Generic, TypeVar

from app.core.database import Base


T = TypeVar("T", bound=Base)

class RepositorioBase(Generic[T]):
    def __init__(self, db: Session, model: type[T]):
        self.db = db
        self.model = model

    # CRUD
    def adicionar(self, objeto: T) -> T:
        """Adicionar à sessão e faz flush para o dados gerar o id (sem fazer commit)"""
        self.db.add(objeto) # INSERT
        self.db.flush() # Gerando o id
        self.db.refresh(objeto) # Definindo o id no objeto que chegou
        return objeto

    def obter_por_id(self, id: int) -> T | None:
        return self.db.get(self.model, id)

    def remover(self, objeto: T) -> None:
        self.db.delete(objeto)
        self.db.flush()

    def listar_todos(self) -> list[T]:
        # from sqlalchemy import select
        return list(self.db.scalars(select(self.model)).unique().all()) 