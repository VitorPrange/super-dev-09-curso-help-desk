# Front-end Helpdesk — estado e convenções

> Ponto de partida da pasta `docs/`. Registra **o que já está implementado**, **as convenções
> adotadas** e **o que falta**, para que qualquer sessão de trabalho recomece daqui.
>
> Última atualização: 28/09/2026.

---

## Documentos desta pasta

| Documento | Para que serve |
|---|---|
| `README.md` (este) | Estado do front, convenções e próximos passos. |
| `api-acoes-ticket.md` | Contrato da API das ações **definir prioridade**, **resolver** e **cancelar**: corpo, regras, formatos de erro e matriz status × ação. |
| `componente-modal.md` | Componente genérico `app-modal` (`shared/modal`): título, corpo projetado e botões de rodapé. |
| `componente-definir-prioridade.md` | API do componente `app-definir-prioridade`, o **molde** das modais de ação. |
| `componentes-resolver-cancelar.md` | API de `app-resolver` e `app-cancelar`, com a tabela de diferenças entre os dois. |

---

## Ambiente

| | |
|---|---|
| Front | `npm start` em `front-end/` → `http://localhost:4200` |
| API | `uvicorn app.main:app --reload` em `api/` → `http://localhost:8000` (Swagger em `/docs`) |
| Banco | MySQL local, `DATABASE_URL` no `.env` da API |
| CORS | A API libera **somente** `http://localhost:4200` |
| Tipagem | `npx ng build` — compila os templates (AOT), é o que pega erro de binding |

Angular 21, componentes **standalone**, `signal`/`input`/`output`, controle de fluxo `@if`/`@for`
no template e `FormsModule` (`ngModel`) para formulários. Não há `environment`: a URL da API está
fixa nos services. Não há autenticação: o usuário que executa a ação vai no corpo, em `idUsuario`.

---

## O que está implementado

| Tela / feature | Onde | Endpoint | Situação |
|---|---|---|---|
| Listagem de tickets | `pages/tickets/listar` | `GET /tickets`, `GET /usuarios` | ✅ Ações por status na última coluna. Coluna **Solicitante** ainda mostra `TODO`. |
| Criar ticket | `pages/tickets/cadastro` | `POST /tickets` | ✅ Rota `/tickets/cadastro`. |
| Associar atendente | modal **dentro** de `listar.html` | `POST /tickets/{id}/associar` | ✅ Padrão antigo (formulário e chamada na própria tela). |
| Definir prioridade | `pages/tickets/definir-prioridade` | `POST /tickets/{id}/definir-prioridade` | ✅ Componente próprio. |
| Resolver | `pages/tickets/resolver` | `POST /tickets/{id}/resolver` | ✅ Componente próprio. |
| Cancelar | `pages/tickets/cancelar` | `POST /tickets/{id}/cancelar` | ✅ Componente próprio. |
| Modal genérica | `shared/modal` | — | ✅ Ver `componente-modal.md`. |
| Detalhes do ticket | `pages/tickets/detalhes` | — | ⛔ Só o esqueleto do `ng generate` (`detalhes works!`), sem rota. |

Com isso, **as cinco ações de ticket da API estão cobertas pelo front**.

### Definir prioridade (28/09/2026)

- `models/tickets.model.ts`: interface `TicketDefinirPrioridade`; corrigido o typo
  `dataAtualizaco` → `dataAtualizacao` em `TicketResposta`.
- `services/ticket.service.ts`: `definirPrioridade(id, dado)`.
- `pages/tickets/definir-prioridade/`: componente novo — ver `componente-definir-prioridade.md`.
- `listar.ts`: `ticketSelecionado` passou de `signal<number | null>` para
  `signal<TicketResposta | null>` — por isso `abrirModalAssociar(ticket)` recebe o objeto e
  `associar()` usa `.id`.

### Resolver e cancelar (28/09/2026)

- `models/tickets.model.ts`: interfaces `TicketResolver` e `TicketCancelar`.
- `services/ticket.service.ts`: `resolver(id, dado)` e `cancelar(id, dado)`.
- `pages/tickets/resolver/` e `pages/tickets/cancelar/`: componentes novos — ver
  `componentes-resolver-cancelar.md`.
- `listar.ts`: sinais `modalResolverAberta`/`modalCancelarAberta`, os `abrirModal*` e os
  `aoResolver`/`aoCancelar`. A atualização da linha virou o método `atualizarLista(ticket)`,
  usado pelas três ações.
- `listar.html`: `(click)` nos botões *Resolver* e *Cancelar* e as duas tags novas no fim.
- **Estilo do formulário extraído** para a classe global `.form-modal` em `src/styles.scss`
  (eram quatro modais repetindo as mesmas regras). `listar.scss` perdeu o bloco `.form-associar`
  e os `.scss` dos três componentes de ação ficaram só com `:host { display: contents; }`.
  O estado desabilitado dos botões do rodapé virou uma regra única em `modal.scss`.

Verificado: `npx ng build` passa. Contra a API rodando, foram conferidos os erros que os
componentes exibem — `403` de papel errado, `403` de atendente não associado, `422` de regra de
negócio (cancelar ticket resolvido) e `422` do Pydantic para texto curto. O clique de ponta a
ponta no navegador é validado pelo autor do projeto.

---

## Convenções adotadas

### 1. Cada ação de ticket é um componente próprio e autônomo

```
pages/tickets/<acao>/<acao>.ts|.html|.scss     ← sem rota, usado por composição
```

O componente contém a modal, o formulário, a **chamada da API** e o tratamento de erro. A tela que
o usa informa apenas `[aberto]`, `[ticket]` e `[usuarios]`, e recebe de volta o ticket já
atualizado na saída de sucesso. Motivo: evitar que `listar.ts` acumule quatro formulários e quatro
chamadas de serviço.

> A modal de **associar** é a exceção histórica — foi feita antes dessa decisão e continua dentro
> de `listar.html`. Vale migrá-la quando houver oportunidade, não como urgência.

### 2. A lista de usuários vem por input

`listar.ts` já faz `GET /usuarios` no `ngOnInit`; as modais recebem a lista completa em
`[usuarios]` e decidem internamente o que fazer com ela (filtrar por papel, achar o atendente do
ticket, ou usar inteira). Evita repetir a mesma request.

### 3. Quem fecha a modal é a tela, nunca o componente

O componente só emite. É o que mantém a modal aberta quando a API devolve erro, preservando o que
foi digitado.

### 4. Erro da API aparece dentro da modal; sucesso usa `alert()`

A mensagem sai de `erro.error?.mensagem` (formato dos erros de domínio) com fallback genérico
para o formato do Pydantic. O `alert()` de sucesso é o padrão herdado das telas existentes.

### 5. Atualizar a linha, não recarregar a lista

As ações devolvem o `TicketResposta` completo, então a tela usa `atualizarLista(ticket)`
(`listar.ts`) em vez de um novo `GET /tickets`.

### 6. `[ngValue]` em `<option>`, não `[value]`

Mantém `idUsuario` como `number` no corpo da requisição. As telas antigas (`cadastro`, `associar`)
ainda usam `[value]` e só funcionam porque o Pydantic converte `"2"` → `2`.

### 7. Validar os limites de texto no formulário

Os campos de texto das ações têm mínimo de 10 e máximo de 1000 caracteres na API. O front valida
antes de enviar (e usa `maxlength` no `textarea`), para o usuário não receber a mensagem em inglês
do Pydantic.

### 8. Formulário de modal usa a classe global `.form-modal`

Definida em `src/styles.scss`: rótulos, `select`, `textarea`, grupo de radios (`.opcoes`/`.opcao`),
campo somente leitura (`.valor-fixo`), contador (`.contador`) e mensagem de erro (`.erro`).
Global porque o corpo da modal é conteúdo projetado e cada ação é um componente diferente.

---

## Próximos passos

- Coluna **Solicitante** da listagem mostra `TODO` — a API devolve `solicitanteId`, o nome sai do
  cruzamento com `usuarios()`.
- Tela de **detalhes** do ticket: só o esqueleto, sem rota. O número do protocolo na listagem já
  tem estilo de link (`.link`) esperando por ela.
- **Visibilidade das ações**: hoje *Definir Prioridade*, *Resolver* e *Cancelar* só aparecem em
  `EM_ANALISE`. A API é mais permissiva (aceita definir prioridade em qualquer status e cancelar
  em `ABERTO`) — ver a matriz em `api-acoes-ticket.md`. É decisão de produto.
- Migrar a modal de **associar** para componente próprio, seguindo a convenção 1.
- Trocar a URL fixa dos services por `environment`.
- Trocar os `alert()` de sucesso por algo menos intrusivo (toast), se for desejado.
