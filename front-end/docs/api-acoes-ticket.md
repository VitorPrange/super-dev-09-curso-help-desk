# API — Ações do Ticket: Definir Prioridade, Resolver e Cancelar

> Análise do contrato da API para implementar as três ações no front-end.
> Fonte: `api/app/controllers/ticket_controller.py`, `api/app/schemas/ticket_schema.py`,
> `api/app/services/ticket_service.py`, `api/app/core/enums.py`, `api/app/core/exceptions.py`.
>
> **Escopo deste documento:** apenas o que é necessário para a comunicação com a API
> (rotas, corpo da requisição, resposta, regras que geram erro e o que já existe/falta no front).
> O planejamento da UI vem depois.

---

## Sumário

1. [Contexto geral](#contexto-geral)
2. [Enums](#enums)
3. [Definir Prioridade](#definir-prioridade)
4. [Resolver](#resolver)
5. [Cancelar](#cancelar)
6. [Resposta de sucesso (TicketResposta)](#resposta-de-sucesso-ticketresposta)
7. [Respostas de erro](#respostas-de-erro)
8. [Matriz status × ação](#matriz-status--ação)
9. [O que já existe no front](#o-que-já-existe-no-front)
10. [O que falta implementar](#o-que-falta-implementar)
11. [Pontos de atenção e divergências](#pontos-de-atenção-e-divergências)

---

## Contexto geral

| Item | Valor |
|---|---|
| Base URL | `http://localhost:8000` (fixo em `ticket.service.ts`) |
| Prefixo do recurso | `/tickets` |
| Método das três ações | `POST` |
| Content-Type | `application/json` |
| Autenticação | **Não existe.** O usuário que executa a ação vai no corpo, em `idUsuario` |
| CORS | A API libera somente `http://localhost:4200` (`api/app/main.py`) |
| Convenção do JSON | **camelCase** na entrada e na saída |
| Status de sucesso | `200 OK` (só `POST /tickets` retorna `201`) |

As três ações seguem exatamente o mesmo formato do `associar`, que já está implementado:
`POST /tickets/{id}/<ação>` com um corpo pequeno, devolvendo o **ticket completo e atualizado**.
Ou seja: o `TicketService` do front ganha três métodos irmãos de `associar()`, e a resposta
pode ser usada para atualizar a tela sem um novo `listar()`.

---

## Enums

Valores aceitos, exatamente como a API espera (string, maiúsculas):

| Enum | Valores |
|---|---|
| `PrioridadeChamado` | `BAIXA`, `MEDIA`, `ALTA` |
| `StatusChamado` | `ABERTO`, `EM_ANALISE`, `RESOLVIDO`, `CANCELADO` |
| `SetorChamado` | `TI`, `RH`, `FINANCEIRO`, `ADMINISTRATIVO`, `MANUTENCAO` |
| `Papel` | `ATENDENTE`, `SOLICITANTE` |

> ⚠️ O `TODO.md` cita a prioridade como `BAIXO`. O valor correto é **`BAIXA`** — qualquer
> outra string cai em erro de validação `422`.

---

## Definir Prioridade

### Requisição

```
POST /tickets/{id}/definir-prioridade
```

```json
{
  "idUsuario": 2,
  "prioridade": "ALTA"
}
```

| Campo | Tipo | Obrigatório | Validação |
|---|---|---|---|
| `idUsuario` | `number` | sim | precisa existir e estar ativo |
| `prioridade` | `string` | sim | um de `BAIXA` \| `MEDIA` \| `ALTA` |

### Regras do back-end (`definir_prioridade`)

1. O ticket precisa existir → senão `404`.
2. O usuário precisa existir e estar ativo → senão `404`.
3. O usuário precisa ter papel `ATENDENTE` → senão `403`.
4. Grava `prioridade` e `dataAtualizacao`.

### Efeito

Altera **somente** `prioridade` (e `dataAtualizacao`). **Não muda o status** e **não** exige
que o atendente seja o que está associado ao ticket.

> 🔎 **Não há validação de status neste endpoint.** A API aceita definir prioridade de um
> ticket `ABERTO`, `RESOLVIDO` ou `CANCELADO`. Quem restringe isso hoje é o front (o botão
> só aparece em `EM_ANALISE`).

---

## Resolver

### Requisição

```
POST /tickets/{id}/resolver
```

```json
{
  "idUsuario": 2,
  "descricao": "Placa de vídeo substituída e testada."
}
```

| Campo | Tipo | Obrigatório | Validação |
|---|---|---|---|
| `idUsuario` | `number` | sim | precisa existir e estar ativo |
| `descricao` | `string` | sim | **mínimo 10** e **máximo 1000** caracteres |

### Regras do back-end (`resolver`)

1. O ticket precisa existir → senão `404`.
2. O usuário precisa existir e estar ativo → senão `404`.
3. O usuário precisa ter papel `ATENDENTE` → senão `403`.
4. `ticket.atendenteId` precisa ser **igual** a `idUsuario` → senão `403`
   ("Somente o atendente associado pode resolver este ticket").
5. O status precisa ser `EM_ANALISE` → senão `422` (`regra_negocio`).

### Efeito

`status` → `RESOLVIDO`, grava `descricaoSolucao` e `dataAtualizacao`.

> 🔑 **Consequência direta para o front:** um `<select>` livre de atendentes aqui produz `403`
> em quase toda escolha. O único `idUsuario` válido é o `atendenteId` do próprio ticket — que já
> vem na listagem. O campo deve ser fixo/pré-selecionado com o atendente associado, ou nem existir.

---

## Cancelar

### Requisição

```
POST /tickets/{id}/cancelar
```

```json
{
  "idUsuario": 1,
  "motivo": "Equipamento foi trocado pelo fornecedor."
}
```

| Campo | Tipo | Obrigatório | Validação |
|---|---|---|---|
| `idUsuario` | `number` | sim | precisa existir e estar ativo |
| `motivo` | `string` | sim | **mínimo 10** e **máximo 1000** caracteres |

### Regras do back-end (`cancelar`)

1. O ticket precisa existir → senão `404`.
2. O usuário precisa existir e estar ativo → senão `404`.
3. Se o status for `RESOLVIDO` → `422` ("Tickets resolvidos não podem ser cancelados").
4. Se o status for `CANCELADO` → `422` ("Ticket já está cancelado").

### Efeito

`status` → `CANCELADO`, grava `motivoCancelamento` e `dataAtualizacao`.

> 🔎 **Cancelar não valida papel.** Qualquer usuário existente e ativo (`ATENDENTE` **ou**
> `SOLICITANTE`) pode cancelar. Também aceita ticket `ABERTO` (sem atendente). Portanto o
> `<select>` de usuário desta ação **não deve** ser filtrado por `papel` como o de associar.

---

## Resposta de sucesso (`TicketResposta`)

As três ações devolvem o mesmo objeto (`200 OK`), em camelCase:

```json
{
  "id": 7,
  "numeroProtocolo": "20260928-00007",
  "titulo": "PC com problema",
  "descricao": "Placa de vídeo não tem internet",
  "status": "RESOLVIDO",
  "prioridade": "ALTA",
  "setor": "TI",
  "descricaoSolucao": "Placa de vídeo substituída e testada.",
  "motivoCancelamento": null,
  "dataCriacao": "2026-09-28T13:45:10",
  "dataAtualizacao": "2026-09-28T14:02:33",
  "solicitanteId": 1,
  "atendenteId": 2
}
```

Observações:

- `prioridade`, `descricaoSolucao`, `motivoCancelamento`, `dataAtualizacao` e `atendenteId`
  podem vir `null`.
- As datas são **ISO 8601 sem timezone e em UTC** (`api/app/core/tempo.py` grava
  `datetime.now(timezone.utc)` sem `tzinfo`). Ao exibir com `| date` o Angular vai
  interpretar como hora **local** — a diferença de fuso aparece na tela.
- O `interface TicketResposta` do front tem o campo escrito **`dataAtualizaco`**
  (falta o `a`), então esse valor chega como `undefined` hoje.

---

## Respostas de erro

Existem **dois formatos diferentes**, e ambos podem chegar com status `422`:

### 1. Erro de domínio (`api/app/core/exceptions.py`)

```json
{
  "codigo": "regra_negocio",
  "mensagem": "Somente tickets em análise podem ser resolvidos",
  "detalhes": []
}
```

| Status | `codigo` | Quando acontece nas três ações |
|---|---|---|
| `404` | `nao_encontrado` | ticket inexistente; usuário inexistente ou inativo |
| `403` | `permissao_negada` | papel errado (prioridade/resolver); atendente não associado (resolver) |
| `422` | `regra_negocio` | status inválido (resolver, cancelar) |

A mensagem em `mensagem` é escrita em português e pode ser exibida direto ao usuário.

### 2. Erro de validação do FastAPI/Pydantic

Quando o corpo não bate com o schema (`descricao` com menos de 10 caracteres, `prioridade`
fora do enum, campo ausente):

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "descricao"],
      "msg": "String should have at least 10 characters",
      "input": "ok"
    }
  ]
}
```

Também `422`, mas com a chave `detail` (um array) e mensagens em inglês.

> 🔧 Implicação: o tratamento de erro do front precisa olhar o corpo, não só o status.
> Algo como “se existir `error.mensagem`, mostre; senão, mensagem genérica” cobre os dois casos.
> Validar os tamanhos mínimos no próprio formulário evita o formato 2 quase sempre.

---

## Matriz status × ação

O que a API de fato permite (linha = status atual do ticket):

| Status | Associar | Definir Prioridade | Resolver | Cancelar |
|---|---|---|---|---|
| `ABERTO` | ✅ | ✅ (não bloqueado) | ❌ `422` | ✅ |
| `EM_ANALISE` | ❌ `422` | ✅ | ✅ (só o atendente associado) | ✅ |
| `RESOLVIDO` | ❌ `422` | ✅ (não bloqueado) | ❌ `422` | ❌ `422` |
| `CANCELADO` | ❌ `422` | ✅ (não bloqueado) | ❌ `422` | ❌ `422` |

O `listar.html` atual é **mais restritivo** que a API: mostra `Definir Prioridade`, `Resolver`
e `Cancelar` somente em `EM_ANALISE`. Isso é seguro (nunca gera erro), mas esconde dois casos
que a API aceitaria: definir prioridade em ticket `ABERTO` e cancelar ticket `ABERTO`.
**É uma decisão de produto** — vale confirmar antes de implementar a UI.

---

## O que já existe no front

| Peça | Arquivo | Situação |
|---|---|---|
| `TicketResposta` | `models/tickets.model.ts` | existe (com o typo `dataAtualizaco`) |
| `TicketAssociar` | `models/tickets.model.ts` | existe — serve de molde para as novas |
| `listar()` / `cadastrar()` / `associar()` | `services/ticket.service.ts` | existem |
| `UsuarioService.listar()` | `services/usuario.service.ts` | existe (devolve `id`, `nome`, `papel`) |
| Componente `app-modal` | `shared/modal/modal.ts` | pronto (ver `docs/componente-modal.md`) |
| Botões das 3 ações | `pages/tickets/listar/listar.html` | existem, **sem `(click)`** |
| Fluxo completo de referência | `pages/tickets/listar/listar.ts` → `associar()` | pronto — mesmo padrão a seguir |

---

## O que falta implementar

### 1. Models (`models/tickets.model.ts`)

```ts
export interface TicketDefinirPrioridade {
  idUsuario: number | null;
  prioridade: string | null;
}

export interface TicketResolver {
  idUsuario: number | null;
  descricao: string;
}

export interface TicketCancelar {
  idUsuario: number | null;
  motivo: string;
}
```

E corrigir `dataAtualizaco` → `dataAtualizacao`.

### 2. Métodos no `TicketService`

```ts
definirPrioridade(id: number, dado: TicketDefinirPrioridade): Observable<TicketResposta> {
  return this.http.post<TicketResposta>(`${this.baseUrl}/${id}/definir-prioridade`, dado);
}

resolver(id: number, dado: TicketResolver): Observable<TicketResposta> {
  return this.http.post<TicketResposta>(`${this.baseUrl}/${id}/resolver`, dado);
}

cancelar(id: number, dado: TicketCancelar): Observable<TicketResposta> {
  return this.http.post<TicketResposta>(`${this.baseUrl}/${id}/cancelar`, dado);
}
```

### 3. Tela de listagem

- Três modais (uma por ação) com seus sinais de abertura.
- Guardar o **ticket inteiro** no `ticketSelecionado`, não só o `id` — `resolver` precisa do
  `atendenteId` e as mensagens de confirmação ficam melhores com `numeroProtocolo`.
- Ligar os `(click)` dos botões já existentes.
- Reset dos campos ao fechar/concluir (o `associar()` já faz isso).

### 4. Campos por modal

| Ação | Campos | Observação |
|---|---|---|
| Definir Prioridade | usuário (atendentes) + prioridade | radio ou select com `BAIXA`/`MEDIA`/`ALTA` |
| Resolver | usuário (**o atendente associado**) + descrição | textarea; mínimo 10, máximo 1000 |
| Cancelar | usuário (**todos**, sem filtro de papel) + motivo | textarea; mínimo 10, máximo 1000 |

---

## Pontos de atenção e divergências

1. **`resolver` exige o atendente associado.** É a regra mais fácil de esbarrar. Tratar o
   campo de usuário como fixo (derivado de `ticket.atendenteId`) evita um `403` garantido.
2. **`cancelar` não filtra papel**, ao contrário de `associar` e `definir-prioridade`.
   Copiar o `@if(usuario.papel == "ATENDENTE")` do `listar.html` para a modal de cancelar
   restringiria sem necessidade.
3. **`definir-prioridade` não valida status** — a API é mais permissiva que a tela.
4. **Dois formatos de erro no mesmo status `422`** (`mensagem` vs `detail`). Ver
   [Respostas de erro](#respostas-de-erro).
5. **`[value]` em `<select>` devolve `string`.** No `associar` funciona porque o Pydantic
   converte `"2"` → `2`. Ainda assim, `[ngValue]` mantém o tipo `number` e é mais seguro
   (com `[value]`, `idUsuario` chega como texto ao back).
6. **Mínimo de 10 caracteres** em `descricao` e `motivo`: sem validação no formulário, o
   usuário recebe uma mensagem em inglês vinda do Pydantic.
7. **Nomes dos campos de texto diferem entre as ações:** `resolver` usa `descricao`,
   `cancelar` usa `motivo`. Não são intercambiáveis.
8. **Tickets só aparecem via `GET /tickets`** (sem filtro/paginação na API). Após a ação,
   ou se usa o ticket devolvido para atualizar o sinal, ou se chama `carregarTickets()`
   de novo — como o `associar()` faz hoje.
9. **Não existe endpoint para desfazer** nenhuma dessas ações. `RESOLVIDO` e `CANCELADO` são
   estados finais — a confirmação na UI importa.
10. **`GET /usuarios` não tem filtro por papel**; a separação entre atendentes e solicitantes
    é feita no front, sobre a lista completa já carregada em `usuarios()`.
