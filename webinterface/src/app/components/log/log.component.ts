import { AfterViewInit, Component, inject, ViewChild } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { Log, LogLevel, LogSource } from '../../models/Log';
import { LogService } from '../../services/log.service';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-log',
  standalone: true,
  imports: [
    CommonModule,
    MatInputModule,
    MatSelectModule,
    MatFormFieldModule,
    MatTableModule,
    MatSortModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './log.component.html',
  styleUrl: './log.component.scss',
})
export class LogComponent {
  @ViewChild(MatSort) sort!: MatSort;

  availableSources: string[] = Object.keys(LogSource);
  selectedSource: string;

  displayedColumns = ['time', 'level', 'message'];
  dataSource: MatTableDataSource<Log> = new MatTableDataSource();
  isLoadingResults = true;

  constructor(private readonly logService: LogService) {
    this.selectedSource = this.availableSources[0];
    this.loadLogData(LogSource.DESK_CONTROLLER);
  }

  detectSelectChanges(e: any) {
    let source = this.getLogSourceFromString(e.value);
    if (!source) return;

    console.log('CHANGED ', source);
    this.loadLogData(source);
  }

  loadLogData(source: LogSource) {
    this.isLoadingResults = true;
    this.logService
      .getGenericLog(source, [LogLevel.CRITICAL])
      .subscribe((data: Log[]) => {
        console.log('DATA ', data);
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.sort = this.sort;
        this.isLoadingResults = false;
      });
  }

  getLogSourceFromString(source: string): LogSource | undefined {
    return LogSource[source as keyof typeof LogSource];
  }
}
