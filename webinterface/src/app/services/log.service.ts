import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Log, LogLevel, LogSource } from '../models/Log';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class LogService {
  constructor(private readonly http: HttpClient) {}

  getGenericLog(source: LogSource, levels: LogLevel[]): Observable<Log[]> {
    return this.http.get<Log[]>(environment.BASE_URL + '/monitoring/logs');
  }
}
