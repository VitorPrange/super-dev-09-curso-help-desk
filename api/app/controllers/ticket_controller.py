from fastapi.routing import APIRouter
from fastapi import status

from app.dependencies.database import DbSession
from app.schemas.ticket_schema import TicketAssociar, TicketCancelar, TicketCriar, TicketDefinirPrioridade, TicketResolver, TicketResposta
from app.services.ticket_service import TicketService


router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("", response_model=TicketResposta, status_code=status.HTTP_201_CREATED)
def criar(dado: TicketCriar, db: DbSession):
    return TicketService(db).criar(dado)


@router.post("/{id}/definir-prioridade", response_model=TicketResposta)
def definir_prioridade(id: int, dado: TicketDefinirPrioridade, db: DbSession):
    return TicketService(db).definir_prioridade(id, dado)


@router.post("/{id}/associar", response_model=TicketResposta)
def associar(id: int, dado: TicketAssociar, db: DbSession):
    return TicketService(db).associar(id, dado)


@router.get("/{id}", response_model=TicketResposta)
def obter_por_id(id: int, db: DbSession):
    return TicketService(db).obter_por_id(id)


@router.get("", response_model=list[TicketResposta])
def obter_todos(db: DbSession):
    return TicketService(db).listar()

@router.post("/{id}/resolver", response_model=TicketResposta)
def resolver(id: int, dado: TicketResolver, db: DbSession):
    return TicketService(db).resolver(id, dado)

@router.post("/{id}/cancelar", response_model=TicketResposta)
def cancelar(id: int, dado: TicketCancelar, db: DbSession):
    return TicketService(db).cancelar(id, dado)
