import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'transection-pool',
  templateUrl: './transection-pool.component.html',
  styleUrls: ['./transection-pool.component.css']
})
export class TransectionPoolComponent implements OnInit {
  transections:any;

  constructor(private http:HttpClient){

  }
  private getTransections(){
    this.http.get("http://localhost:8000/api/transections").subscribe(res => {
      let result:any = res;
      this.transections = result["message"]
    });
  }

  ngOnInit(): void {
      this.getTransections()
  }
}
