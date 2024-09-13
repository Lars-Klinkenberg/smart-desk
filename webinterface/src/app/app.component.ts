import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { TimeHeatmapComponent } from "./components/time-heatmap/time-heatmap.component";
import { PieChartComponent } from "./components/pie-chart/pie-chart.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, TimeHeatmapComponent, PieChartComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'webinterface';
  pieChartData =  [30,50]
}