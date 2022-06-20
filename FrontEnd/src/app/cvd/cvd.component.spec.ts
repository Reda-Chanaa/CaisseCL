import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CVDComponent } from './cvd.component';

describe('CVDComponent', () => {
  let component: CVDComponent;
  let fixture: ComponentFixture<CVDComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CVDComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CVDComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
