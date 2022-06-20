from datetime import datetime
import pandas as pd
from django.http import HttpResponse
from datetime import datetime


def Adv_debit(df1):

    df_seaware = df1[(df1["Type Trans."] == "PMNT") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") ]
    df_seaware['Transaction'] = df_seaware['Num. Trans.'].astype(str).str[2:]
    df_seaware['Montant init.'] = df_seaware['Montant init.'].astype(float)
    df_seaware['Montant']= df_seaware['Montant init.']
    df_seaware['Mode']= df_seaware['Mode pmt']
    df_seaware['Commande']= df_seaware['Num. Dest.']
    print("number seaware : ", len(df_seaware))

    
    print(len(df_seaware))
    
    return df_seaware

def AdvDebit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]

        df1 = pd.read_excel(File1)

        print("df1", df1)
        # Stats
        data = Adv_debit(df1)
        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))



def Adv_Credit(df1):

    df_seaware = df1[(df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANREFUND") ]
    df_seaware['Transaction'] = df_seaware['Num. Trans.'].astype(str).str[2:]
    df_seaware['Montant init.'] = df_seaware['Montant init.'].astype(float)
    df_seaware['Montant']= df_seaware['Montant init.']
    df_seaware['Mode']= df_seaware['Mode pmt']
    df_seaware['Commande']= df_seaware['Num. Dest.']
    print("number seaware : ", len(df_seaware))

    return df_seaware

def AdvCredit(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]

        df1 = pd.read_excel(File1)

        print("df1", df1)
        # Stats
        data = Adv_Credit(df1)
        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))


def Adv_phrase(df1):

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
    df_seaware['Montant']= df_seaware['Montant init.']
    df_seaware['Mode']= df_seaware['Mode pmt']
    df_seaware['Commande']= df_seaware['Num. Dest.']
    print("number seaware : ", len(df_seaware))
    print("date seaware : ", df_seaware['date'][0])
    
    
    
    return df_seaware

def AdvPhrase(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        #annee = request.POST["annee"]

        df1 = pd.read_excel(File1)

        print("df1", df1)
        # Stats
        data = Adv_phrase(df1)

        print('data : ', data)

    return HttpResponse(data, content_type="text/plain")
