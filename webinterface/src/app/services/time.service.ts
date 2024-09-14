import { HttpClient } from '@angular/common/http';
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
    return this.http.get<DailyActivity[]>(
      environment.BASE_URL + '/time/activity/115',
      {
        responseType: 'json',
      }
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
}
