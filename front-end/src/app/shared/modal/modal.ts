import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.html',
  styleUrl: './modal.scss',
  host: {
    '(document:keydown.escape)': 'aoPressionarEsc()',
  },
})
export class Modal {
  /** Texto exibido no cabeçalho da modal. */
  titulo = input<string>('');

  /** Controla a exibição da modal. */
  aberto = input<boolean>(false);

  /** Permite fechar clicando no fundo escuro. */
  fecharAoClicarFora = input<boolean>(true);

  /** Permite fechar pressionando ESC. */
  fecharComEsc = input<boolean>(true);

  /** Exibe o "x" no canto superior direito. */
  mostrarBotaoFechar = input<boolean>(true);

  /** Emitido sempre que o usuário pede para fechar a modal. */
  fechar = output<void>();

  aoClicarNoFundo(evento: MouseEvent) {
    const clicouNoFundo = evento.target === evento.currentTarget;

    if (clicouNoFundo && this.fecharAoClicarFora()) {
      this.fechar.emit();
    }
  }

  aoPressionarEsc() {
    if (this.aberto() && this.fecharComEsc()) {
      this.fechar.emit();
    }
  }
}
