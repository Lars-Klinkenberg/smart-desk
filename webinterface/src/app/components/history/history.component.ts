import { Component, OnInit } from '@angular/core';
import { HeightService } from '../../services/height.service';
import { Observable } from 'rxjs';
import { Entry } from '../../models/Entry';
import { AsyncPipe, CommonModule } from '@angular/common';

@Component({
  selector: 'history',
  standalone: true,
  imports: [CommonModule, AsyncPipe],
  templateUrl: './history.component.html',
  styleUrl: './history.component.scss',
})
export class HistoryComponent implements OnInit {
  MAX_LOG_COUNT = 20;
  completeHistory!: Observable<Entry[]>;

  constructor(private heigtService: HeightService) {}

  ngOnInit(): void {
    this.completeHistory = this.heigtService.getAllHeights();
  }
}
