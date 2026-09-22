from enum import Enum


class Papel(str, Enum):
    ATENDENTE = "ATENDENTE"
    SOLICITANTE = "SOLICITANTE"


class StatusChamado(str, Enum):
    ABERTO = "ABERTO"
    EM_ANALISE = "EM_ANALISE"
    RESOLVIDO = "RESOLVIDO"
    CANCELADO = "CANCELADO"


class PrioridadeChamado(str, Enum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"


class SetorChamado(str, Enum):
    TI = "TI"
    RH = "RH"
    FINANCEIRO = "FINANCEIRO"
    ADMINISTRATIVO = "ADMINISTRATIVO"
    MANUTENCAO = "MANUTENCAO"
