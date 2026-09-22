/tickets        GET

/tickets/{id}   GET

/tickets        POST
    RN: Para abrir ticket somente usuário com papel solicitante
    SIstema preenche:
        numero protocolo (gerado automagicamente)
        status => aberto
        data_criacao
    usuário preenche (PAYLOAD):
    - id_usuario
    - titulo
    - descricao
    - setor

/tickets/{id}/definir-prioridade POST
    Usuario preencher:
        id_usuario
    RN: Usuário deve conter o papel de atendente
    RN: Atualizar a data_atualizacao

/tickets/{id}/associar  POST
    usuario preenche:
        id usuario
    Sistema preenche:
        data_atualizacao

    RN: ticket n pode ser associado senão for atente
    RN: Ao associar um ticket o status deve ir para EM_ANALISE
    RN: Ticket deve estar ABERTO para poder associar
    RN: Atualizar a data_atualizacao


/tickets/{id}/resolver POST
    usuario(atendente) preencher:
        descritivo do que foi feito
    
    RN: ticket deve ter o status de EM_ANALISE para poder resolver
    RN: Status deve ser definido como resolvido
    RN: Atualizar a data_atualizacao

/tickets/{id}/cancelar POST
    RN: definir o status como "CANCELADO"
    RN: ticket n pode ser cancelado quando estiver resolvido
    RN: Atualizar a data_atualizacao

    usuario preenche(PAYLOAD):
        descricao_motivo do cancelamento
    

