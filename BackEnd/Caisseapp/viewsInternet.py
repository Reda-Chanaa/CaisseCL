import calendar
from colorsys import hsv_to_rgb
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
from django.http import HttpResponse
from datetime import datetime


def Internet_files_AMEX_debit(df1, df2):

    df_seaware = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") &
                     (df1['Utilisateur'].str.contains('BLO', na=False)) &
                     (df1['Commentaires'].str.contains('AMEX', na=False))]
    df_seaware['Transaction'] = df_seaware['Num. Trans.'].astype(str).str[2:]
    df_seaware['Montant init.'] = df_seaware['Montant init.'].astype(float)
    print("number seaware : ", len(df_seaware))

    df_cepac = df2[(df2["Type"] == "Débit")
                   & (df2["Moyen de paiement"] == "AMEX") &
                   (df2["Info. compl."].str.contains('INT', na=False))]
    df_cepac['Transaction'] = df_cepac['Transaction'].astype(str)
    df_cepac['Montant du paiement'] = df_cepac['Montant du paiement'].astype(
        float)
    print("number remisé : ", len(df_cepac))
    merged = pd.merge(df_cepac, df_seaware, on='Transaction')

    merged["MontantSeaware"] = merged['Montant init.']
    merged["MontantCepac"] = merged['Montant du paiement']
    merged["Ecart"] = merged["MontantCepac"] - merged["MontantSeaware"]
    ecart=merged[merged["Ecart"]!=0]
    print(len(ecart))
    
    return ecart

def InternetAmexDebit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        File2 = request.FILES["file2"]
        File3 = request.FILES["file3"]
        #annee = request.POST["annee"]

        df1 = pd.read_excel(File1)
        df2 = pd.read_excel(File2)
        df3 = pd.read_excel(File3)

        print("df1", df1)
        print("df2", df2)
        #print("df3",df3)
        # Stats
        data = Internet_files_AMEX_debit(df1, df2)
        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))



def Internet_files_AMEX_Credit(df1, df2):

    df_seaware = df1[(df1["Type Trans."] == "REFUND") & (df1["Statut"] == "OK") &
                     (df1['Utilisateur'].str.contains('BLO', na=False)) &
                     (df1['Commentaires'].str.contains('AMEX', na=False))]
    df_seaware['Transaction'] = df_seaware['Num. Trans.'].astype(str).str[2:]
    df_seaware['Montant init.'] = df_seaware['Montant init.'].astype(float)
    print("number seaware : ", len(df_seaware))

    df_cepac = df2[(df2["Type"] == "Crédit")
                   & (df2["Moyen de paiement"] == "AMEX") &
                   (df2["Info. compl."].str.contains('INT', na=False))]
    df_cepac['Transaction'] = df_cepac['Transaction'].astype(str)
    df_cepac['Montant du paiement'] = df_cepac['Montant du paiement'].astype(
        float)
    print("number remisé : ", len(df_cepac))
    merged = pd.merge(df_cepac, df_seaware, on='Transaction')

    merged["MontantSeaware"] = merged['Montant init.']
    merged["MontantCepac"] = merged['Montant du paiement']
    merged["Ecart"] = merged["MontantCepac"] - merged["MontantSeaware"]
    ecart=merged[merged["Ecart"]!=0]
    print(len(ecart))
    
    return ecart

def InternetAmexCredit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        File2 = request.FILES["file2"]
        File3 = request.FILES["file3"]
        #annee = request.POST["annee"]

        df1 = pd.read_excel(File1)
        df2 = pd.read_excel(File2)
        df3 = pd.read_excel(File3)

        print("df1", df1)
        print("df2", df2)
        #print("df3",df3)
        # Stats
        data = Internet_files_AMEX_Credit(df1, df2)
        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))



def Internet_files_Cc_debit(df1, df2, df3):

    df_seaware = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") &
                     (df1['Utilisateur'].str.contains('BLO', na=False)) &
                     (~df1['Commentaires'].str.contains('AMEX', na=False)) &
                     (~df1['Commentaires'].str.contains('PPAL', na=False))]
    df_seaware['Transaction'] = df_seaware['Num. Trans.'].astype(str).str[2:]
    df_seaware['Montant init.'] = df_seaware['Montant init.'].astype(float)
    print("number seaware : ", len(df_seaware))

    df_cepac = df2[(df2["Type"] == "Débit")
                   & (df2["Moyen de paiement"] != "PAYPAL") &
                   (df2["Moyen de paiement"] != "AMEX") &
                   (df2["Info. compl."].str.contains('INT', na=False))]
    df_cepac['Transaction'] = df_cepac['Transaction'].astype(str)
    df_cepac['Montant du paiement'] = df_cepac['Montant du paiement'].astype(
        float)
    print("number remisé : ", len(df_cepac))
    merged = pd.merge(df_cepac, df_seaware, on='Transaction')

    merged["MontantSeaware"] = merged['Montant init.']
    merged["MontantCepac"] = merged['Montant du paiement']
    merged["Ecart"] = merged["MontantCepac"] - merged["MontantSeaware"]
    ecart=merged[merged["Ecart"]!=0]
    print(len(ecart))
    
    return ecart

def InternetCcDebit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        File2 = request.FILES["file2"]
        File3 = request.FILES["file3"]
        #annee = request.POST["annee"]

        df1 = pd.read_excel(File1)
        df2 = pd.read_excel(File2)
        df3 = pd.read_excel(File3)

        print("df1", df1)
        print("df2", df2)
        print("df3", df3)
        # Stats
        data = Internet_files_Cc_debit(df1, df2, df3)
        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))



def Internet_files_Cc_credit(df1, df2, df3):

    df_seaware = df1[(df1["Type Trans."] == "REFUND")]
    df_seaware['Transaction'] = df_seaware['Num. Trans.'].astype(str).str[2:]
    df_seaware['Montant init.'] = df_seaware['Montant init.'].astype(float)
    print("number seaware : ", len(df_seaware))

    df_cepac = df2[(df2["Type"] == "Crédit")]
    df_cepac['Transaction'] = df_cepac['Transaction'].astype(str)
    df_cepac['Montant du paiement'] = df_cepac['Montant du paiement'].astype(
        float)
    print("number remisé : ", len(df_cepac))
    merged = pd.merge(df_cepac, df_seaware, on='Transaction')

    merged["MontantSeaware"] = merged['Montant init.']
    merged["MontantCepac"] = merged['Montant du paiement']
    merged["Ecart"] = merged["MontantCepac"] - merged["MontantSeaware"]
    ecart=merged[merged["Ecart"]!=0]
    print(len(ecart))
    
    return ecart

def InternetCcCredit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        File2 = request.FILES["file2"]
        File3 = request.FILES["file3"]
        #annee = request.POST["annee"]

        df1 = pd.read_excel(File1)
        df2 = pd.read_excel(File2)
        df3 = pd.read_excel(File3)

        print("df1", df1)
        print("df2", df2)
        print("df3", df3)
        # Stats
        data = Internet_files_Cc_credit(df1, df2, df3)
        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))



def Internet_cc_phrase(df1, df2, df3):

    df_seaware = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") &
                     (df1['Utilisateur'].str.contains('BLO', na=False)) &
                     (~df1['Commentaires'].str.contains('AMEX', na=False)) &
                     (~df1['Commentaires'].str.contains('PPAL', na=False))]
    df_seaware['Transaction'] = df_seaware['Num. Trans.'].astype(str).str[2:]
    df_seaware['Montant init.'] = df_seaware['Montant init.'].astype(float)
    print("tpe:",df_seaware['Date transaction'].dtypes)
    if(df_seaware['Date transaction'].dtypes=='datetime64[ns]'):
        df_seaware['date'] =  df_seaware['Date transaction'].dt.date
    else:
        df_seaware['date'] = df_seaware['Date transaction'].astype('datetime64[ns]')
        df_seaware['date']=df_seaware['date'].dt.date
        df_seaware['date']=df_seaware['date'].astype(str)

    df_seaware.reset_index(inplace=True)
    print("number seaware : ", len(df_seaware))
    print("date seaware : ", df_seaware['date'][0])
    
    df_cepac_remise = df2[(df2["Type"] == "Débit")
                   & (df2["Moyen de paiement"] != "PAYPAL") &
                   (df2["Moyen de paiement"] != "AMEX") &
                   (df2["Info. compl."].str.contains('INT', na=False))]
    df_cepac_remise['Transaction'] = df_cepac_remise['Transaction'].astype(str)
    df_cepac_remise['Montant du paiement'] = df_cepac_remise['Montant du paiement'].astype(
        float)
    
    if(df_cepac_remise['Date du paiement'].dtypes=='datetime64[ns]'):
        df_cepac_remise['date'] = df_cepac_remise['Date du paiement'].dt.date
        df_cepac_remise['date'] = df_cepac_remise['date'].astype(str)
    else:
        df_cepac_remise['date'] = pd.to_datetime(df_cepac_remise['Date du paiement'],  format = '%d/%m/%Y %H:%M:%S')
        print("tpe:",df_cepac_remise['date'].dtypes)
        df_cepac_remise['date'] = df_cepac_remise['date'].dt.date
        df_cepac_remise['date'] = df_cepac_remise['date'].astype(str)
    df_cepac_remise.reset_index(inplace=True)

    print("number remisé : ", len(df_cepac_remise))

    df_cepac_attente = df3[(df3["Type"] == "Débit")
                   & (df3["Moyen de paiement"] != "PAYPAL") &
                   (df3["Moyen de paiement"] != "AMEX") &
                   (df3["Info. compl."].str.contains('INT', na=False))]
    df_cepac_attente['Transaction'] = df_cepac_attente['Transaction'].astype(str)
    df_cepac_attente['Montant du paiement'] = df_cepac_attente['Montant du paiement'].astype(
        float)

    if(df_cepac_attente['Date du paiement'].dtypes=='datetime64[ns]'):
        df_cepac_attente['date'] = df_cepac_attente['Date du paiement'].dt.date
        df_cepac_attente['date'] = df_cepac_attente['date'].astype(str)
    else:
        df_cepac_attente['date'] = pd.to_datetime(df_cepac_attente['Date du paiement'],  format = '%d/%m/%Y %H:%M:%S')
        print("tpe:",df_cepac_attente['date'].dtypes)
    df_cepac_attente.reset_index(inplace=True)

    print("tpe:",df_cepac_remise['Date du paiement'].dtypes)
    print("tpe date:",df_cepac_remise['date'].dtypes)     
    print("number attente : ", len(df_cepac_remise))

    print(df_cepac_remise['Date du paiement'])
    print(df_cepac_remise['date'])
    
    stri=df_seaware['date'][0]

    print("-------------- date ---------------",stri)

    attenteRemise=df_cepac_remise[df_cepac_remise['date'].astype(str).str.contains(str(stri), na=False)]
    print(len(attenteRemise))

    attenteRemise_1 = df_cepac_remise[~df_cepac_remise['Transaction'].isin(attenteRemise["Transaction"].values)]
    attenteRemise_1.reset_index(drop=True, inplace=True)

    datetime_object = datetime.strptime(str(stri), '%Y-%m-%d')
    print(datetime_object)

    attenteRemiseJour=df_cepac_attente[(df_cepac_attente["date"]>=datetime(datetime_object.year,datetime_object.month,datetime_object.day,22,30,00)) & (df_cepac_attente["date"]<=datetime(datetime_object.year,datetime_object.month,datetime_object.day,23,59,59))]
    print("_________ dat________",len(attenteRemiseJour))


    totalRemise = round(df_cepac_remise["Montant du paiement"].sum(), 2)
    totalAttente = round(attenteRemise_1["Montant du paiement"].sum(), 2)
    total1 = round(totalRemise - totalAttente, 2)
    TotalAttenteJ = round(attenteRemiseJour["Montant du paiement"].sum(), 2)
    total = round(total1 + TotalAttenteJ, 2)

    data = "Calcul montant CEPAC => Total remisé du jour (", totalRemise, ") - En attente de remise J-1 (", totalAttente, ") = ",total1," + En attente de remise du jour (", TotalAttenteJ, ") // Total CEPAC du ",datetime_object.day,"/",datetime_object.month,"  = ", total, ""

    return data

def InternetPhrase(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        File2 = request.FILES["file2"]
        File3 = request.FILES["file3"]
        #annee = request.POST["annee"]

        df1 = pd.read_excel(File1)
        df2 = pd.read_excel(File2)
        df3 = pd.read_excel(File3)

        print("df1", df1)
        print("df2", df2)
        print("df3", df3)
        # Stats
        data = Internet_cc_phrase(df1, df2, df3)

        print('data : ', data)

    return HttpResponse(data, content_type="text/plain")



def Internet_files_Paypal_Debit(df1, df2):

    df_seaware = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") &
                     (df1['Utilisateur'].str.contains('BLO', na=False)) &
                     (df1['Commentaires'].str.contains('PPAL', na=False))]
    df_seaware['Transaction'] = df_seaware['Num. Trans.'].astype(str).str[2:]
    df_seaware['Montant init.'] = df_seaware['Montant init.'].astype(float)
    print("number seaware : ", len(df_seaware))

    df_cepac = df2[(df2["Type"] == "Débit")
                   & (df2["Moyen de paiement"] == "PAYPAL") &
                   (df2["Info. compl."].str.contains('INT', na=False))]
    df_cepac['Transaction'] = df_cepac['Transaction'].astype(str)
    df_cepac['Montant du paiement'] = df_cepac['Montant du paiement'].astype(
        float)
    print("number remisé : ", len(df_cepac))
    merged = pd.merge(df_cepac, df_seaware, on='Transaction')

    merged["MontantSeaware"] = merged['Montant init.']
    merged["MontantCepac"] = merged['Montant du paiement']
    merged["Ecart"] = merged["MontantCepac"] - merged["MontantSeaware"]
    ecart=merged[merged["Ecart"]!=0]
    print(len(ecart))
    
    return ecart

def InternetPaypalDebit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        File2 = request.FILES["file2"]
        File3 = request.FILES["file3"]
        #annee = request.POST["annee"]

        df1 = pd.read_excel(File1)
        df2 = pd.read_excel(File2)
        df3 = pd.read_excel(File3)

        print("df1", df1)
        print("df2", df2)
        print("df3", df3)
        # Stats
        data = Internet_files_Paypal_Debit(df1, df2)
        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))



def Internet_files_Paypal_Credit(df1, df2):

    df_seaware = df1[(df1["Type Trans."] == "REFUND") & (df1["Statut"] == "OK") &
                     (df1['Utilisateur'].str.contains('BLO', na=False)) &
                     (df1['Commentaires'].str.contains('PPAL', na=False))]
    df_seaware['Transaction'] = df_seaware['Num. Trans.'].astype(str).str[2:]
    df_seaware['Montant init.'] = df_seaware['Montant init.'].astype(float)
    print("number seaware : ", len(df_seaware))

    df_cepac = df2[(df2["Type"] == "Crédit")
                   & (df2["Moyen de paiement"] == "PAYPAL") &
                   (df2["Info. compl."].str.contains('INT', na=False))]
    df_cepac['Transaction'] = df_cepac['Transaction'].astype(str)
    df_cepac['Montant du paiement'] = df_cepac['Montant du paiement'].astype(
        float)
    print("number remisé : ", len(df_cepac))
    merged = pd.merge(df_cepac, df_seaware, on='Transaction')

    merged["MontantSeaware"] = merged['Montant init.']
    merged["MontantCepac"] = merged['Montant du paiement']
    merged["Ecart"] = merged["MontantCepac"] - merged["MontantSeaware"]
    ecart=merged[merged["Ecart"]!=0]
    print(len(ecart))
    
    return ecart

def InternetPaypalCredit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        File2 = request.FILES["file2"]
        File3 = request.FILES["file3"]
        #annee = request.POST["annee"]

        df1 = pd.read_excel(File1)
        df2 = pd.read_excel(File2)
        df3 = pd.read_excel(File3)

        print("df1", df1)
        print("df2", df2)
        print("df3", df3)
        # Stats
        data = Internet_files_Paypal_Credit(df1, df2)
        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))
