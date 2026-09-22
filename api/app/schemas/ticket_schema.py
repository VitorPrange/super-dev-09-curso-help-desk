from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.core.enums import PrioridadeChamado, SetorChamado, StatusChamado


class TicketCriar(BaseModel):
    id_usuario:int = Field(alias="idUsuario")
    titulo:str = Field(min_length=3, max_length=120)
    descricao:str = Field(min_length=10)
    setor:SetorChamado

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "idUsuario": 1,
                "titulo": "PC com problema",
                "descricao": "Placa de vídeo não tem internet",
                "setor": "ADMINISTRATIVO"
            }
        }
    )



class TicketDefinirPrioridade(BaseModel):
    id_usuario: int = Field(alias="idUsuario")
    prioridade: PrioridadeChamado


class TicketAssociar(BaseModel):
    id_usuario: int = Field(alias="idUsuario")


class TicketResolver(BaseModel):
    id_usuario: int = Field(alias="idUsuario")
    descricao: str = Field(min_length=10, max_length=1000)


class TicketCancelar(BaseModel):
    id_usuario: int = Field(alias="idUsuario")
    motivo: str = Field(min_length=10, max_length=1000)


class TicketResposta(BaseModel):
    id: int
    numero_protocolo: str
    titulo: str
    descricao: str
    status: StatusChamado
    prioridade: PrioridadeChamado | None
    setor: SetorChamado
    descricao_solucao: str | None
    motivo_cancelamento: str | None
    data_criacao: datetime
    data_atualizacao: datetime | None
    solicitante_id: int
    atendente_id: int | None
