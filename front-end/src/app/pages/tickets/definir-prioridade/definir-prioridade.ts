import { Component, computed, inject, input, output, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TicketDefinirPrioridade, TicketResposta } from '../../../models/tickets.model';
import { UsuarioResposta } from '../../../models/usuarios.model';
import { TicketService } from '../../../services/ticket.service';
import { Modal } from '../../../shared/modal/modal';

@Component({
  selector: 'app-definir-prioridade',
  imports: [Modal, FormsModule],
  templateUrl: './definir-prioridade.html',
  styleUrl: './definir-prioridade.scss',
})
export class DefinirPrioridade {
  private ticketService = inject(TicketService);

  /** Controla a exibição da modal. */
  aberto = input<boolean>(false);

  /** Ticket que terá a prioridade definida. */
  ticket = input<TicketResposta | null>(null);

  /** Lista completa de usuários; o filtro por papel é feito aqui. */
  usuarios = input<UsuarioResposta[]>([]);

  /** Emitido quando o usuário pede para fechar a modal. */
  fechar = output<void>();

  /** Emitido no sucesso, com o ticket já atualizado pela API. */
  definido = output<TicketResposta>();

  // A API aceita definir prioridade somente por usuário com papel ATENDENTE
  atendentes = computed(() =>
    this.usuarios().filter(usuario => usuario.papel === 'ATENDENTE')
  );

  prioridades = [
    {
      "valor": "BAIXA",
      "descricao": "Baixa"
    },
    {
      "valor": "MEDIA",
      "descricao": "Média"
    },
    {
      "valor": "ALTA",
      "descricao": "Alta"
    }
  ]

  dado: TicketDefinirPrioridade = {
    idUsuario: null,
    prioridade: null
  }

  salvando = signal<boolean>(false);
  erro = signal<string | null>(null);

  aoFechar() {
    this.reiniciar();
    this.fechar.emit();
  }

  reiniciar() {
    this.dado = {
      idUsuario: null,
      prioridade: null
    };
    this.erro.set(null);
    this.salvando.set(false);
  }

  salvar() {
    const ticket = this.ticket();
    if (ticket === null) return;

    if (this.dado.idUsuario === null || this.dado.prioridade === null) {
      this.erro.set("Selecione o atendente e a prioridade");
      return;
    }

    this.salvando.set(true);
    this.erro.set(null);

    this.ticketService.definirPrioridade(ticket.id, this.dado).subscribe({
      next: atualizado => {
        // reset dos campos da modal; quem fecha a modal é a tela
        this.reiniciar();
        this.definido.emit(atualizado);
      },
      error: erro => {
        console.error(erro);
        this.salvando.set(false);
        // Erro de domínio traz { codigo, mensagem, detalhes }; validação do
        // Pydantic traz { detail: [...] } — ver docs/api-acoes-ticket.md
        this.erro.set(erro.error?.mensagem ?? "Não foi possível definir a prioridade");
      }
    })
  }
}
