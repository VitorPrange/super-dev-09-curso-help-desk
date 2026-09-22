from sqlalchemy.orm import Session

from app.core.exceptions import ConflitoError, NaoEncontradoError
from app.core.security import hash_senha
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioCriar, UsuarioEditar

class UsuarioService:
    def __init__(self, db: Session):
        self.db = db
        self.usuario_repository = UsuarioRepository(db)

    def criar(self, dado: UsuarioCriar) -> Usuario:
        if self.usuario_repository.consultar_por_email(dado.email) is not None:
            raise ConflitoError(f"E-mail '{dado.email}' já cadastrado")

        usuario = Usuario(
            nome=dado.nome,
            email=dado.email,
            senha_hash=hash_senha(dado.senha),
            papel=dado.papel,
            ativo=True
        )
        self.usuario_repository.adicionar(usuario)
        self.db.commit()
        return usuario

    def listar(self) -> list[Usuario]:
        return self.usuario_repository.listar_todos()

    def editar(self, id: int, dado: UsuarioEditar) -> Usuario:
        usuario = self.usuario_repository.obter_por_id(id)

        if usuario is None:
            raise NaoEncontradoError("Usuário não encontrado")

        usuario.nome = dado.nome
        usuario.email = dado.email
        usuario.papel = dado.papel
        usuario.senha_hash = hash_senha(dado.senha)

        self.db.commit()
        return usuario

    def obter_por_id(self, id: int) -> Usuario:
        usuario = self.usuario_repository.obter_por_id(id)

        if usuario is None:
            raise NaoEncontradoError("Usuário não encontrado")

        if usuario.ativo == False:
            raise NaoEncontradoError("Usuário não encontrado")

        return usuario


    def apagar(self, id: int) -> Usuario:
        """Soft delete: marca `ativo=False`. O registro continua no 
        banco para manter histórico"""
        usuario = self.usuario_repository.obter_por_id(id)

        if usuario is None:
            raise NaoEncontradoError("Usuário não encontrado")

        usuario.ativo = False
        self.db.commit()
        return usuario