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

  constructor(private timeService: TimeService) {}

  ngAfterViewInit(): void {
    this.timeService.getTodaysStandingTime().subscribe((data) => {
      data.forEach((activity) => {
        if (!activity.height) return;

        if (activity.height == 115) {
          this.todaysStandingTime = this.formatMinutesToTimeString(
            Number(activity.total_time)
          );
        }
      });
    });
  }

  formatMinutesToTimeString(minutes: number): string {
    const hrs = Math.floor(minutes / 60); // Get the whole hours
    const mins = Math.floor(minutes % 60); // Get the remaining minutes
    const secs = Math.floor((minutes % 1) * 60); // Get the remaining seconds if there are fractions

    // Pad the hours, minutes, and seconds to always show two digits
    const hoursStr = String(hrs).padStart(2, '0');
    const minutesStr = String(mins).padStart(2, '0');
    const secondsStr = String(secs).padStart(2, '0');

    return `${hoursStr}:${minutesStr}:${secondsStr}`;
  }
}
