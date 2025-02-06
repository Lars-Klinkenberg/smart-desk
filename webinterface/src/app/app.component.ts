import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TimeHeatmapComponent } from './components/time-heatmap/time-heatmap.component';
import { StatsComponent } from './components/stats/stats.component';
import { ProfileComponent } from './components/profile/profile.component';
import { Setting } from './models/Setting';
import { LogComponent } from './components/log/log.component';

@Component({
  selector: 'app-root',
  imports: [
    CommonModule,
    TimeHeatmapComponent,
    StatsComponent,
    ProfileComponent,
    LogComponent,
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'webinterface';
  pieChartData = [30, 50];
  currentProfile: Setting | undefined;

  settingChangeSelectionChange(e: Setting) {
    this.currentProfile = e;
  }
}
