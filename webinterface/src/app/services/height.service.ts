import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Entry } from '../models/Entry';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class HeightService {
  constructor(private http: HttpClient) {}

  getAllHeights(): Observable<Entry[]> {
    return this.http.get<Entry[]>(environment.BASE_URL + '/height/entrys/all', {
      responseType: 'json',
    });
  }
}

