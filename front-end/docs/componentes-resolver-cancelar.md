# Componentes `app-resolver` e `app-cancelar`

> Modais das ações **Resolver** e **Cancelar**: formulário, chamada da API e tratamento de erro.
> Arquivos: `src/app/pages/tickets/resolver/` e `src/app/pages/tickets/cancelar/`.
> Seguem o mesmo molde de `app-definir-prioridade` (`componente-definir-prioridade.md`) e usam o
> `app-modal` internamente. Contrato da API em `api-acoes-ticket.md`.

---

## Sumário

1. [O que os dois têm em comum](#o-que-os-dois-têm-em-comum)
2. [Diferenças](#diferenças)
3. [`app-resolver`](#app-resolver)
4. [`app-cancelar`](#app-cancelar)
5. [Pontos de atenção](#pontos-de-atenção)

---

## O que os dois têm em comum

- **Autônomos**: injetam o `TicketService`, chamam a API, tratam o erro e emitem o ticket
  atualizado. A tela só informa `[aberto]`, `[ticket]` e `[usuarios]`.
- **Não se fecham sozinhos** — emitem e a tela decide, o que mantém a modal aberta no erro.
- **Validam localmente antes da request**: o texto tem mínimo de 10 caracteres (`trim()`), e o
  `maxlength` de 1000 no `textarea` espelha o limite da API. Assim o usuário nunca recebe a
  mensagem em inglês do Pydantic.
- **Contador de caracteres** abaixo do campo (`{{ ... .length }}/1000`).
- **Erro dentro da modal**, de `erro.error?.mensagem`, com fallback genérico.
- **Botão de confirmar desabilitado** enquanto a request está no ar (sinal `salvando`).
- **Reset** ao fechar e ao concluir (`reiniciar()`).
- Formulário com a classe global `.form-modal` (`src/styles.scss`).

---

## Diferenças

| | `app-resolver` | `app-cancelar` |
|---|---|---|
| Endpoint | `POST /tickets/{id}/resolver` | `POST /tickets/{id}/cancelar` |
| Campo de texto | `descricao` (solução) | `motivo` (cancelamento) |
| Campo de usuário | **não é escolha** — exibição do atendente associado | `<select>` com **todos** os usuários |
| `idUsuario` enviado | `ticket.atendenteId` | o escolhido no select |
| Saída de sucesso | `(resolvido)` | `(cancelado)` |
| Botão de confirmar | `class="sucesso"` — *Resolver* | `class="perigo"` — *Cancelar Ticket* |
| Botão de fechar | `class="perigo-contorno"` — *Cancelar* | `class="secundario"` — *Voltar* |

O motivo da diferença no campo de usuário está no back-end: `resolver` exige que `idUsuario` seja
**exatamente** o `atendenteId` do ticket (um select livre daria `403` em qualquer outra escolha),
enquanto `cancelar` **não valida papel nenhum** — qualquer usuário ativo pode cancelar.

---

## `app-resolver`

### Entradas e saídas

| Entrada | Tipo | Descrição |
|---|---|---|
| `aberto` | `boolean` | Controla a exibição. |
| `ticket` | `TicketResposta \| null` | De onde saem o `id` e o `atendenteId` enviados à API. |
| `usuarios` | `UsuarioResposta[]` | Usada **só para exibir o nome** do atendente associado. |

| Saída | Tipo | Quando dispara |
|---|---|---|
| `fechar` | `void` | *Cancelar*, `×` ou `ESC`. |
| `resolvido` | `TicketResposta` | Sucesso, com o ticket já em `RESOLVIDO`. |

### Uso

```html
<app-resolver
    [aberto]="modalResolverAberta()"
    [ticket]="ticketSelecionado()"
    [usuarios]="usuarios()"
    (fechar)="modalResolverAberta.set(false)"
    (resolvido)="aoResolver($event)" />
```

O atendente sai de um `computed()` que cruza `ticket().atendenteId` com `usuarios()`:

```ts
atendente = computed(() =>
  this.usuarios().find(usuario => usuario.id === this.ticket()?.atendenteId) ?? null
);
```

Se o ticket não tiver atendente (`atendenteId === null`), `salvar()` recusa antes de chamar a API
com "Este ticket não tem atendente associado" — situação que não acontece pela listagem, onde o
botão só aparece em `EM_ANALISE`.

---

## `app-cancelar`

### Entradas e saídas

| Entrada | Tipo | Descrição |
|---|---|---|
| `aberto` | `boolean` | Controla a exibição. |
| `ticket` | `TicketResposta \| null` | De onde sai o `id` enviado à API. |
| `usuarios` | `UsuarioResposta[]` | Vai inteira para o `<select>`, **sem filtro de papel**. |

| Saída | Tipo | Quando dispara |
|---|---|---|
| `fechar` | `void` | *Voltar*, `×` ou `ESC`. |
| `cancelado` | `TicketResposta` | Sucesso, com o ticket já em `CANCELADO`. |

### Uso

```html
<app-cancelar
    [aberto]="modalCancelarAberta()"
    [ticket]="ticketSelecionado()"
    [usuarios]="usuarios()"
    (fechar)="modalCancelarAberta.set(false)"
    (cancelado)="aoCancelar($event)" />
```

---

## Pontos de atenção

1. **Não filtre `papel` no select de cancelar.** É a única ação de ticket que não exige
   `ATENDENTE`; copiar o `@if(usuario.papel == "ATENDENTE")` das outras modais restringiria
   sem necessidade.
2. **Não transforme o campo de atendente do resolver em `<select>`.** O único `idUsuario` aceito
   é o `atendenteId` do ticket; qualquer outro atendente recebe
   `403 "Somente o atendente associado pode resolver este ticket"`.
3. **`RESOLVIDO` e `CANCELADO` são estados finais** — não existe endpoint para desfazer. Por isso
   `[fecharAoClicarFora]="false"` e o botão de cancelar usa a variação `perigo`.
4. **Os nomes dos campos não são intercambiáveis**: `resolver` usa `descricao`, `cancelar` usa
   `motivo`.
5. **`[ngValue]` no `<option>`** do select de cancelar, para `idUsuario` viajar como `number`.
