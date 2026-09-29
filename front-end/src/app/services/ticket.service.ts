import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { TicketAssociar, TicketCadastro, TicketCancelar, TicketDefinirPrioridade, TicketResolver, TicketResposta } from '../models/tickets.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TicketService {
  // HttpClient é o cliente que utilizamos no angular para fazer requests
  private http = inject(HttpClient);

  // URL do back-end por enquanto está fixo, depois 
  // utilizaremos environment para ser dinâmico
  private baseUrl = `http://localhost:8000/tickets`

  // função que será responsável por comunicar com o back 
  // para obter a lista de tickets
  listar(): Observable<TicketResposta[]> {
    // faz a requisição para /tickets no back-end
    return this.http.get<TicketResposta[]>(this.baseUrl);
  }

  cadastrar(ticket: TicketCadastro): Observable<TicketResposta> {
    return this.http.post<TicketResposta>(this.baseUrl, ticket);
  }

  associar(id: number, ticket: TicketAssociar): Observable<TicketResposta> {
    return this.http.post<TicketResposta>(`${this.baseUrl}/${id}/associar`, ticket);
  }

  definirPrioridade(id: number, dado: TicketDefinirPrioridade): Observable<TicketResposta> {
    return this.http.post<TicketResposta>(`${this.baseUrl}/${id}/definir-prioridade`, dado);
  }

  resolver(id: number, dado: TicketResolver): Observable<TicketResposta> {
    return this.http.post<TicketResposta>(`${this.baseUrl}/${id}/resolver`, dado);
  }

  cancelar(id: number, dado: TicketCancelar): Observable<TicketResposta> {
    return this.http.post<TicketResposta>(`${this.baseUrl}/${id}/cancelar`, dado);
  }
}
