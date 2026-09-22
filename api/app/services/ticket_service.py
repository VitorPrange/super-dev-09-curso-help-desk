from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.enums import Papel, StatusChamado
from app.core.exceptions import PermissaoNegadaError, RegraNegocioError, NaoEncontradoError
from app.core.tempo import agora
from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket_schema import TicketCancelar, TicketCriar, TicketDefinirPrioridade, TicketAssociar, TicketResolver
from app.services.usuario_service import UsuarioService


class TicketService:
    def __init__(self, db: Session):
        self.db = db
        self.ticket_repository = TicketRepository(db)
        self.usuario_service = UsuarioService(db)

    def __gerar_numero_protocolo(self, ticket: Ticket) -> str:
        data_criacao = ticket.data_criacao.strftime("%Y%m%d")
        numero = str(ticket.id).zfill(5)

        return f"{data_criacao}-{numero}"

    def criar(self, dado: TicketCriar) -> Ticket:
        # Validar que o usuário existe efetivamente
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)
        if usuario.papel != Papel.SOLICITANTE:
            raise PermissaoNegadaError("Tickets podem ser abertos somente por SOLICITANTE")

        numero_protocolo_fake = str(uuid4())[:20] # gerar numero de protocolo fake

        ticket = Ticket(
            titulo=dado.titulo,
            descricao=dado.descricao,
            setor=dado.setor,
            solicitante_id=dado.id_usuario,
            status=StatusChamado.ABERTO,
            numero_protocolo=numero_protocolo_fake
        )
        self.ticket_repository.adicionar(ticket)
        # envia um insert para o banco sem fazer commit
        # depois o id estara disponivel pois o banco de dados ja gerou o id com auto increment
        self.db.flush()

        numero_protocolo = self.__gerar_numero_protocolo(ticket)

        ticket.numero_protocolo = numero_protocolo

        self.db.commit()
        return ticket


    def obter_por_id(self, id: int) -> Ticket:
        ticket = self.ticket_repository.obter_por_id(id)
        if ticket is None:
            raise NaoEncontradoError("Ticket não encontrado")
        return ticket

    def definir_prioridade(self, id: int, dado: TicketDefinirPrioridade) -> Ticket:
        # buscar ticket no banco e valida que existe
        ticket = self.obter_por_id(id)

        #buscar usuario no banco e valida se existe
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)

        #verificar se papel do usuario é ATENDENTE pois so ele pode abrir tickets
        if usuario.papel != Papel.ATENDENTE:
            raise PermissaoNegadaError("Ticket pode ser definido prioridade somente por ATENDENTE")

        ticket.prioridade = dado.prioridade

        ticket.data_atualizacao = agora()

        # salva as modificações
        self.db.commit()
        return ticket

    def associar(self, id: int, dado: TicketAssociar) -> Ticket:
        ticket = self.obter_por_id(id)
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)
        if usuario.papel != Papel.ATENDENTE:
            raise PermissaoNegadaError("Somente usuario com papel ATENDENTE pode ser atribuidos a ticket")

        if ticket.status != StatusChamado.ABERTO:
            raise RegraNegocioError("Somente tickets abertos podem ser associados")

        ticket.atendente_id = dado.id_usuario
        ticket.status =  StatusChamado.EM_ANALISE
        ticket.data_atualizacao = agora()
        self.db.commit()

        return ticket

    def listar(self) -> list[Ticket]:
        return self.ticket_repository.listar_todos()

    def resolver(self, id: int, dado: TicketResolver) -> Ticket:
        ticket = self.obter_por_id(id)
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)
        if usuario.papel != Papel.ATENDENTE:
            raise PermissaoNegadaError("Somente usuarios com papel ATENDENTE pode resolver o ticket")

        if ticket.atendente_id != dado.id_usuario:
            raise PermissaoNegadaError("Somente o atendente associado pode resolver este ticket")

        if ticket.status != StatusChamado.EM_ANALISE:
            raise RegraNegocioError("Somente tickets em analise podem ser resolvidos")

        ticket.descricao_solucao = dado.descricao
        ticket.status = StatusChamado.RESOLVIDO
        ticket.data_atualizacao = agora()
        self.db.commit()

        return ticket

    def cancelar(self, id: int, dado: TicketCancelar) -> Ticket:
        ticket = self.obter_por_id(id)
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)

        if ticket.status == StatusChamado.RESOLVIDO:
            raise RegraNegocioError("Ticket resolvidos não podem ser cancelados")

        if ticket.status == StatusChamado.CANCELADO:
            raise RegraNegocioError("Ticket ja esta cancelado")

        ticket.motivo_cancelamento = dado.motivo
        ticket.status = StatusChamado.CANCELADO
        ticket.data_atualizacao = agora()
        self.db.commit()
        return ticket