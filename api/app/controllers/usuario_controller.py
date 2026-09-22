from fastapi import APIRouter, Depends

from app.dependencies.database import DbSession
from app.schemas.usuario_schema import UsuarioCriar, UsuarioEditar, UsuarioListar
from app.services.usuario_service import UsuarioService


router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post(
    "",
    summary="Cadastrar usuário",
    response_model=UsuarioListar
)
def criar(dado: UsuarioCriar, db:DbSession):
    return UsuarioService(db).criar(dado)


@router.get(
    "",
    summary="Listar usuários",
    response_model=list[UsuarioListar],
)
def listar(db: DbSession):
    return UsuarioService(db).listar()


@router.put("/{id}")
def editar(id: int, dado: UsuarioEditar, db: DbSession):
    return UsuarioService(db).editar(id, dado)


@router.get(
    "/{id}",
    summary="Consultar usuário filtrando por id",
    response_model=UsuarioListar
)
def consultar_por_id(id: int, db: DbSession):
    return UsuarioService(db).obter_por_id(id)


@router.delete(
    "/{id}",
    summary="Apagar usuário filtrando por id",
    response_model=UsuarioListar
)
def apagar(id: int, db: DbSession):
    return UsuarioService(db).apagar(id)
