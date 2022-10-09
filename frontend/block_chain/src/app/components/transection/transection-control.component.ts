import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'transection-control',
  templateUrl: './transection-control.component.html',
  styleUrls: ['./transection-control.component.css']
})

export class TransectionControlComponent implements OnInit{

  // should use services
  private postTransection(data:string){
    const headers = { 'content-type': 'application/json'}
    let body = {"content": data}
    JSON.stringify(body);
    this.http.post("http://localhost:8000/api/add-transection", body,{'headers':headers}).subscribe(res => {
      console.log(res)
    });
  }

  @ViewChild('trandata', { static: true }) transectionElement: ElementRef;
  tdata:string = "";
  
  constructor(transectionElement: ElementRef, private http:HttpClient) {
    this.transectionElement = transectionElement;
  }

  addTransection(){
    this.tdata = this.transectionElement.nativeElement.value;
    this.postTransection(this.tdata)
    location.reload();
  }

  ngOnInit(): void {
  }
}
