import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ADVComponent } from './adv.component';

describe('ADVComponent', () => {
  let component: ADVComponent;
  let fixture: ComponentFixture<ADVComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ADVComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ADVComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
