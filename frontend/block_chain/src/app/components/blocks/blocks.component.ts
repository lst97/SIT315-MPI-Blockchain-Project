import { Component } from '@angular/core';
import { BlocksService } from './blocks.service';

@Component({
  selector: 'blocks',
  templateUrl: './blocks.component.html',
  styleUrls: ['./blocks.component.css']
})
export class BlocksComponent {
  blocks:any;
  constructor(private service:BlocksService) { }

  ngOnInit(): void {
    // {"message":[[1,"INITIAL_BLOCK","00000c197a21d1ea83a17c1e8cf5f366cccfa882","",42054]]}
    this.service.getBlocks().subscribe(res => {
      this.blocks = res;
      this.blocks = this.blocks["message"]
    });
  }
}