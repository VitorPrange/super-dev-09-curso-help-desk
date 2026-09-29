# Componente `app-definir-prioridade`

> Modal completa da ação **Definir Prioridade**: formulário, chamada da API e tratamento de erro.
> Arquivos: `src/app/pages/tickets/definir-prioridade/definir-prioridade.ts`, `.html`, `.scss`.
> Usa o `app-modal` internamente (ver `docs/componente-modal.md`) e o endpoint descrito em
> `docs/api-acoes-ticket.md`.

---

## Sumário

1. [Ideia geral](#ideia-geral)
2. [Como usar](#como-usar)
3. [API](#api)
4. [Comportamento](#comportamento)
5. [Pontos de atenção](#pontos-de-atenção)

---

## Ideia geral

O componente é **autônomo**: ele é o único lugar do front que conhece
`POST /tickets/{id}/definir-prioridade`. Quem o utiliza só precisa dizer **qual ticket** e
**se a modal está aberta** — e recebe de volta, em `(definido)`, o ticket já atualizado pela API.

Isso mantém a tela de listagem enxuta: nenhum formulário, nenhuma chamada de serviço e nenhum
tratamento de erro desta ação vivem no `listar.ts`.

---

## Como usar

```ts
import { DefinirPrioridade } from '../definir-prioridade/definir-prioridade';

@Component({
  selector: 'app-listar',
  imports: [DefinirPrioridade],
  ...
})
export class Listar {
  modalPrioridadeAberta = signal<boolean>(false);
  ticketSelecionado = signal<TicketResposta | null>(null);

  abrirModalPrioridade(ticket: TicketResposta) {
    this.ticketSelecionado.set(ticket);
    this.modalPrioridadeAberta.set(true);
  }

  aoDefinirPrioridade(ticket: TicketResposta) {
    this.modalPrioridadeAberta.set(false);
    // a api devolve o ticket completo: atualiza só a linha alterada
    this.tickets.update(tickets =>
      tickets.map(item => item.id === ticket.id ? ticket : item)
    );
    alert("Prioridade definida com sucesso");
  }
}
```

```html
<button (click)="abrirModalPrioridade(ticket)">Definir Prioridade</button>

<app-definir-prioridade
    [aberto]="modalPrioridadeAberta()"
    [ticket]="ticketSelecionado()"
    [usuarios]="usuarios()"
    (fechar)="modalPrioridadeAberta.set(false)"
    (definido)="aoDefinirPrioridade($event)" />
```

---

## API

### Entradas

| Entrada | Tipo | Padrão | Descrição |
|---|---|---|---|
| `aberto` | `boolean` | `false` | Controla a exibição da modal. |
| `ticket` | `TicketResposta \| null` | `null` | Ticket que terá a prioridade definida. É daqui que sai o `id` enviado à API. |
| `usuarios` | `UsuarioResposta[]` | `[]` | Lista **completa** de usuários. O componente filtra `papel === 'ATENDENTE'` internamente, porque a API só aceita atendentes nesta ação. |

### Saídas

| Saída | Tipo | Quando dispara |
|---|---|---|
| `fechar` | `void` | Clique em *Cancelar*, no `×`, ou `ESC`. |
| `definido` | `TicketResposta` | Sucesso da API, com o ticket já atualizado (status, prioridade e `dataAtualizacao`). |

---

## Comportamento

- **Não se fecha sozinho.** Como o `app-modal`, ele só emite — inclusive no sucesso (`definido`).
  Quem fecha é a tela. Isso é o que mantém a modal aberta quando a API devolve erro.
- **Validação local antes da request**: sem atendente ou sem prioridade selecionada, exibe
  "Selecione o atendente e a prioridade" e **não** chama a API.
- **Erro aparece dentro da modal**, não em `alert()`, para não descartar o que foi preenchido.
  A mensagem vem de `erro.error?.mensagem` (formato dos erros de domínio da API) e cai numa
  mensagem genérica quando o corpo tem outro formato — por exemplo a validação do Pydantic,
  que usa `detail`. Os dois formatos estão descritos em `docs/api-acoes-ticket.md`.
- **Botão *Salvar* desabilitado durante a request** (sinal `salvando`), evitando duplo envio.
- **Reset dos campos** ao fechar e ao concluir com sucesso (`reiniciar()`).
- **`:host { display: contents; }`** — o componente não cria caixa no layout de quem o usa.

---

## Pontos de atenção

1. **`[ngValue]` no `<option>`, não `[value]`.** Assim `idUsuario` chega à API como `number`.
   Com `[value]`, o valor viaja como string (a modal de associar ainda faz isso e só funciona
   porque o Pydantic converte `"2"` → `2`).
2. **Os radios precisam do `name="prioridade"`** — é por ele que o Angular agrupa os `input`s.
3. **Valores da prioridade são `BAIXA`, `MEDIA`, `ALTA`** (o `TODO.md` cita `BAIXO`, que a API
   rejeita com `422`).
4. **Definir prioridade não muda o status** do ticket e a API **não** valida o status atual —
   quem restringe a ação a `EM_ANALISE` é o `listar.html`.
5. **O estilo do `select` está duplicado** entre `listar.scss` (`.form-associar`) e este
   componente. Quando as modais de resolver e cancelar existirem, vale extrair para uma classe
   global `.form-modal` em `styles.scss`.
