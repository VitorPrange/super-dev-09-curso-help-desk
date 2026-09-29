import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: "tickets",
        loadComponent: () => import("./pages/tickets/listar/listar").then(m => m.Listar)
    },
    {
        path: "tickets/cadastro",
        loadComponent: () => import("./pages/tickets/cadastro/cadastro").then(m => m.Cadastro)
    },
];
