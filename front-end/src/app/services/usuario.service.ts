import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { UsuarioResposta } from '../models/usuarios.model';

@Injectable({
  providedIn: 'root',
})
export class UsuarioService {
  private httpClient = inject(HttpClient)

  private baseUrl = `http://localhost:8000/usuarios`;

  listar(): Observable<UsuarioResposta[]> {
    return this.httpClient.get<UsuarioResposta[]>(this.baseUrl)
  }
}
