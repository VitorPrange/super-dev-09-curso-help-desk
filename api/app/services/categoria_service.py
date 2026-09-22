# categoria_service.py

from sqlalchemy.orm.session import Session

from app.core.exceptions import ConflitoError, NaoEncontradoError
from app.models.categoria import Categoria
from app.repositories.categoria_repository import CategoriaRepository
from app.schemas.categoria_schema import CategoriaCriar, CategoriaEditar


class CategoriaService:
    # construtor
    def __init__(self, db: Session):
        self.db = db
        self.categoria_repository = CategoriaRepository(db)

    def criar(self, dado: CategoriaCriar):
        categoria_existente = self.categoria_repository.obter_por_nome(dado.nome)
        if categoria_existente is not None:
            raise ConflitoError("Já existe uma categoria com este nome")

        categoria = Categoria(nome=dado.nome, descricao=dado.descricao, ativa=True)
        self.categoria_repository.adicionar(categoria)
        self.db.commit()
        return categoria

    def listar(self) -> list[Categoria]:
        return self.categoria_repository.listar_todos()

    def obter_por_id(self, id: int) -> Categoria:
        categoria = self.categoria_repository.obter_por_id(id)
        if categoria is None:
            raise NaoEncontradoError("Categoria não encontrada")
        return categoria

    def editar(self, id: int, dado: CategoriaEditar) -> Categoria:
        categoria = self.categoria_repository.obter_por_id(id)
        if categoria is None:
            raise NaoEncontradoError("Categoria não encontrada")
        categoria.nome = dado.nome
        categoria.descricao = dado.descricao
        self.db.commit()
        return categoria

    def apagar(self, id: int) -> None:
        categoria = self.categoria_repository.obter_por_id(id)
        if categoria is None:
            raise NaoEncontradoError("Categoria não encontrada")
        categoria.ativa = False
        self.db.commit()
