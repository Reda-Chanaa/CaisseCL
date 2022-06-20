import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SAVComponent } from './sav.component';

describe('SAVComponent', () => {
  let component: SAVComponent;
  let fixture: ComponentFixture<SAVComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SAVComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SAVComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
