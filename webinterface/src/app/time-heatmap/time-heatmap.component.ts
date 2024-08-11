import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import {MatTooltipModule} from '@angular/material/tooltip';

export const Months = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
];

export const Weekdays = [
  'Sonntag',
  'Montag',
  'Dienstag',
  'Mittwoch',
  'Donnerstag',
  'Freitag',
  'Samstag',
];

@Component({
  selector: 'time-heatmap',
  standalone: true,
  imports: [CommonModule, MatTooltipModule],
  templateUrl: './time-heatmap.component.html',
  styleUrl: './time-heatmap.component.scss',
})
export class TimeHeatmapComponent implements OnInit {
  MONTHS = Months;
  WEEKDAYS = Weekdays;

  year: Date[] = [];

  ngOnInit(): void {
    this.year = [];
    this.year.push(...this.getAllDaysOfYear(new Date().getFullYear()));
  }

  /**
   * returns a list of all days within the current year
   * @returns
   */
  getAllDaysOfYear(year: number): Date[] {
    let allDays: Date[] = [];
    for (let i = 1; i < 13; i++) {
      let month = this.getAllDaysInMonth(i, year);

      allDays.push(...month);
    }

    console.log(allDays);

    return allDays;
  }

  /**
   * returns a list of all days in the month
   * @param month index of the month - starting with 1
   * @param year year as number
   * @returns
   */
  getAllDaysInMonth(month: number, year: number): Date[] {
    return Array.from(
      { length: new Date(year, month, 0).getDate() },
      (_, i) => new Date(year, month - 1, i + 1)
    );
  }

  /**
   * returns all days of the allDays array with the given weekday
   * @param weekday weekday (0-6) - monday => 1
   * @param allDays array of allDays that should be filtered
   * @returns
   */
  getAllDaysByDayOfWeek(weekday: number, allDays: Date[]): Date[] {
    let allWeekdays = allDays.filter((date) => {
      return date.getDay() == weekday;
    });

    if (weekday == 0) {
      if (allWeekdays[0].getDate() - 7 > 0) {
        allWeekdays.unshift(new Date(1970, 0, 1));
      }
    } else if (allWeekdays[0].getDate() - weekday > 0) {
      allWeekdays.unshift(new Date(1970, 0, 1));
    }

    return allWeekdays || [];
  }
}
