# Componente `app-modal`

> Modal reutilizável com **título**, **conteúdo livre** e **botões no rodapé**.
> Arquivos: `src/app/shared/modal/modal.ts`, `modal.html`, `modal.scss`.
> Segue a paleta das telas de tickets (fundo `#181126`, cabeçalho `#25163d`, roxo `#6d28d9`).

---

## Sumário

1. [Como importar](#como-importar)
2. [Uso básico](#uso-básico)
3. [API](#api)
4. [Botões do rodapé](#botões-do-rodapé)
5. [Exemplos](#exemplos)
6. [Comportamento](#comportamento)
7. [Pontos de atenção](#pontos-de-atenção)

---

## Como importar

O componente é standalone — basta adicioná-lo ao `imports` do componente que vai usá-lo.

```ts
import { Component, signal } from '@angular/core';
import { Modal } from '../../../shared/modal/modal';

@Component({
  selector: 'app-listar',
  imports: [Modal],
  templateUrl: './listar.html',
  styleUrl: './listar.scss',
})
export class Listar {
  modalAberta = signal(false);
}
```

> Ajuste o caminho do `import` conforme a profundidade da sua pasta. De `src/app/pages/tickets/listar/` o caminho é `../../../shared/modal/modal`.

---

## Uso básico

```html
<button (click)="modalAberta.set(true)">Abrir</button>

<app-modal
  titulo="Definir Prioridade"
  [aberto]="modalAberta()"
  (fechar)="modalAberta.set(false)">

  <!-- conteúdo (corpo da modal) -->
  <p>Escolha a prioridade do ticket.</p>

  <!-- botões (rodapé da modal) -->
  <button modal-acoes class="secundario" (click)="modalAberta.set(false)">Cancelar</button>
  <button modal-acoes (click)="confirmar()">Confirmar</button>
</app-modal>
```

São três coisas para lembrar:

| O quê | Como |
|---|---|
| Título | atributo `titulo` |
| Corpo | qualquer conteúdo **sem** atributo especial |
| Rodapé | elementos com o atributo `modal-acoes` |

---

## API

### Entradas

| Entrada | Tipo | Padrão | Descrição |
|---|---|---|---|
| `titulo` | `string` | `''` | Texto do cabeçalho. |
| `aberto` | `boolean` | `false` | Controla a exibição. Quando `false`, a modal **não existe no DOM**. |
| `fecharAoClicarFora` | `boolean` | `true` | Clique no fundo escuro emite `fechar`. |
| `fecharComEsc` | `boolean` | `true` | Tecla `ESC` emite `fechar`. |
| `mostrarBotaoFechar` | `boolean` | `true` | Exibe o `×` no canto superior direito. |

### Saída

| Saída | Tipo | Quando dispara |
|---|---|---|
| `fechar` | `void` | Clique no `×`, clique no fundo ou `ESC`. |

---

## Botões do rodapé

Qualquer elemento com o atributo `modal-acoes` vai para o rodapé, alinhado à direita. Os `<button>` já recebem o estilo roxo padrão; as classes abaixo são opcionais:

| Classe | Aparência | Uso típico |
|---|---|---|
| *(nenhuma)* | roxo `#6d28d9` | ação principal (Confirmar, Salvar) |
| `secundario` | contorno, fundo transparente | Cancelar, Voltar |
| `sucesso` | verde `#15803d` | Resolver, Aprovar |
| `perigo` | vermelho `#991b1b` | Cancelar ticket, Excluir |

```html
<button modal-acoes class="secundario" (click)="fecharModal()">Voltar</button>
<button modal-acoes class="perigo" (click)="cancelarTicket()">Cancelar Ticket</button>
```

Sem nenhum elemento `modal-acoes`, o rodapé simplesmente não aparece.

---

## Exemplos

### 1. Confirmação

```ts
confirmacaoAberta = signal(false);
ticketSelecionado = signal<TicketResposta | null>(null);

abrirConfirmacao(ticket: TicketResposta) {
  this.ticketSelecionado.set(ticket);
  this.confirmacaoAberta.set(true);
}

confirmarCancelamento() {
  const ticket = this.ticketSelecionado();
  if (!ticket) return;

  this.ticketService.cancelar(ticket.id).subscribe({
    next: () => {
      this.confirmacaoAberta.set(false);
      this.carregarTickets();
    },
    error: erro => console.error(erro),
  });
}
```

```html
<app-modal
  titulo="Cancelar Ticket"
  [aberto]="confirmacaoAberta()"
  (fechar)="confirmacaoAberta.set(false)">

  <p>Deseja cancelar o ticket {{ ticketSelecionado()?.numeroProtocolo }}?</p>

  <button modal-acoes class="secundario" (click)="confirmacaoAberta.set(false)">Não</button>
  <button modal-acoes class="perigo" (click)="confirmarCancelamento()">Sim, cancelar</button>
</app-modal>
```

### 2. Formulário dentro da modal

Os campos ficam no corpo; o estilo dos inputs é responsabilidade da tela que usa a modal (o corpo aceita qualquer HTML).

```html
<app-modal
  titulo="Definir Prioridade"
  [aberto]="modalPrioridade()"
  [fecharAoClicarFora]="false"
  (fechar)="modalPrioridade.set(false)">

  <label for="campo-prioridade">Prioridade</label>
  <select id="campo-prioridade" [(ngModel)]="prioridade">
    <option value="BAIXA">Baixa</option>
    <option value="MEDIA">Média</option>
    <option value="ALTA">Alta</option>
  </select>

  <button modal-acoes class="secundario" (click)="modalPrioridade.set(false)">Cancelar</button>
  <button modal-acoes (click)="salvarPrioridade()">Salvar</button>
</app-modal>
```

> `[fecharAoClicarFora]="false"` evita que um clique acidental descarte o que foi digitado.

### 3. Mais de uma modal na mesma tela

Cada modal tem seu próprio sinal — não há limite de instâncias.

```ts
modalAssociar = signal(false);
modalResolver = signal(false);
```

```html
<app-modal titulo="Associar Atendente" [aberto]="modalAssociar()" (fechar)="modalAssociar.set(false)">
  ...
</app-modal>

<app-modal titulo="Resolver Ticket" [aberto]="modalResolver()" (fechar)="modalResolver.set(false)">
  ...
</app-modal>
```

---

## Comportamento

- **Componente controlado**: a modal **não se fecha sozinha**. Ela apenas emite `fechar`; quem decide é a tela — o que permite validar o formulário antes de fechar, ou manter aberta em caso de erro da API.
- **Fora do DOM quando fechada**: o `@if (aberto())` remove o conteúdo, então o estado dos campos internos é perdido ao fechar (comportamento desejado para formulários).
- **Corpo com rolagem**: a caixa tem `max-height: calc(100vh - 48px)` e o corpo rola sozinho quando o conteúdo é grande.
- **Responsivo**: abaixo de 700px o padding diminui e os botões do rodapé se dividem em largura igual.
- **Acessibilidade**: `role="dialog"`, `aria-modal="true"` e `aria-label="Fechar"` no `×`.

---

## Pontos de atenção

1. **Não esqueça o `Modal` no `imports`** do componente. Sem isso o Angular trata `<app-modal>` como elemento desconhecido e o conteúdo simplesmente não renderiza.
2. **O atributo é `modal-acoes`, sem colchetes** no uso (`<button modal-acoes>`). Os colchetes aparecem apenas no seletor interno (`select="[modal-acoes]"`).
3. **Estilo dos botões do rodapé usa `::ng-deep`**, porque conteúdo projetado mantém a encapsulação do componente pai e não seria alcançado pelos seletores da modal. A API é deprecada, mas continua sendo a saída prática; a alternativa seria mover essas regras para `styles.scss` como classes globais.
4. **Rolagem do fundo não é bloqueada.** Com a modal aberta, a página atrás ainda rola. Se isso incomodar, é preciso adicionar o bloqueio de `overflow` no `body`.
5. **Sem foco automático nem foco preso (focus trap).** A tecla `ESC` funciona porque o listener está em `document`, mas o `Tab` ainda alcança elementos atrás da modal.
