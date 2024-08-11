import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { MatTooltipModule } from '@angular/material/tooltip';

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
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
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
  heightData = new Map<string, number>();

  ngOnInit(): void {
    let currentYear = new Date().getFullYear();
    this.year = [];
    this.year.push(...this.getAllDaysOfYear(currentYear));
    this.loadHeightData(currentYear);
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

  getTooltip(day: Date): string {
    return day.getDate() + '.' + (day.getMonth() + 1);
  }

  getDayLevel(day: Date): string {
    return this.heightData.get(day.toLocaleDateString())?.toString() ?? '0';
  }

  loadHeightData(year: number) {
    this.heightData.clear();

    this.getAllDaysOfYear(year).forEach((day) => {
      this.heightData.set(
        day.toLocaleDateString(),
        Math.floor(Math.random() * 4) + 1
      );
    });
  }

  getClassname(day: Date): string {
    return day.getMonth() % 2 == 0 ? 'month-even' : 'month-odd';
  }

  getMonthColWidth(month: string): string {
    let firstRow = this.getAllDaysByDayOfWeek(1, this.year);
    let daysOfMonth = firstRow.filter((day) => {
      return day.getMonth() == this.MONTHS.indexOf(month);
    });

    return daysOfMonth.length.toString();
  }
}
