import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { PlayerFishData } from './fishing';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class FishingService {
  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getPlayerFishData(username: string): Observable<PlayerFishData> {
    return this.http.get<PlayerFishData>(`${this.baseUrl}/${username}`);
  }
}
