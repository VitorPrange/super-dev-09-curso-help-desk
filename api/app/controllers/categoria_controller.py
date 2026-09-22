from fastapi.routing import APIRouter

from app.dependencies.database import DbSession
from app.schemas.categoria_schema import CategoriaCriar, CategoriaEditar, CategoriaResposta
from app.services.categoria_service import CategoriaService


router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get(
    "",
    summary="Lista de Categorias",
    response_model=list[CategoriaResposta]
)
def listar(db: DbSession):
    return CategoriaService(db).listar()


@router.get(
    "/{id}",
    summary="Obtém uma categoria pelo id",
    response_model=CategoriaResposta
)
def consultar_por_id(id: int, db: DbSession):
    return CategoriaService(db).obter_por_id(id)


@router.post(
    "",
    summary="Cadatrar uma categoria",
    response_model=CategoriaResposta
)
def criar(dado: CategoriaCriar, db: DbSession):
    return CategoriaService(db).criar(dado)



@router.put(
    "/{id}",
    summary="Editar uma categoria pelo id",
    response_model=CategoriaResposta
)
def editar(id: int, dado: CategoriaEditar, db: DbSession):
    return CategoriaService(db).editar(id, dado)


@router.delete(
    "/{id}",
    summary="Apagar uma categoria pelo id",
    # response_model=CategoriaResposta
)
def apagar(id: int, db: DbSession):
    return CategoriaService(db).apagar(id)
