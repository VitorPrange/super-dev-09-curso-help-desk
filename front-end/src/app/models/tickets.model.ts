export interface TicketResposta{
    id: number;
    numeroProtocolo: string;
    titulo: string;
    descricao: string;
    status: string;
    prioridade: string | null;
    setor: string;
    descricaoSolucao: string | null;
    motivoCancelamento: string | null;
    dataCricacao: Date;
    dataAtualizacao: Date | null;
    solicitanteId: number;
    atendenteId: number | null;
}

export interface TicketCadastro{
    descricao: string;
    idUsuario: number | null;
    setor: string;
    titulo: string;
}

export interface TicketAssociar{
    idUsuario: number | null;
}