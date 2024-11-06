import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatSelectChange, MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { Setting } from '../../models/Setting';
import { SettingService } from '../../services/setting.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [MatInputModule, MatSelectModule, MatFormFieldModule],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss',
})
export class ProfileComponent {
  @Output() selectionChange = new EventEmitter<Setting>();
  availableProfiles: Setting[] = [];
  selectedProfile: string | undefined;

  constructor(private readonly settingService: SettingService) {
    this.settingService.loadProfileList().subscribe({
      next: (settings) => {
        this.availableProfiles = settings;

        this.setSelectedProfile();
        if (this.selectedProfile) {
          this.sendSelectedChanges(this.selectedProfile);
        }
      },
    });
  }

  detectSelectChanges(e: MatSelectChange) {
    let selectedValue = e.value;
    let selectedSetting = this.availableProfiles.find((value) => {
      return value.presetName == selectedValue;
    });

    if (!selectedSetting) return;

    this.settingService.saveSelectedProfileToStorage(selectedSetting);
    this.sendSelectedChanges(selectedValue)
  }

  /**
   * loads selected setting from storage if exists if not sets default to available[0]
   * @returns
   */
  setSelectedProfile() {
    let storageSetting = this.settingService.getSelectedProfileFromStorage();

    if (this.availableProfiles.length === 0) {
      this.selectedProfile = undefined;
      return;
    }

    if (!storageSetting) {
      this.selectedProfile = this.availableProfiles[0].presetName;
      return;
    }

    if (
      this.availableProfiles.find((value) => {
        return value.presetName === storageSetting;
      })
    ) {
      this.selectedProfile = storageSetting;
      return;
    }

    this.selectedProfile = this.availableProfiles[0].presetName;
  }

  sendSelectedChanges(presetName: string) {
    this.selectionChange.emit(
      this.availableProfiles.find((value) => {
        return value.presetName === presetName;
      })
    );
  }
}
