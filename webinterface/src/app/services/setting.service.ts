import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { Setting } from '../models/Setting';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SettingService {
  private readonly selectedProfileStorageSelector = 'selected_profile';
  constructor(private readonly http: HttpClient) {}

  public loadProfileList(): Observable<Setting[]> {
    return this.http.get<Setting[]>(
      environment.BASE_URL + '/setting/profile_list'
    );
  }

  public saveSelectedProfileToStorage(profile: Setting) {
    sessionStorage.setItem(
      this.selectedProfileStorageSelector,
      profile.presetName
    );
  }

  public getSelectedProfileFromStorage(): string | null {
    return sessionStorage.getItem(this.selectedProfileStorageSelector);
  }
}
