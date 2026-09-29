from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.enums import Papel, StatusChamado
from app.core.exceptions import NaoEncontradoError, PermissaoNegadaError, RegraNegocioError
from app.core.tempo import agora
from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket_schema import TicketAssociar, TicketCancelar, TicketCriar, TicketDefinirPrioridade, TicketResolver
from app.services.usuario_service import UsuarioService


class TicketService:
    def __init__(self, db: Session):
        self.db = db
        self.ticket_repository = TicketRepository(db)
        self.usuario_service = UsuarioService(db)

    def __gerar_numero_protocolo(self, ticket: Ticket) -> str:
        data_criacao = ticket.data_criacao.strftime("%Y%m%d") #ANOMESDIA
        numero = str(ticket.id).zfill(5) # ticket 1 => 00001
        return f"{data_criacao}-{numero}"


    def criar(self, dado: TicketCriar) -> Ticket:
        # Validar que o usuário existe efetivamente
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)
        if usuario.papel != Papel.SOLICITANTE:
            raise PermissaoNegadaError("Tickets podem ser abertos somente por SOLICITANTE")

        # gerar um numero protocolo fake
        numero_protocolo_fake = str(uuid4())[:20]

        ticket = Ticket(
            titulo=dado.titulo,
            descricao=dado.descricao,
            setor=dado.setor,
            solicitante_id=dado.id_usuario,
            status=StatusChamado.ABERTO,
            numero_protocolo=numero_protocolo_fake
        )
        self.ticket_repository.adicionar(ticket)

        # Envia o INSERT para o banco de dados sem fazer o commit.
        # Depois desta chamada o id do ticket estará disponível pois o banco 
        # de dados já gerou o id com AUTO_INCREMENT
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
        # buscar o ticket do banco de dados, validando q o mesmo existe
        ticket = self.obter_por_id(id)
        # definir a prioridade do ticket

        # buscar o usuário do banco de dados, validando que o mesmo existe
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)
        # verificar que o usuário tem o papel de ATENDENTE, pois o ticket pode ser 
        # resolvido somente por um ATENDENTE
        if usuario.papel != Papel.ATENDENTE:
            raise PermissaoNegadaError("Ticket pode ser definido prioridade somente por ATENDENTE")

        ticket.prioridade = dado.prioridade
        ticket.data_atualizacao = agora()
        # Salvar as modificações do ticket
        self.db.commit()
        return ticket

    def associar(self, id: int, dado: TicketAssociar) -> Ticket:
        ticket = self.obter_por_id(id)
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)
        if usuario.papel != Papel.ATENDENTE:
            raise PermissaoNegadaError("Somente usuário com papel " \
            "ATENDENTE podem ser atribuidos a ticket")

        if ticket.status != StatusChamado.ABERTO:
            raise RegraNegocioError("Somente tickets abertos podem ser associados")

        ticket.atendente_id = dado.id_usuario
        ticket.status = StatusChamado.EM_ANALISE
        ticket.data_atualizacao = agora()
        self.db.commit()

        return ticket

    def listar(self) -> list[Ticket]:
        return self.ticket_repository.listar_todos()

    def resolver(self, id: int, dado: TicketResolver) -> Ticket:
        ticket = self.obter_por_id(id)
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)
        if usuario.papel != Papel.ATENDENTE:
            raise PermissaoNegadaError("Somente usuário com papel ATENDENTE pode resolver o ticket")

        if ticket.atendente_id != dado.id_usuario:
            raise PermissaoNegadaError("Somente o atendente associado pode resolver este ticket")

        if ticket.status != StatusChamado.EM_ANALISE:
            raise RegraNegocioError("Somente tickets em análise podem ser resolvidos")
        
        ticket.descricao_solucao = dado.descricao
        ticket.status = StatusChamado.RESOLVIDO
        ticket.data_atualizacao = agora()
        self.db.commit()

        return ticket

    def cancelar(self, id: int, dado: TicketCancelar) -> Ticket:
        ticket = self.obter_por_id(id)
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)

        if ticket.status == StatusChamado.RESOLVIDO:
            raise RegraNegocioError("Tickets resolvidos não podem ser cancelados")

        if ticket.status == StatusChamado.CANCELADO:
            raise RegraNegocioError("Ticket já está cancelado")
        
        ticket.motivo_cancelamento = dado.motivo
        ticket.status = StatusChamado.CANCELADO
        ticket.data_atualizacao = agora()
        self.db.commit()
        return ticket