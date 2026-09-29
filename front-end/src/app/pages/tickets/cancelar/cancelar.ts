import { Component, inject, input, output, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TicketCancelar, TicketResposta } from '../../../models/tickets.model';
import { UsuarioResposta } from '../../../models/usuarios.model';
import { TicketService } from '../../../services/ticket.service';
import { Modal } from '../../../shared/modal/modal';

const MOTIVO_MINIMO = 10;
const MOTIVO_MAXIMO = 1000;

@Component({
  selector: 'app-cancelar',
  imports: [Modal, FormsModule],
  templateUrl: './cancelar.html',
  styleUrl: './cancelar.scss',
})
export class Cancelar {
  private ticketService = inject(TicketService);

  /** Controla a exibição da modal. */
  aberto = input<boolean>(false);

  /** Ticket que será cancelado. */
  ticket = input<TicketResposta | null>(null);

  /** Lista completa de usuários. Cancelar não exige papel nenhum,
      então aqui não há filtro por ATENDENTE. */
  usuarios = input<UsuarioResposta[]>([]);

  /** Emitido quando o usuário pede para fechar a modal. */
  fechar = output<void>();

  /** Emitido no sucesso, com o ticket já atualizado pela API. */
  cancelado = output<TicketResposta>();

  motivoMinimo = MOTIVO_MINIMO;
  motivoMaximo = MOTIVO_MAXIMO;

  dado: TicketCancelar = {
    idUsuario: null,
    motivo: ""
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
      motivo: ""
    };
    this.erro.set(null);
    this.salvando.set(false);
  }

  salvar() {
    const ticket = this.ticket();
    if (ticket === null) return;

    if (this.dado.idUsuario === null) {
      this.erro.set("Selecione o usuário que está cancelando o ticket");
      return;
    }

    if (this.dado.motivo.trim().length < MOTIVO_MINIMO) {
      this.erro.set(`Descreva o motivo com no mínimo ${MOTIVO_MINIMO} caracteres`);
      return;
    }

    this.salvando.set(true);
    this.erro.set(null);

    this.ticketService.cancelar(ticket.id, this.dado).subscribe({
      next: atualizado => {
        // reset dos campos da modal; quem fecha a modal é a tela
        this.reiniciar();
        this.cancelado.emit(atualizado);
      },
      error: erro => {
        console.error(erro);
        this.salvando.set(false);
        // Erro de domínio traz { codigo, mensagem, detalhes }; validação do
        // Pydantic traz { detail: [...] } — ver docs/api-acoes-ticket.md
        this.erro.set(erro.error?.mensagem ?? "Não foi possível cancelar o ticket");
      }
    })
  }
}
