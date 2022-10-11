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
  debitOui(File1: any, File2: any, File3: any, File4: any, File5: any, File6: any,File7: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    formData.append("file3", File3, File.name);
    formData.append('file4', File4, File.name);
    formData.append('file5', File5, File.name);
    formData.append("file6", File6, File.name);
    formData.append("file7", File7, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/journal-debit-oui/', formData, { headers: header })
  }
  creditOui(File1: any, File2: any, File3: any, File4: any, File5: any, File6: any,File7: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    formData.append("file3", File3, File.name);
    formData.append('file4', File4, File.name);
    formData.append('file5', File5, File.name);
    formData.append("file6", File6, File.name);
    formData.append("file7", File7, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/journal-credit-oui/', formData, { headers: header })
  }
  debitNon(File1: any, File2: any, File3: any, File4: any, File5: any, File6: any,File7: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    formData.append("file3", File3, File.name);
    formData.append('file4', File4, File.name);
    formData.append('file5', File5, File.name);
    formData.append("file6", File6, File.name);
    formData.append("file7", File7, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/journal-debit-non/', formData, { headers: header })
  }
  creditNon(File1: any, File2: any, File3: any, File4: any, File5: any, File6: any,File7: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    formData.append("file3", File3, File.name);
    formData.append('file4', File4, File.name);
    formData.append('file5', File5, File.name);
    formData.append("file6", File6, File.name);
    formData.append("file7", File7, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/journal-credit-non/', formData, { headers: header })
  }
}
// interface StatData qui précise les données affichées dans le tableau ainsi que leur type.
export interface StatData {
  Comptes: string;
  Gestions: string;
  Libelles: string;
  NB: string;
  Montants: string;

}
@Component({
  selector: 'app-journal',
  templateUrl: './journal.component.html',
  styleUrls: ['./journal.component.css'],
  providers: [ApiStat]
})
export class JournalComponent {

  @ViewChild('TABLE') table: ElementRef;

  day = new Date().getDate()
  moiss = new Date().getMonth() + 1
  annees = new Date().getFullYear()
  date: any

  selections: string;
  selectionss: string;
  /*
  pickerVeille:Date;
  pickerJour:Date;

  veille = new FormControl('');
  jour = new FormControl('');*/

  dataFrame: any;

  displayedColumns: string[] = ['Comptes', 'Gestions', 'Libelles', 'NB', 'Montants'];
  dataSource: MatTableDataSource<StatData>;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  df1: any;
  df2: any;
  df3: any;
  df4: any;
  df5: any;
  df6: any;
  df7: any;

  value: number;

  constructor(private DATACLEANING: ApiStat) {
    // Assign the data to the data source for the table to render
    this.dataSource = new MatTableDataSource([]);
  }

  // function executed when file is changed
  fileChangeListener1($event: any): void {
    this.df1 = $event.target.files[0]
  }
  // function executed when file is changed
  fileChangeListener2($event: any): void {
    this.df2 = $event.target.files[0]
  }
  // function executed when file is changed
  fileChangeListener3($event: any): void {
    this.df3 = $event.target.files[0]
  }
  // function executed when file is changed
  fileChangeListener4($event: any): void {
    this.df4 = $event.target.files[0]
  }
  // function executed when file is changed
  fileChangeListener5($event: any): void {
    this.df5 = $event.target.files[0]
  }
  // function executed when file is changed
  fileChangeListener6($event: any): void {
    this.df6 = $event.target.files[0]
  }
  // function executed when file is changed
  fileChangeListener7($event: any): void {
    this.df7 = $event.target.files[0]
  }

  deleteData() {
    this.dataSource = new MatTableDataSource([]);
  }

  printTable() {
    const printContents = document.getElementById("reporting").outerHTML
    var newWin = window.open("");
    newWin.document.write(`
      <html>
        <head>
          <title>Journal 39 Internet - ADV - SAV</title>
          <style>
          table th, table td {
            border-top: 0.25px solid #000;
            padding:0.25em;
          }
          </style>
        </head>
    <body onload="window.print();window.close()">${printContents}</body>
      </html>`
    );
    newWin.print();
    newWin.close();

  }
  // function executed when user click on Reporting button
  createFile = () => {

    if (this.df1 != null && this.df2 != null && this.df3 != null && this.df4 != null && this.df5 != null && this.df6 != null && this.df7 != null) {
      if (this.selections == "credit") {
        if(this.selectionss == "oui"){
        this.value = 0
        this.DATACLEANING.creditOui(this.df1, this.df2, this.df3, this.df4, this.df5, this.df6, this.df7).subscribe(
          data => {
            this.value = 10
            this.dataFrame = data;
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
      if(this.selectionss == "non"){
        this.value = 0
        this.DATACLEANING.creditNon(this.df1, this.df2, this.df3, this.df4, this.df5, this.df6, this.df7).subscribe(
          data => {
            this.value = 10
            this.dataFrame = data;
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
      }}
      if (this.selections == "debit") {
        if(this.selectionss == "oui"){
        this.value = 0
        this.DATACLEANING.debitOui(this.df1, this.df2, this.df3, this.df4, this.df5, this.df6, this.df7).subscribe(
          data => {
            this.value = 10
            this.dataFrame = data;
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
      if(this.selectionss == "non"){
        this.value = 0
        this.DATACLEANING.debitNon(this.df1, this.df2, this.df3, this.df4, this.df5, this.df6, this.df7).subscribe(
          data => {
            this.value = 10
            this.dataFrame = data;
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
  }
  // Prevent no number type input, valid characters in input are numbers only
  _keyPress(event: any) {
    //console.log(this.paq1.value.toISOString())
    const pattern = /^[0-9]*$/;
    let inputChar = String.fromCharCode(event.charCode);

    if (!pattern.test(inputChar)) {
      // invalid character, prevent input
      event.preventDefault();
    }
  }

  //observable for the checkBox execute every time the checkBox is changed
  executeVisualisation() {
    let c0: Observable<boolean> = this.Comptes.valueChanges;
    let c1: Observable<boolean> = this.Gestions.valueChanges;
    let c2: Observable<boolean> = this.Libelles.valueChanges;
    let c3: Observable<boolean> = this.NB.valueChanges;
    let c4: Observable<boolean> = this.Montants.valueChanges;
    merge(c0, c1, c2, c3, c4).subscribe(v => {
      this.columnDefinitions[0].show = this.Comptes.value;
      this.columnDefinitions[1].show = this.Gestions.value;
      this.columnDefinitions[2].show = this.Libelles.value;
      this.columnDefinitions[3].show = this.NB.value;
      this.columnDefinitions[4].show = this.Montants.value;
    });
  }

  // to initialize the visualisation with user's checkBox
  InitializeVisualization() {
    this.columnDefinitions = [
      { def: 'Comptes', label: 'Comptes', show: this.Comptes.value },
      { def: 'Gestions', label: 'Gestions', show: this.Gestions.value },
      { def: 'Libelles', label: 'Libelles', show: this.Libelles.value },
      { def: 'NB', label: 'NB', show: this.NB.value },
      { def: 'Montants', label: 'Montants', show: this.Montants.value },
    ]
  }

  // declaring a form group for the checkBoxes
  form: FormGroup = new FormGroup({
    Comptes: new FormControl(true),
    Gestions: new FormControl(true),
    Libelles: new FormControl(true),
    NB: new FormControl(true),
    Montants: new FormControl(true),
  });

  // geting the checkBox
  Comptes = this.form.get('Comptes');
  Gestions = this.form.get('Gestions');
  Libelles = this.form.get('Libelles');
  NB = this.form.get('NB');
  Montants = this.form.get('Montants');

  //Control column ordering and which columns are displayed.
  columnDefinitions = [
    { def: 'Comptes', label: 'Comptes', show: this.Comptes.value },
    { def: 'Gestions', label: 'Gestions', show: this.Gestions.value },
    { def: 'Libelles', label: 'Libelles', show: this.Libelles.value },
    { def: 'NB', label: 'NB', show: this.NB.value },
    { def: 'Montants', label: 'Montants', show: this.Montants.value },
  ]

  // Filter data in witch columns is checked
  getDisplayedColumns(): string[] {
    return this.columnDefinitions.filter(cd => cd.show).map(cd => cd.def);
  }

}
