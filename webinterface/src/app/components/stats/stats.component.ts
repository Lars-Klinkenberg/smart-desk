import { AfterViewInit, Component } from '@angular/core';
import { TimeService } from '../../services/time.service';

@Component({
  selector: 'app-stats',
  standalone: true,
  imports: [],
  templateUrl: './stats.component.html',
  styleUrl: './stats.component.scss',
})
export class StatsComponent implements AfterViewInit {
  todaysStandingTime = '--:--:--';
  dailyGoal = '--:--:--';
  weeklyAvg = '--:--:--';

  constructor(private timeService: TimeService) {}

  ngAfterViewInit(): void {
    this.timeService.getTodaysStandingTime().subscribe((data) => {
      data.forEach((activity) => {
        if (!activity.height) return;

        if (activity.height == 115) {
          this.todaysStandingTime = this.timeService.formatMinutesToTimeString(
            Number(activity.total_time)
          );
        }
      });
    });
  }
}
