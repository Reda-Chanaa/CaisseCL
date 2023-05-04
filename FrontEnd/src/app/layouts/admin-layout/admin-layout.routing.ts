import { Routes } from '@angular/router';
import { JournalComponent } from '../../journal/journal.component';
import { ADVComponent } from '../../adv/adv.component';
import { CVDComponent } from '../../cvd/cvd.component';
import { InternetComponent } from '../../internet/internet.component';
import { SAVComponent } from '../../sav/sav.component';
import { PrepComponent } from '../../prep/prep.component';



export const AdminLayoutRoutes: Routes = [
    { path: 'journal',     component: JournalComponent },
    { path: 'internet',     component: InternetComponent },
    { path: 'sav',     component: SAVComponent },
    { path: 'adv',     component: ADVComponent },
    { path: 'cvd',     component: CVDComponent },
    { path: 'prepaye',     component: PrepComponent }

];
