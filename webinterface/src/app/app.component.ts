import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'webinterface';

  // Constructor with HttpClient injection
  constructor(private http: HttpClient) {}

  // Updated API method to call an example API and log the response
  public changeDeskHeight(status: "UP" | "DOWN") {
    const apiUrl = 'http://192.168.178.122:5000/move/' + status; // Placeholder URL
    this.http.get(apiUrl).subscribe({
      next: (response) => console.log(response),
      error: (error) => console.error('There was an error!', error)
    });
  }
}
