import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TimeHeatmapComponent } from './time-heatmap.component';

describe('TimeHeatmapComponent', () => {
  let component: TimeHeatmapComponent;
  let fixture: ComponentFixture<TimeHeatmapComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TimeHeatmapComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TimeHeatmapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
