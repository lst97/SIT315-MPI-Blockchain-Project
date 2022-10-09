import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ServerStatusService {
  private url = 'http://127.0.0.1:8000/api/server_status';
  constructor(private http:HttpClient) {
  }

  getServerStatus(){
    return this.http.get(this.url);
  }
}
