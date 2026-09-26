import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { TicketAssociar, TicketCadastro, TicketResposta } from '../models/tickets.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TicketService {
  private http = inject(HttpClient);

  private baseUrl = `http://localhost:8000/tickets`

  listar(): Observable<TicketResposta[]>{
    return this.http.get<TicketResposta[]>(this.baseUrl);
  }

  cadastrar(ticket: TicketCadastro): Observable<TicketResposta> {
    return this.http.post<TicketResposta>(this.baseUrl, ticket);
  }

  associar(id: number, ticket: TicketAssociar): Observable<TicketResposta> {
    return this.http.post<TicketResposta>(`${this.baseUrl}/${id}/associar`, ticket)
  }
}
