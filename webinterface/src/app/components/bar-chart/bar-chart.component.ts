import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { TimeService } from '../../services/time.service';

@Component({
  selector: 'app-bar-chart',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './bar-chart.component.html',
  styleUrl: './bar-chart.component.scss',
})
export class BarChartComponent {
  data = [333, 32, 105, 405, 163, 444, 192];
  GOAL = 100;

  constructor(private readonly timeService: TimeService) {}

  getBarHeight(data: number) {
    return ((data / this.GOAL) * 80).toString() + '%';
  }

  getGoalHeight() {
    console.log((this.GOAL / 100) * 20);

    return ((this.GOAL / 100) * 20).toString() + '%';
  }

  getBarLabel(data: number) {
    return this.timeService.formatMinutesToTimeString(data, false) + " h";
  }
}
