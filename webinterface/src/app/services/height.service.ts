import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Height } from '../models/Height';

@Injectable({
  providedIn: 'root',
})
export class HeightService {
  constructor(private readonly http: HttpClient) {}

  getAllHeights(): Observable<Height[]> {
    let headers = new HttpHeaders();
    headers = headers.set('day', 'all');

    return this.http.get<Height[]>(environment.BASE_URL + '/height/entries', {
      responseType: 'json',
      headers: headers,
    });
  }
}
