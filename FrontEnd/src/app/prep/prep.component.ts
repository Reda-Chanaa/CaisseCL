import { Component, ElementRef, ViewChild } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { merge, Observable } from 'rxjs';
import { FormControl, FormGroup } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
// class pour les requettes GET et POST.
export class ApiStat {

  baseurl = environment.BASE_URL;

  constructor(private http: HttpClient) {

  }
  sendFile(File1: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/prepaye/', formData, { headers: header })
  }

}

// interface StatData qui précise les données affichées dans le tableau ainsi que leur type.
export interface StatData {
  date_depart: string;
  armateur: string;
  reseau: string;
  code_navire: string;
  port_depart: string;
  port_arrivee: string;
  res_type: string;
  code_addon: string;
  nb_pax_addon: string;
  total_pax_traversee: string;
  SEUIL:string

}
@Component({
  selector: 'app-prep',
  templateUrl: './prep.component.html',
  styleUrls: ['./prep.component.scss'],
  providers: [ApiStat]
})
export class PrepComponent {



  @ViewChild('TABLE') table: ElementRef;

  @ViewChild('MatPaginator') paginator: MatPaginator;

  day = new Date().getDate()
  moiss = new Date().getMonth() + 1
  annees = new Date().getFullYear()
  date: any

  selection: string;
  selections: string;
  selectionss: string;

  dataFrame: any;
  dataFrameFilter: any;
  dataFrameFilter2: any;

  displayedColumns: string[] = ['date_depart', 'armateur', 'reseau', 'code_navire', 'port_depart', 'port_arrivee', 'res_type', 'code_addon', 'nb_pax_addon', 'total_pax_traversee','SEUIL'];

  dataSource: MatTableDataSource<StatData>;

  element: any;
  df1: any;

  annee: string;

  value: number = 10;

  constructor(private DATACLEANING: ApiStat) {
    // Assign the data to the data source for the table to render
    this.dataSource = new MatTableDataSource([]);
  }

  // function executed when file is changed
  fileChangeListener1($event: any): void {
    this.df1 = $event.target.files[0]
  }
  getNbColor(ar: string, nb: number): string {
    if ((ar === 'GOTA' && nb < 100 && nb >= 50)
      || (ar === 'BABU' && nb < 80 && nb >= 40)
      || (ar === 'MORO' && nb < 80 && nb >= 40)
      || (ar === 'ORBA' && nb < 80 && nb >= 40)
      || (ar === 'NEPI' && nb < 70 && nb >= 35)
      || (ar === 'VONA' && nb < 40 && nb >= 20)) {
      return 'orange';
    }
    else if ((ar === 'GOTA' && nb < 50)
      || (ar === 'BABU' && nb < 40)
      || (ar === 'MORO' && nb < 40)
      || (ar === 'ORBA' && nb < 40)
      || (ar === 'NEPI' && nb < 35)
      || (ar === 'VONA' && nb < 20)) {
      return 'green';
    }
    else {
      return 'red';
    }
  }

  deleteData() {
    this.dataSource = new MatTableDataSource([]);
  }
  // function executed when user click on Reporting button
  createFile = () => {

    if (this.df1 != null) {
      this.value = 0
      this.DATACLEANING.sendFile(this.df1).subscribe(
        data => {
          this.value = 10
          this.dataFrame = data;
          console.log(this.dataFrame)
          // to choose witch data gonna be showing in the table
          this.InitializeVisualization();
          // puts data into the datasource table
          this.dataSource = new MatTableDataSource(data);
          // execute the visualisation function
          this.executeVisualisation();
          // add paginator to the data
          this.dataSource.paginator = this.paginator;
        },
        error => {
          console.log("error ", error);
        }
      );
    }
  }

  filterTable = () => {
    if (this.dataFrame != null) {
      this.dataFrameFilter = this.dataFrame.filter(item => item.code_navire === this.selections);
      //console.log(this.selections)
      // to choose witch data gonna be showing in the table
      if (this.selections == "TOUS") {
        this.dataFrameFilter = this.dataFrame
      }
      this.InitializeVisualization();
      this.dataSource = new MatTableDataSource(this.dataFrameFilter);
      this.executeVisualisation();
      // add paginator to the data
      this.dataSource.paginator = this.paginator;

    }
  }

  filterTables = () => {
    if (this.dataFrameFilter != null && this.dataFrame==null ) {
      this.dataFrameFilter2 = this.dataFrameFilter.filter(item => this.getNbColor(item.code_navire, item.nb_pax_addon) === this.selectionss);
      //console.log(this.selectionss)
      // to choose witch data gonna be showing in the table
      if (this.selectionss == "TOUS") {
        this.dataFrameFilter2 = this.dataFrameFilter
      }
      this.InitializeVisualization();
      this.dataSource = new MatTableDataSource(this.dataFrameFilter2);
      this.executeVisualisation();
      // add paginator to the data
      this.dataSource.paginator = this.paginator;
    }
    else if (this.dataFrame != null  && this.dataFrameFilter==null) {
      this.dataFrameFilter2 = this.dataFrame.filter(item => this.getNbColor(item.code_navire, item.nb_pax_addon) === this.selectionss);
      //console.log(this.selectionss)
      // to choose witch data gonna be showing in the table
      if (this.selectionss == "TOUS") {
        this.dataFrameFilter2 = this.dataFrame
      }
      this.InitializeVisualization();
      this.dataSource = new MatTableDataSource(this.dataFrameFilter2);
      this.executeVisualisation();
      // add paginator to the data
      this.dataSource.paginator = this.paginator;
    }
    else if(this.dataFrame != null  || this.dataFrameFilter!=null) {
      this.dataFrameFilter2 = this.dataFrameFilter.filter(item => this.getNbColor(item.code_navire, item.nb_pax_addon) === this.selectionss);
      //console.log(this.selectionss)
      // to choose witch data gonna be showing in the table
      if (this.selectionss == "TOUS") {
        this.dataFrameFilter2 = this.dataFrameFilter
      }
      this.InitializeVisualization();
      this.dataSource = new MatTableDataSource(this.dataFrameFilter2);
      this.executeVisualisation();
      // add paginator to the data
      this.dataSource.paginator = this.paginator;
    }

  }

  //observable for the checkBox execute every time the checkBox is changed
  executeVisualisation() {
    let c0: Observable<boolean> = this.date_depart.valueChanges;
    let c1: Observable<boolean> = this.armateur.valueChanges;
    let c2: Observable<boolean> = this.reseau.valueChanges;
    let c3: Observable<boolean> = this.code_navire.valueChanges;
    let c4: Observable<boolean> = this.port_depart.valueChanges;
    let c5: Observable<boolean> = this.port_arrivee.valueChanges;
    let c6: Observable<boolean> = this.res_type.valueChanges;
    let c7: Observable<boolean> = this.code_addon.valueChanges;
    let c8: Observable<boolean> = this.nb_pax_addon.valueChanges;
    let c9: Observable<boolean> = this.total_pax_traversee.valueChanges;
    let c10: Observable<boolean> = this.SEUIL.valueChanges;
    merge(c0, c1, c2, c3, c4, c5, c6, c7, c8, c9,c10).subscribe(v => {
      this.columnDefinitions[0].show = this.date_depart.value;
      this.columnDefinitions[1].show = this.armateur.value;
      this.columnDefinitions[2].show = this.reseau.value;
      this.columnDefinitions[3].show = this.code_navire.value;
      this.columnDefinitions[4].show = this.port_depart.value;
      this.columnDefinitions[5].show = this.port_arrivee.value;
      this.columnDefinitions[6].show = this.res_type.value;
      this.columnDefinitions[7].show = this.code_addon.value;
      this.columnDefinitions[8].show = this.nb_pax_addon.value;
      this.columnDefinitions[9].show = this.total_pax_traversee.value;
      this.columnDefinitions[10].show = this.SEUIL.value;
    });
  }

  // to initialize the visualisation with user's checkBox
  InitializeVisualization() {
    this.columnDefinitions = [
      { def: 'date_depart', label: 'date_depart', show: this.date_depart.value },
      { def: 'armateur', label: 'armateur', show: this.armateur.value },
      { def: 'reseau', label: 'reseau', show: this.reseau.value },
      { def: 'code_navire', label: 'code_navire', show: this.code_navire.value },
      { def: 'port_depart', label: 'port_depart', show: this.port_depart.value },
      { def: 'port_arrivee', label: 'port_arrivee', show: this.port_arrivee.value },
      { def: 'res_type', label: 'res_type', show: this.res_type.value },
      { def: 'code_addon', label: 'code_addon', show: this.code_addon.value },
      { def: 'nb_pax_addon', label: 'nb_pax_addon', show: this.nb_pax_addon.value },
      { def: 'total_pax_traversee', label: 'total_pax_traversee', show: this.total_pax_traversee.value },
      { def: 'SEUIL', label: 'SEUIL', show: this.SEUIL.value },
    ]
  }

  // declaring a form group for the checkBoxes
  form: FormGroup = new FormGroup({
    date_depart: new FormControl(true),
    armateur: new FormControl(true),
    reseau: new FormControl(true),
    code_navire: new FormControl(true),
    port_depart: new FormControl(true),
    port_arrivee: new FormControl(true),
    res_type: new FormControl(true),
    code_addon: new FormControl(true),
    nb_pax_addon: new FormControl(true),
    total_pax_traversee: new FormControl(true),
    SEUIL: new FormControl(true),
  });

  // geting the checkBox
  date_depart = this.form.get('date_depart');
  armateur = this.form.get('armateur');
  reseau = this.form.get('reseau');
  code_navire = this.form.get('code_navire');
  port_depart = this.form.get('port_depart');
  port_arrivee = this.form.get('port_arrivee');
  res_type = this.form.get('res_type');
  code_addon = this.form.get('code_addon');
  nb_pax_addon = this.form.get('nb_pax_addon');
  total_pax_traversee = this.form.get('total_pax_traversee');
  SEUIL = this.form.get('SEUIL');

  //Control column ordering and which columns are displayed.
  columnDefinitions = [
    { def: 'date_depart', label: 'date_depart', show: this.date_depart.value },
    { def: 'armateur', label: 'armateur', show: this.armateur.value },
    { def: 'reseau', label: 'reseau', show: this.reseau.value },
    { def: 'code_navire', label: 'code_navire', show: this.code_navire.value },
    { def: 'port_depart', label: 'port_depart', show: this.port_depart.value },
    { def: 'port_arrivee', label: 'port_arrivee', show: this.port_arrivee.value },
    { def: 'res_type', label: 'res_type', show: this.res_type.value },
    { def: 'code_addon', label: 'code_addon', show: this.code_addon.value },
    { def: 'nb_pax_addon', label: 'nb_pax_addon', show: this.nb_pax_addon.value },
    { def: 'total_pax_traversee', label: 'total_pax_traversee', show: this.total_pax_traversee.value },
    { def: 'SEUIL', label: 'SEUIL', show: this.SEUIL.value },
  ]

  // Filter data in witch columns is checked
  getDisplayedColumns(): string[] {
    return this.columnDefinitions.filter(cd => cd.show).map(cd => cd.def);
  }
}
