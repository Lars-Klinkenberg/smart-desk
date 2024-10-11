import { Component, OnInit } from '@angular/core';
import { HeightService } from '../../services/height.service';
import { Observable } from 'rxjs';
import { AsyncPipe, CommonModule } from '@angular/common';
import { Height } from '../../models/Height';

@Component({
  selector: 'history',
  standalone: true,
  imports: [CommonModule, AsyncPipe],
  templateUrl: './history.component.html',
  styleUrl: './history.component.scss',
})
export class HistoryComponent implements OnInit {
  MAX_LOG_COUNT = 20;
  completeHistory!: Observable<Height[]>;

  constructor(private readonly heigtService: HeightService) {}

  ngOnInit(): void {
    this.completeHistory = this.heigtService.getAllHeights();
  }
}
