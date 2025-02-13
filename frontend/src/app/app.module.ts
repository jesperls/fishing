import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http'; // For API calls
import { FormsModule } from '@angular/forms'; // For ngModel

import { AppComponent } from './app.component';
import { FishingComponent } from './fishing/fishing.component';

@NgModule({
  declarations: [AppComponent, FishingComponent],
  imports: [BrowserModule, HttpClientModule, FormsModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
