import { ServerStatusService } from './server-status.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  server_status:string[] = [];
  api_status = "offline";
  pool_status = "offline";
  result:any;
  constructor(private service:ServerStatusService) { 
  }
  
  ngOnInit(): void {
    this.service.getServerStatus().subscribe(res => {
      this.result = res;
      // [0]: number of record
      // [0][0...4]: ID, NAME, IP, PORT, STATUS
      // {"message":[[1,"API","127.0.0.1","8000","online"]]}
      for(let i =0; i < 2; i++){
        if (this.result["message"][i] != undefined){
          this.server_status.push(this.result["message"][i][4])
        }
        else 
          this.server_status.push("offline")
      }
      this.api_status = this.server_status[0];
      this.pool_status = this.server_status[1];
    });
  }
}
