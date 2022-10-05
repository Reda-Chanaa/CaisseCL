import { Component, ElementRef, ViewChild } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { merge, Observable } from 'rxjs';
import { FormControl, FormGroup } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { Options } from 'selenium-webdriver';

@Injectable({
  providedIn: 'root'
})
// class pour les requettes GET et POST.
export class ApiStat {

  baseurl = "http://127.0.0.1:7000";

  constructor(private http: HttpClient) {

  }
  sendFileDebit(File1: any,File2: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/adv-debit/', formData, { headers: header })
  }

  sendFileCredit(File1: any,File2: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/adv-credit/', formData, { headers: header })
  }
  sendSumDebit(File1: any,File2: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/adv-sum-debit/', formData, { headers: header})
  }
  sendSumCredit(File1: any,File2: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/adv-sum-credit/', formData, { headers: header})
  }

}

// interface StatData qui précise les données affichées dans le tableau ainsi que leur type.
export interface StatData {
  Transaction: string;
  Commande: string;
  Mode: string;
  Montant: string;
  Commentaires: string;

}
@Component({
  selector: 'app-cvd',
  templateUrl: './cvd.component.html',
  styleUrls: ['./cvd.component.css'],
  providers: [ApiStat]
})
export class CVDComponent {

  @ViewChild('TABLE') table: ElementRef;
  @ViewChild('TABLE2') table2: ElementRef;

  @ViewChild('MatPaginator') paginator: MatPaginator;
  @ViewChild('MatPaginator2') paginator2: MatPaginator;

  day = new Date().getDate()
  moiss = new Date().getMonth() + 1
  annees = new Date().getFullYear()
  date: any

  selection: string;
  selections: string;

  dataFrame: any;
  dataFrame2: any;

  displayedColumns: string[] = ['Transaction', 'Commande', 'Mode', 'Montant', 'Commentaires'];
  displayedColumns2: string[] = ['Mode', 'Montant'];

  dataSource: MatTableDataSource<StatData>;
  dataSource2: MatTableDataSource<StatData>;

  element: any;
  df1: any;
  df2: any;

  annee: string;

  value: number = 10;
  value2: number = 10;

  constructor(private DATACLEANING: ApiStat) {
    // Assign the data to the data source for the table to render
    this.dataSource = new MatTableDataSource([]);
    this.dataSource2 = new MatTableDataSource([]);
  }

  // function executed when file is changed
  fileChangeListener1($event: any): void {
    this.df1 = $event.target.files[0]
  }

  // function executed when file is changed
  fileChangeListener2($event: any): void {
    this.df2 = $event.target.files[0]
  }

  deleteData() {
    this.dataSource = new MatTableDataSource([]);
  }
  // function executed when user click on Reporting button
  createFile = () => {

    if (this.df1 != null) {
      if (this.selections == "debit") {
        this.value = 0
        this.DATACLEANING.sendFileDebit(this.df1,this.df2).subscribe(
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
      if (this.selections == "credit") {
        this.value = 0
        this.DATACLEANING.sendFileCredit(this.df1,this.df2).subscribe(
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
  }

  // function executed when user click on Reporting button
  createSum = () => {

    if (this.df1 != null) {
      if (this.selections == "debit") {
        this.value = 0
        this.DATACLEANING.sendSumDebit(this.df1,this.df2).subscribe(
          data => {
            this.value = 10
            this.dataFrame2 = data;
            console.log(this.dataFrame2)
            // to choose witch data gonna be showing in the table
            this.InitializeVisualization();
            // puts data into the datasource table
            this.dataSource2 = new MatTableDataSource(data);
            // execute the visualisation function
            this.executeVisualisation();
            // add paginator to the data
            this.dataSource2.paginator = this.paginator2;
          },
          error => {
            console.log("error ", error);
          }
        );
      }
      if (this.selections == "credit") {
        this.value = 0
        this.DATACLEANING.sendSumCredit(this.df1,this.df2).subscribe(
          data => {
            this.value = 10
            this.dataFrame2 = data;
            console.log(this.dataFrame2)
            // to choose witch data gonna be showing in the table
            this.InitializeVisualization();
            // puts data into the datasource table
            this.dataSource2 = new MatTableDataSource(data);
            // execute the visualisation function
            this.executeVisualisation();
            // add paginator to the data
            this.dataSource2.paginator = this.paginator2;
          },
          error => {
            console.log("error ", error);
          }
        );
      }
    }
  }

  deleteSum() {
    this.dataSource2 = new MatTableDataSource([]);
  }
  //observable for the checkBox execute every time the checkBox is changed
  executeVisualisation() {
    let c0: Observable<boolean> = this.Transaction.valueChanges;
    let c1: Observable<boolean> = this.Commande.valueChanges;
    let c2: Observable<boolean> = this.Mode.valueChanges;
    let c3: Observable<boolean> = this.Montant.valueChanges;
    let c4: Observable<boolean> = this.Commentaires.valueChanges;
    merge(c0, c1, c2, c3, c4).subscribe(v => {
      this.columnDefinitions[0].show = this.Transaction.value;
      this.columnDefinitions[1].show = this.Commande.value;
      this.columnDefinitions[2].show = this.Mode.value;
      this.columnDefinitions[3].show = this.Montant.value;
      this.columnDefinitions[4].show = this.Commentaires.value;
    });
  }

  // to initialize the visualisation with user's checkBox
  InitializeVisualization() {
    this.columnDefinitions = [
      { def: 'Transaction', label: 'Transaction', show: this.Transaction.value },
      { def: 'Commande', label: 'Commande', show: this.Commande.value },
      { def: 'Mode', label: 'Mode', show: this.Mode.value },
      { def: 'Montant', label: 'Montant', show: this.Montant.value },
      { def: 'Commentaires', label: 'Commentaires', show: this.Commentaires.value },
    ]
  }

  // declaring a form group for the checkBoxes
  form: FormGroup = new FormGroup({
    Transaction: new FormControl(true),
    Commande: new FormControl(true),
    Mode: new FormControl(true),
    Montant: new FormControl(true),
    Commentaires: new FormControl(true),
  });

  // geting the checkBox
  Transaction = this.form.get('Transaction');
  Commande = this.form.get('Commande');
  Mode = this.form.get('Mode');
  Montant = this.form.get('Montant');
  Commentaires = this.form.get('Commentaires');

  //Control column ordering and which columns are displayed.
  columnDefinitions = [
    { def: 'Transaction', label: 'Transaction', show: this.Transaction.value },
    { def: 'Commande', label: 'Commande', show: this.Commande.value },
    { def: 'Mode', label: 'Mode', show: this.Mode.value },
    { def: 'Montant', label: 'Montant', show: this.Montant.value },
    { def: 'Commentaires', label: 'Commentaires', show: this.Commentaires.value },
  ]

  //Control column ordering and which columns are displayed.
  columnDefinitions2 = [
    { def: 'Mode', label: 'Mode', show: this.Mode.value },
    { def: 'Montant', label: 'Montant', show: this.Montant.value },
  ]

  // Filter data in witch columns is checked
  getDisplayedColumns(): string[] {
    return this.columnDefinitions.filter(cd => cd.show).map(cd => cd.def);
  }

  // Filter data in witch columns is checked
  getDisplayedColumns2(): string[] {
    return this.columnDefinitions2.filter(cd => cd.show).map(cd => cd.def);
  }

}
