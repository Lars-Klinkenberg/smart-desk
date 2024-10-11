import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { DailyActivity } from '../models/DailyActivity';

@Injectable({
  providedIn: 'root',
})
export class TimeService {
  constructor(private http: HttpClient) {}

  getDailyActivity(): Observable<DailyActivity[]> {
    const baseHeaders = new HttpHeaders().set('year', '2024');
    return this.http.get<DailyActivity[]>(environment.BASE_URL + '/height/total/year', {
      headers: baseHeaders.set('year', '2024'),
    });
  }

  getTodaysStandingTime(): Observable<DailyActivity[]> {
    return this.http.get<DailyActivity[]>(environment.BASE_URL + '/height/total/today');
  }

  getYesterdaysStandingTime(): Observable<DailyActivity[]> {
    return this.http.get<DailyActivity[]>(
      environment.BASE_URL + '/height/total/yesterday'
    );
  }
  /**
   * turns an activity time like "0:34:25" to an hour as number like 0,56
   * @param activity
   * @returns
   */
  getHoursOfActivity(activity: DailyActivity): number {
    let splitted = activity.total_time.split(':');
    let hoursAsMinutes = Number(splitted[0]) * 60;
    let totalMinutes = hoursAsMinutes + Number(splitted[1]);
    return totalMinutes / 60;
  }

  formatMinutesToTimeString(minutes: number, showSeconds = true): string {
    const hrs = Math.floor(minutes / 60); // Get the whole hours
    const mins = Math.floor(minutes % 60); // Get the remaining minutes
    const secs = Math.floor((minutes % 1) * 60); // Get the remaining seconds if there are fractions

    // Pad the hours, minutes, and seconds to always show two digits
    const hoursStr = String(hrs).padStart(2, '0');
    const minutesStr = String(mins).padStart(2, '0');
    const secondsStr = String(secs).padStart(2, '0');

    if (!showSeconds) {
      return `${hoursStr}:${minutesStr}`;
    }

    return `${hoursStr}:${minutesStr}:${secondsStr}`;
  }
}
