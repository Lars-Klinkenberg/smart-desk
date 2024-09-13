import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { AsyncPipe, CommonModule } from '@angular/common';
import { Entry } from '../../models/Entry';
import { HeightService } from '../../services/height.service';

@Component({
  selector: 'app-pie-chart',
  standalone: true,
  imports: [CommonModule, AsyncPipe],
  templateUrl: './pie-chart.component.html',
  styleUrl: './pie-chart.component.scss',
})
export class PieChartComponent implements OnInit {
  allEntrys!: Observable<Entry[]>;

  constructor(private heigtService: HeightService) {}

  ngOnInit(): void {
    this.allEntrysCall();
  }

  allEntrysCall() {
    this.allEntrys = this.heigtService.getAllHeights();
  }
}
