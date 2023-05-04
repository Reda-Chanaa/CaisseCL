import { Component, OnInit } from '@angular/core';

declare interface RouteInfo {
  path: string;
  title: string;
  icon: string;
  class: string;
}
export const ROUTES: RouteInfo[] = [
  
  { path: '/internet', title: 'Internet', icon: 'design_bullet-list-67', class: '' },
  { path: '/sav', title: 'SAV', icon: 'design_bullet-list-67', class: '' },
  { path: '/adv', title: 'ADV', icon: 'design_bullet-list-67', class: '' },
  { path: '/cvd', title: 'CVD', icon: 'design_bullet-list-67', class: '' },
  { path: '/journal', title: 'Journal', icon: 'design_bullet-list-67', class: '' },
  { path: '/prepaye', title: 'Prépayés', icon: 'design_bullet-list-67', class: '' },

];

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  menuItems: any[];

  constructor() { }

  ngOnInit() {
    this.menuItems = ROUTES.filter(menuItem => menuItem);
  }
  isMobileMenu() {
    if (window.innerWidth > 991) {
      return false;
    }
    return true;
  };
}
