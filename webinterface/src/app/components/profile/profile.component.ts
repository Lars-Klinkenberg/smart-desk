import { Component, Input } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { Setting } from '../../models/Setting';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [MatInputModule, MatSelectModule, MatFormFieldModule],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss',
})
export class ProfileComponent {
  @Input() set profiles(value: Setting[]) {
    this.availableProfiles = value;

    if (this.availableProfiles.length === 0) {
      this.selectedProfile = undefined;
      return;
    }

    this.selectedProfile = this.availableProfiles[0].presetName;
  }

  availableProfiles: Setting[] = [];
  selectedProfile: string | undefined;
}
