import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PreviousDayStatsComponent } from './previous-day-stats.component';

describe('PreviousDayStatsComponent', () => {
  let component: PreviousDayStatsComponent;
  let fixture: ComponentFixture<PreviousDayStatsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PreviousDayStatsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PreviousDayStatsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
