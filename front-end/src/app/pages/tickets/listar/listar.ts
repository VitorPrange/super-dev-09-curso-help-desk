import { Component, inject, signal } from '@angular/core';
import { TicketService } from '../../../services/ticket.service';
import { TicketAssociar, TicketResposta } from '../../../models/tickets.model';
import { RouterLink } from '@angular/router';
import { Modal } from '../../../shared/modal/modal';
import { UsuarioResposta } from '../../../models/usuarios.model';
import { FormsModule } from '@angular/forms';
import { UsuarioService } from '../../../services/usuario.service';
import { DefinirPrioridade } from '../definir-prioridade/definir-prioridade';
import { Resolver } from '../resolver/resolver';
import { Cancelar } from '../cancelar/cancelar';

@Component({
  selector: 'app-listar',
  imports: [RouterLink, Modal, FormsModule, DefinirPrioridade, Resolver, Cancelar],
  templateUrl: './listar.html',
  styleUrl: './listar.scss',
})
export class Listar {
  ticketService = inject(TicketService);
  usuarioService = inject(UsuarioService);

  tickets = signal<TicketResposta[]>([]);
  modalAssociarAberta = signal<boolean>(false);
  modalPrioridadeAberta = signal<boolean>(false);
  modalResolverAberta = signal<boolean>(false);
  modalCancelarAberta = signal<boolean>(false);
  ticketAssociar: TicketAssociar = {
    idUsuario: null
  }
  usuarios = signal<UsuarioResposta[]>([]);
  ticketSelecionado = signal<TicketResposta | null>(null);

  ngOnInit() {
    this.carregarTickets();
    this.carregarUsuarios();
  }

  carregarUsuarios() {
    this.usuarioService.listar().subscribe({
      next: usuarios => this.usuarios.set(usuarios),
      error: erro => {
        console.error(erro);
        alert("Não foi possível listar os usuários");
      }
    })
  }

  carregarTickets() {
    this.ticketService.listar().subscribe({
      next: (tickets) => this.tickets.set(tickets),
      error: (erro) => {
        console.error(erro);
        alert("Não foi possível carregar os tickets");
      }
    })
  }

  // as ações devolvem o ticket completo, então atualizamos apenas a
  // linha alterada em vez de recarregar a lista inteira
  atualizarLista(ticket: TicketResposta) {
    this.tickets.update(tickets =>
      tickets.map(item => item.id === ticket.id ? ticket : item)
    );
  }

  abrirModalAssociar(ticket: TicketResposta){
    this.ticketSelecionado.set(ticket);
    this.modalAssociarAberta.set(true);
  }

  associar(){
    this.ticketService.associar(this.ticketSelecionado()!.id, this.ticketAssociar).subscribe({
      next: () => {
        // fechar modal
        this.modalAssociarAberta.set(false);
        // reset dos campos da modal
        this.ticketAssociar = {
          idUsuario: null
        };
        
        alert("Ticket associado com sucesso");
        this.carregarTickets();
      },
      error: erro => {
        console.error(erro);
        alert("Não foi possível associar o ticket");
      }
    })
  }

  abrirModalPrioridade(ticket: TicketResposta){
    this.ticketSelecionado.set(ticket);
    this.modalPrioridadeAberta.set(true);
  }

  aoDefinirPrioridade(ticket: TicketResposta){
    this.modalPrioridadeAberta.set(false);
    this.atualizarLista(ticket);

    alert("Prioridade definida com sucesso");
  }

  abrirModalResolver(ticket: TicketResposta){
    this.ticketSelecionado.set(ticket);
    this.modalResolverAberta.set(true);
  }

  aoResolver(ticket: TicketResposta){
    this.modalResolverAberta.set(false);
    this.atualizarLista(ticket);

    alert("Ticket resolvido com sucesso");
  }

  abrirModalCancelar(ticket: TicketResposta){
    this.ticketSelecionado.set(ticket);
    this.modalCancelarAberta.set(true);
  }

  aoCancelar(ticket: TicketResposta){
    this.modalCancelarAberta.set(false);
    this.atualizarLista(ticket);

    alert("Ticket cancelado com sucesso");
  }
}
