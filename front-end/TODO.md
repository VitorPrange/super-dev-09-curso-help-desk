ver docs/README.md para o estado atual (o que ja foi implementado e o que falta)

criar o componente
adicionar rota no app.routes
adicionar link(routerLink) na lista para tela de criar
criar model
criar service
componente
    implementar o ts
    implementar o html


Criar
    -> descrição    textarea
    -> id usuário   select permitir o usuário escolher o solicitante
    -> setor        type radio [ADMINISTRATIVO, MANUTENCAO, FINANCEIRO, RH, TI]
    -> titulo       input

    -> botão de criar ticket

    Ao criar o ticket o back define o status como ABERTO

Associar
    -> id ticket
    -> id usuário   select permitir o usuário escolher o atendente

    -> botão Associar

    Ao associar o ticket ao atendente e o status como EM_ANALISE

Definir Prioridade:
    -> id ticket
    -> id usuário   select permitir o usuário escolher o atendente
    -> prioridade   type radio [BAIXO, MEDIA, ALTA]
    -> botão Definir Prioridade

    Ao definir a prioridade atualiza a prioridade

Resolver
    -> id ticket
    -> id usuário   select
    -> descrição    text area
    -> botão Resolver

    Ao resolver o ticket recebe o status RESOLVIDO o atualiza a descrição

Cancelar
    -> id ticket
    -> id usuario   select
    -> motivo       textarea
    -> botão cancelar

    Ao resolver o ticket recebe o status CANCELADO o atualiza o motivo
