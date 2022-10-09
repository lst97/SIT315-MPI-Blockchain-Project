import { ServerStatusService } from './components/header/server-status.service';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { BlocksComponent } from './components/blocks/blocks.component';
import { TransectionPoolComponent } from './components//transection/transection-pool.component';
import { TransectionControlComponent } from './components/transection/transection-control.component';
import { HomeComponent } from './home/home.component';
import { HeaderComponent } from './components/header/header.component';
@NgModule({
  declarations: [
    AppComponent,
    BlocksComponent,
    TransectionPoolComponent,
    TransectionControlComponent,
    HomeComponent,
    HeaderComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [ServerStatusService],
  bootstrap: [AppComponent]
})
export class AppModule { }
