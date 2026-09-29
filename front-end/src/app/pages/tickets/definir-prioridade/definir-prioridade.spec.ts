import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DefinirPrioridade } from './definir-prioridade';

describe('DefinirPrioridade', () => {
  let component: DefinirPrioridade;
  let fixture: ComponentFixture<DefinirPrioridade>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DefinirPrioridade],
    }).compileComponents();

    fixture = TestBed.createComponent(DefinirPrioridade);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
