# categoria_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.repositories.base import RepositorioBase


class CategoriaRepository(RepositorioBase[Categoria]):
    def __init__(self, db: Session):
        super().__init__(db, Categoria)

    # Utilizado para validar que não existe uma categoria 
    # já cadastrada com aquele nome
    def obter_por_nome(self, nome: str) -> Categoria | None:
        return self.db.scalar(select(Categoria).where(Categoria.nome == nome))

    def listar_todos(self) -> list[Categoria]:
        return list(self.db.scalars(select(Categoria).where(Categoria.ativa == True)).all())