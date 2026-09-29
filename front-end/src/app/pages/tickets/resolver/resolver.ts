import { Component, computed, inject, input, output, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TicketResolver, TicketResposta } from '../../../models/tickets.model';
import { UsuarioResposta } from '../../../models/usuarios.model';
import { TicketService } from '../../../services/ticket.service';
import { Modal } from '../../../shared/modal/modal';

const DESCRICAO_MINIMA = 10;
const DESCRICAO_MAXIMA = 1000;

@Component({
  selector: 'app-resolver',
  imports: [Modal, FormsModule],
  templateUrl: './resolver.html',
  styleUrl: './resolver.scss',
})
export class Resolver {
  private ticketService = inject(TicketService);

  /** Controla a exibição da modal. */
  aberto = input<boolean>(false);

  /** Ticket que será resolvido. */
  ticket = input<TicketResposta | null>(null);

  /** Lista completa de usuários, usada apenas para exibir o nome do atendente. */
  usuarios = input<UsuarioResposta[]>([]);

  /** Emitido quando o usuário pede para fechar a modal. */
  fechar = output<void>();

  /** Emitido no sucesso, com o ticket já atualizado pela API. */
  resolvido = output<TicketResposta>();

  descricaoMinima = DESCRICAO_MINIMA;
  descricaoMaxima = DESCRICAO_MAXIMA;

  // A API aceita resolver somente pelo atendente associado ao ticket,
  // então o campo de usuário não é escolha: é o próprio ticket que define
  atendente = computed(() =>
    this.usuarios().find(usuario => usuario.id === this.ticket()?.atendenteId) ?? null
  );

  dado: TicketResolver = {
    idUsuario: null,
    descricao: ""
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
      descricao: ""
    };
    this.erro.set(null);
    this.salvando.set(false);
  }

  salvar() {
    const ticket = this.ticket();
    if (ticket === null) return;

    if (ticket.atendenteId === null) {
      this.erro.set("Este ticket não tem atendente associado");
      return;
    }

    if (this.dado.descricao.trim().length < DESCRICAO_MINIMA) {
      this.erro.set(`Descreva a solução com no mínimo ${DESCRICAO_MINIMA} caracteres`);
      return;
    }

    // quem resolve é sempre o atendente associado ao ticket
    this.dado.idUsuario = ticket.atendenteId;

    this.salvando.set(true);
    this.erro.set(null);

    this.ticketService.resolver(ticket.id, this.dado).subscribe({
      next: atualizado => {
        // reset dos campos da modal; quem fecha a modal é a tela
        this.reiniciar();
        this.resolvido.emit(atualizado);
      },
      error: erro => {
        console.error(erro);
        this.salvando.set(false);
        // Erro de domínio traz { codigo, mensagem, detalhes }; validação do
        // Pydantic traz { detail: [...] } — ver docs/api-acoes-ticket.md
        this.erro.set(erro.error?.mensagem ?? "Não foi possível resolver o ticket");
      }
    })
  }
}
