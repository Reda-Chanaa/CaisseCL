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
  sendFileAmexDebit(File1: any, File2: any, File3: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    formData.append("file3", File3, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/internet-amex-debit/', formData, { headers: header })
  }

  sendFilePaypalDebit(File1: any, File2: any, File3: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    formData.append("file3", File3, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/internet-paypal-debit/', formData, { headers: header })
  }

  sendFileCcDebit(File1: any, File2: any, File3: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    formData.append("file3", File3, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/internet-cc-debit/', formData, { headers: header })
  }

  sendFileAmexCredit(File1: any, File2: any, File3: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    formData.append("file3", File3, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/internet-amex-credit/', formData, { headers: header })
  }

  sendFilePaypalCredit(File1: any, File2: any, File3: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    formData.append("file3", File3, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/internet-paypal-credit/', formData, { headers: header })
  }

  sendFileCcCredit(File1: any, File2: any, File3: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    formData.append("file3", File3, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'multipart/form-data');
    return this.http.post(this.baseurl + '/internet-cc-credit/', formData, { headers: header })
  }
  sendPhrase(File1: any, File2: any, File3: any): Observable<any> {

    let formData = new FormData();
    formData.append('file1', File1, File.name);
    formData.append('file2', File2, File.name);
    formData.append("file3", File3, File.name);
    console.log(formData)

    var header = new HttpHeaders();
    header.append('Content-Type', 'application/json');
    return this.http.post(this.baseurl + '/internet-phrase/', formData, { headers: header, responseType: 'text' })
  }

}

// interface StatData qui précise les données affichées dans le tableau ainsi que leur type.
export interface StatData {
  Transaction: string;
  Commande: string;
  MontantSeaware: string;
  MontantCepac: string;
  Ecart: string;

}
@Component({
  selector: 'app-internet',
  templateUrl: './internet.component.html',
  styleUrls: ['./internet.component.css'],
  providers: [ApiStat]
})
export class InternetComponent {

  @ViewChild('TABLE') table: ElementRef;

  day = new Date().getDate()
  moiss = new Date().getMonth() + 1
  annees = new Date().getFullYear()
  date = "ECART_INTERNET"

  selection: string;
  selections: string;
  /*
  pickerVeille:Date;
  pickerJour:Date;

  veille = new FormControl('');
  jour = new FormControl('');*/

  dataFrame: any;

  displayedColumns: string[] = ['Transaction', 'Commande', 'MontantSeaware', 'MontantCepac', 'Ecart'];
  dataSource: MatTableDataSource<StatData>;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  element: any;
  df1: any;
  df2: any;
  df3: any;
  annee: string;

  phrase: string = "";
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

  deleteData() {
    this.dataSource = new MatTableDataSource([]);
  }
  // function executed when user click on Reporting button
  createFile = () => {

    if (this.df1 != null && this.df2 != null && this.df3 != null) {
      if (this.selection == "amex") {
        if (this.selections == "debit") {
          this.value = 0
          this.DATACLEANING.sendFileAmexDebit(this.df1, this.df2, this.df3).subscribe(
            data => {
              this.value = 10
              this.dataFrame = data;
              this.date = this.date + "_AMEX_DEBIT"
              // to choose witch data gonna be showing in the table
              this.InitializeVisualization();
              let re = ".";
              data.forEach(element => {
                element.Ecart = element.Ecart.replace(re, ",");
                element.MontantSeaware = element.MontantSeaware.replace(re, ",");
                element.MontantCepac = element.MontantCepac.replace(re, ",");
              });
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
          this.DATACLEANING.sendFileAmexCredit(this.df1, this.df2, this.df3).subscribe(
            data => {
              this.value = 10
              this.dataFrame = data;
              this.date = this.date + "_AMEX_CREDIT"
              // to choose witch data gonna be showing in the table
              this.InitializeVisualization();
              let re = ".";
              data.forEach(element => {
                element.Ecart = element.Ecart.replace(re, ",");
                element.MontantSeaware = element.MontantSeaware.replace(re, ",");
                element.MontantCepac = element.MontantCepac.replace(re, ",");
              });
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
      if (this.selection == "paypal") {
        if (this.selections == "debit") {
          this.value = 0
          this.DATACLEANING.sendFilePaypalDebit(this.df1, this.df2, this.df3).subscribe(
            data => {
              this.value = 10
              this.dataFrame = data;
              this.date = this.date + "_PAYPAL_DEBIT"
              // to choose witch data gonna be showing in the table
              this.InitializeVisualization();
              let re = ".";
              data.forEach(element => {
                element.Ecart = element.Ecart.replace(re, ",");
                element.MontantSeaware = element.MontantSeaware.replace(re, ",");
                element.MontantCepac = element.MontantCepac.replace(re, ",");
              });
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
          this.DATACLEANING.sendFilePaypalCredit(this.df1, this.df2, this.df3).subscribe(
            data => {
              this.value = 10
              this.dataFrame = data;
              this.date = this.date + "_PAYPAL_CREDIT"
              // to choose witch data gonna be showing in the table
              this.InitializeVisualization();
              let re = ".";
              data.forEach(element => {
                element.Ecart = element.Ecart.replace(re, ",");
                element.MontantSeaware = element.MontantSeaware.replace(re, ",");
                element.MontantCepac = element.MontantCepac.replace(re, ",");
              });
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
      if (this.selection == "cc") {
        if (this.selections == "debit") {
          this.value = 0
          this.DATACLEANING.sendFileCcDebit(this.df1, this.df2, this.df3).subscribe(
            data => {
              this.value = 10
              this.dataFrame = data;
              this.date = this.date + "_CC_DEBIT"
              // to choose witch data gonna be showing in the table
              this.InitializeVisualization();
              let re = ".";
              data.forEach(element => {
                element.Ecart = element.Ecart.replace(re, ",");
                element.MontantSeaware = element.MontantSeaware.replace(re, ",");
                element.MontantCepac = element.MontantCepac.replace(re, ",");
              });
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
          this.DATACLEANING.sendFileCcCredit(this.df1, this.df2, this.df3).subscribe(
            data => {
              this.value = 10
              this.dataFrame = data;
              this.date = this.date + "_CC_CREDIT"
              // to choose witch data gonna be showing in the table
              this.InitializeVisualization();
              let re = ".";
              data.forEach(element => {
                element.Ecart = element.Ecart.replace(re, ",");
                element.MontantSeaware = element.MontantSeaware.replace(re, ",");
                element.MontantCepac = element.MontantCepac.replace(re, ",");
              });
              // puts data into the datasource table
              this.dataSource = new MatTableDataSource(data);
              // execute the visualisation function
              this.executeVisualisation();
              // add paginator to the data
              this.dataSource.paginator = this.paginator;
            },
            error => {
              console.log("error ", error);
              console.log(error.text)
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

  createPhrase = () => {

    if (this.df1 != null && this.df2 != null && this.df3 != null) {
      this.value = 0
      this.DATACLEANING.sendPhrase(this.df1, this.df2, this.df3).subscribe(
        data => {
          this.value = 10
          this.phrase = data;
          console.log(this.phrase)
        },
        error => {
          console.log("error ", error);
        }
      );
    }
  }

  deletePhrase() {
    this.phrase = ''
  }
  //observable for the checkBox execute every time the checkBox is changed
  executeVisualisation() {
    let c0: Observable<boolean> = this.Transaction.valueChanges;
    let c1: Observable<boolean> = this.Commande.valueChanges;
    let c2: Observable<boolean> = this.MontantSeaware.valueChanges;
    let c3: Observable<boolean> = this.MontantCepac.valueChanges;
    let c4: Observable<boolean> = this.Ecart.valueChanges;
    merge(c0, c1, c2, c3, c4).subscribe(v => {
      this.columnDefinitions[0].show = this.Transaction.value;
      this.columnDefinitions[1].show = this.Commande.value;
      this.columnDefinitions[2].show = this.MontantSeaware.value;
      this.columnDefinitions[3].show = this.MontantCepac.value;
      this.columnDefinitions[4].show = this.Ecart.value;
    });
  }

  // to initialize the visualisation with user's checkBox
  InitializeVisualization() {
    this.columnDefinitions = [
      { def: 'Transaction', label: 'Transaction', show: this.Transaction.value },
      { def: 'Commande', label: 'Commande', show: this.Commande.value },
      { def: 'MontantSeaware', label: 'MontantSeaware', show: this.MontantSeaware.value },
      { def: 'MontantCepac', label: 'MontantCepac', show: this.MontantCepac.value },
      { def: 'Ecart', label: 'Ecart', show: this.Ecart.value },
    ]
  }

  // declaring a form group for the checkBoxes
  form: FormGroup = new FormGroup({
    Transaction: new FormControl(true),
    Commande: new FormControl(true),
    MontantSeaware: new FormControl(true),
    MontantCepac: new FormControl(true),
    Ecart: new FormControl(true),
  });

  // geting the checkBox
  Transaction = this.form.get('Transaction');
  Commande = this.form.get('Commande');
  MontantSeaware = this.form.get('MontantSeaware');
  MontantCepac = this.form.get('MontantCepac');
  Ecart = this.form.get('Ecart');

  //Control column ordering and which columns are displayed.
  columnDefinitions = [
    { def: 'Transaction', label: 'Transaction', show: this.Transaction.value },
    { def: 'Commande', label: 'Commande', show: this.Commande.value },
    { def: 'MontantSeaware', label: 'MontantSeaware', show: this.MontantSeaware.value },
    { def: 'MontantCepac', label: 'MontantCepac', show: this.MontantCepac.value },
    { def: 'Ecart', label: 'Ecart', show: this.Ecart.value },
  ]

  // Filter data in witch columns is checked
  getDisplayedColumns(): string[] {
    return this.columnDefinitions.filter(cd => cd.show).map(cd => cd.def);
  }

}
