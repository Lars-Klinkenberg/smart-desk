import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Log, LogLevel, LogSource } from '../models/Log';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class LogService {
  constructor(private readonly http: HttpClient) {}

  getGenericLog(
    source?: LogSource,
    levels?: LogLevel[],
    offset?: number,
    limit?: number
  ): Observable<Log[]> {
    let headers = new HttpHeaders();
    if (levels) {
      console.log('levels', levels);
      // headers = headers.append('level', levels[0].toString());
    }

    if (source) {
      headers = headers.append('service_name', source);
    }

    if (offset) {
      headers = headers.append('offset', offset.toString());
    }

    if (limit) {
      headers = headers.append('limit', limit.toString());
    }

    return this.http.get<Log[]>(environment.BASE_URL + '/monitoring/logs', {
      headers: headers,
    });
  }
}
