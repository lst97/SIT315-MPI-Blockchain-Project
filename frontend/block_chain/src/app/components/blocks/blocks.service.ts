import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class BlocksService {
  private url = 'http://127.0.0.1:8000/api/blocks';
  constructor(private http:HttpClient) {
  }

  getBlocks(){
    return this.http.get(this.url);
  }
}