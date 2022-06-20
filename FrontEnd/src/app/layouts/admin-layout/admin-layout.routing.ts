import { Routes } from '@angular/router';
import { ADVComponent } from '../../adv/adv.component';
import { CVDComponent } from '../../cvd/cvd.component';
import { InternetComponent } from '../../internet/internet.component';
import { SAVComponent } from '../../sav/sav.component';


export const AdminLayoutRoutes: Routes = [
    { path: 'internet',     component: InternetComponent },
    { path: 'sav',     component: SAVComponent },
    { path: 'adv',     component: ADVComponent },
    { path: 'cvd',     component: CVDComponent }

];
