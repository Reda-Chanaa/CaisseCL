from datetime import datetime
import pandas as pd
import numpy as np
from django.http import HttpResponse
from datetime import datetime


def Cvd_debit(df1):

    df_seaware = df1[(df1["Type Trans."] == "PMNT")
                     & (df1["Mode pmt"] != "TERMS") &
                     (df1["Mode pmt"] != "TO REFUND")]
    df_seaware['Transaction'] = df_seaware['Num. Trans.'].astype(str).str[2:]
    df_seaware['Montant init.'] = df_seaware['Montant init.'].astype(float)
    df_seaware['Montant'] = df_seaware['Montant init.']
    df_seaware['Mode'] = df_seaware['Mode pmt']
    df_seaware['Commande'] = df_seaware['Num. Dest.']
    print("number seaware : ", len(df_seaware))

    print(len(df_seaware))

    return df_seaware


def CvdDebit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]

        df1 = pd.read_excel(File1)

        print("df1", df1)
        # Stats
        data = Cvd_debit(df1)
        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))


def Cvd_Credit(df1):

    df_seaware = df1[(df1["Type Trans."] == "REFUND") |
                     (df1["Type Trans."] == "MANREFUND")]
    df_seaware['Transaction'] = df_seaware['Num. Trans.'].astype(str).str[2:]
    df_seaware['Montant init.'] = df_seaware['Montant init.'].astype(float)
    df_seaware['Montant'] = df_seaware['Montant init.']
    df_seaware['Mode'] = df_seaware['Mode pmt']
    df_seaware['Commande'] = df_seaware['Num. Dest.']
    print("number seaware : ", len(df_seaware))

    return df_seaware


def CvdCredit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]

        df1 = pd.read_excel(File1)

        print("df1", df1)
        # Stats
        data = Cvd_Credit(df1)
        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))


def Cvd_Somme_Debit(df1):

    df_seaware = df1[(df1["Type Trans."] == "PMNT")
                     & (df1["Mode pmt"] != "TERMS") &
                     (df1["Mode pmt"] != "TO REFUND")]
    df_sum = df_seaware.groupby(['Mode pmt'],
                                as_index=False)['Montant init.'].sum()
    df_sum.reset_index(inplace=True)
    df_sum['Montant'] = df_sum['Montant init.']
    df_sum['Mode'] = df_sum['Mode pmt']
    df_sum.reset_index(inplace=True)
    print(df_sum.columns)

    print("number seaware : ", len(df_sum))

    return df_sum


def CvdSumDebit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        #annee = request.POST["annee"]

        df1 = pd.read_excel(File1)

        print("df1", df1)
        # Stats
        data = Cvd_Somme_Debit(df1)

        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))


def Cvd_Somme_Credit(df1):

    df_seaware = df1[(df1["Type Trans."] == "REFUND") |
                     (df1["Type Trans."] == "MANREFUND")]
    df_sum = df_seaware.groupby(['Mode pmt'],
                                as_index=False)['Montant init.'].sum()
    df_sum.reset_index(inplace=True)
    df_sum['Montant'] = df_sum['Montant init.']
    df_sum['Mode'] = df_sum['Mode pmt']
    df_sum.reset_index(inplace=True)
    print(df_sum.columns)

    print("number seaware : ", len(df_sum))

    return df_sum


def CvdSumCredit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        #annee = request.POST["annee"]

        df1 = pd.read_excel(File1)

        print("df1", df1)
        # Stats
        data = Cvd_Somme_Credit(df1)

        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))
