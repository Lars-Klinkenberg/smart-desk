import { AfterViewInit, Component } from '@angular/core';
import { TimeService } from '../../services/time.service';

@Component({
    selector: 'app-previous-day-stats',
    imports: [],
    templateUrl: './previous-day-stats.component.html',
    styleUrl: './previous-day-stats.component.scss'
})
export class PreviousDayStatsComponent implements AfterViewInit {
  standingTime = '--:--:--';

  constructor(private readonly timeService: TimeService) {}

  ngAfterViewInit(): void {
    this.timeService.getYesterdaysStandingTime().subscribe((data) => {
      data.forEach((activity) => {
        if (!activity.height) return;

        if (activity.height == 115) {
          this.standingTime = activity.total_time;
        }
      });
    });
  }
}
