from datetime import datetime
import email
import pandas as pd
from django.http import HttpResponse
from datetime import datetime


def Journal_Debit_Oui(df1,df2,df3,df4):

    Remboursement_ADMV = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") 
                      & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") &
                     ((df1['Office Location'].str.contains('SAV', na=False)) | (df1['Office Location'].str.contains('ADV', na=False)))]
    RA = Remboursement_ADMV["Montant init."].sum()

    Remboursement_INTERNET = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (~df1['Commentaires'].str.contains('AMEX', na=False)) &
                        (~df1['Commentaires'].str.contains('PPAL', na=False))]
    RI = Remboursement_INTERNET["Montant init."].sum()

    Remboursement_INTERNET_PAYPAL = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('PPAL', na=False))]
    RIP = Remboursement_INTERNET_PAYPAL["Montant init."].sum()

    Remboursement_INTERNET_Amex = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('AMEX', na=False))]
    RIA = Remboursement_INTERNET_Amex["Montant init."].sum()

    Remboursement_VAD_AMEX_rem = df3[(df3["Type"] == "Crédit") & (df3["Moyen de paiement"] == "AMEX") & (~df3["Info. compl."].str.contains('INT', na=False))]
    print(len(Remboursement_VAD_AMEX_rem))
    Remboursement_VAD_AMEX_rem['Transaction'] = Remboursement_VAD_AMEX_rem['Transaction'].astype('string')
    
    Remboursement_VAD_AMEX_sw = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Ent. Dest."] != "AGEN")  & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") & (df1['Office Location'].str.contains('CVD', na=False))]
    print(len(Remboursement_VAD_AMEX_sw))
    Remboursement_VAD_AMEX_sw['Id. Externe'] = Remboursement_VAD_AMEX_sw['Id. Externe'].astype('string')
    RV=Remboursement_VAD_AMEX_sw["Montant init."].sum()
    
    Remboursement_VAD_AMEX=Remboursement_VAD_AMEX_rem[Remboursement_VAD_AMEX_rem['Transaction'].isin(Remboursement_VAD_AMEX_sw["Id. Externe"].values)]
    print(len(Remboursement_VAD_AMEX))
    RVA=Remboursement_VAD_AMEX["Montant du paiement"].sum()

    Emission_VAD_AMEX_rem = df3[(df3["Type"] == "Débit") & (df3["Moyen de paiement"] == "AMEX") & (~df3["Info. compl."].str.contains('INT', na=False))]
    print(len(Emission_VAD_AMEX_rem))
    Emission_VAD_AMEX_rem['Transaction'] = Emission_VAD_AMEX_rem['Transaction'].astype('string')
    
    Emission_VAD_AMEX_sw = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") & (df1['Office Location'].str.contains('CVD', na=False))]
    print(len(Emission_VAD_AMEX_sw))
    Emission_VAD_AMEX_sw['Id. Externe'] = Emission_VAD_AMEX_sw['Id. Externe'].astype('string')
    EV=Emission_VAD_AMEX_sw["Montant init."].sum()
    
    Emission_VAD_AMEX=Emission_VAD_AMEX_rem[Emission_VAD_AMEX_rem['Transaction'].isin(Emission_VAD_AMEX_sw["Id. Externe"].values)]
    print(len(Emission_VAD_AMEX))
    EVA=Emission_VAD_AMEX["Montant du paiement"].sum()

    Marie_Do = df4[(df4["IS_VALID"]=="Y")]
    MD=Marie_Do["DON_AMOUNT"].sum()

    # encaiss cb ppal
    Emission_INTERNET_PAYPAL = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('PPAL', na=False))]
    Emission_INTERNET_PAYPAL['Id. Externe'] = Emission_INTERNET_PAYPAL['Id. Externe'].astype('string')
    print("ppal sw",len(Emission_INTERNET_PAYPAL))
    ppal_remis=df2[(df2["Type"] == "Débit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Moyen de paiement"] == "PAYPAL") & (df2["Info. compl."].str.contains('INT', na=False))]
    ppal_remis['Transaction'] = ppal_remis['Transaction'].astype('string')
    print("ppal_remis",len(ppal_remis))
    existppal=ppal_remis[ppal_remis['Transaction'].isin(Emission_INTERNET_PAYPAL["Id. Externe"].values)]
    print("existppal",len(existppal))
    ppal_total = existppal["Montant du paiement"].sum()

    Emission_INTERNET_Amex = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('AMEX', na=False))]
    EIA = Emission_INTERNET_Amex["Montant init."].sum()

    # Débit
    Cheque=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CHK")]
    C = Cheque["Montant init."].sum()

    Cheque_vacance=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CV")]
    CV = Cheque_vacance["Montant init."].sum()

    avoir_client=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & ((df1["Mode pmt"] == "AVOIR CLIENT") | (df1["Mode pmt"] == "AVOIRCLIENT"))]
    AC = avoir_client["Montant init."].sum()

    coupon=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CPN")]
    CPN = coupon["Montant init."].sum()

    WriteOFF=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "WRITEOFF")]
    WOFF = WriteOFF["Montant init."].sum()

    result=phrase(df1,df2,df3)
    Emission_ADMV = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") &
                     ((df1['Office Location'].str.contains('SAV', na=False)) | (df1['Office Location'].str.contains('ADV', na=False)))]
    EA = Emission_ADMV["Montant init."].sum()

    cvd=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "B2C TPEV")
                    & (df1['Office Location'].str.contains('CVD', na=False))]
    cvd['Id. Externe'] = cvd['Id. Externe'].astype('string')
    cvd['Num. Dest.'] = cvd['Num. Dest.'].astype('string')
    print("cvd",len(cvd))
    cvd_remis=df2[(df2["Type"] == "Débit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Moyen de paiement"] != "PAYPAL") & (~df2["Info. compl."].str.contains('INT', na=False))]
    cvd_remis['Transaction'] = cvd_remis['Transaction'].astype('string')
    cvd_remis['Commande'] = cvd_remis['Commande'].astype('string')
    print("cvd_remis",len(cvd_remis))
    exist=cvd_remis[cvd_remis['Transaction'].isin(cvd["Id. Externe"].values)]
    print("exist",len(exist))
    df1_2=cvd[~cvd['Id. Externe'].isin(exist["Transaction"].values)]
    exist2=cvd_remis[cvd_remis['Commande'].isin(df1_2["Num. Dest."].values)]
    print("exist2",len(exist2))
    cvd_total = exist["Montant du paiement"].sum()+exist2["Montant du paiement"].sum()
    print("cvd",round(cvd_total,2))

    adv= df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") &
                     (df1['Office Location'].str.contains('ADV', na=False)) & (df1["Mode pmt"] == "B2C TPEV")]
    adv_remis=df2[(df2["Type"] == "Débit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Moyen de paiement"] != "PAYPAL")]
    adv_remis['Transaction'] = adv_remis['Transaction'].astype('string')
    adv_remis['Commande'] = adv_remis['Commande'].astype('string')
    print("adv_remis",len(adv_remis))
    exist_adv=adv_remis[adv_remis['Transaction'].isin(adv["Id. Externe"].values)]
    print("exist",len(exist_adv))
    adv_total = exist_adv["Montant du paiement"].sum()

    sav= df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") &
                     (df1['Office Location'].str.contains('SAV', na=False)) & (df1["Mode pmt"] == "CC")]
    sav_remis=df2[(df2["Type"] == "Débit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Moyen de paiement"] != "PAYPAL")]
    sav_remis['Transaction'] = sav_remis['Transaction'].astype('string')
    sav_remis['Commande'] = sav_remis['Commande'].astype('string')
    print("sav_remis",len(sav_remis))
    exist_sav=sav_remis[sav_remis['Transaction'].isin(sav["Id. Externe"].values)]
    print("exist",len(exist_sav))
    sav_total = exist_sav["Montant du paiement"].sum()



    debit=pd.DataFrame(columns=['Comptes', 'Gestions', 'Libelles', 'NB', 'Montants'])
    debit = debit.append({'Comptes': "Débit", 'Gestions': "", 'Libelles': '','NB':"", 'Montants':""}, ignore_index=True)
    debit = debit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Remboursement ADMV','NB':len(Remboursement_ADMV), 'Montants':round(RA,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Remboursement Internet','NB':len(Remboursement_INTERNET), 'Montants':round(RI,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Remboursement Internet PAYPAL','NB':len(Remboursement_INTERNET_PAYPAL), 'Montants':round(RIP,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Remboursement Internet AMEX','NB':len(Remboursement_INTERNET_Amex), 'Montants':round(RIA,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Remboursement VAD','NB':len(Remboursement_VAD_AMEX_sw)-len(Remboursement_VAD_AMEX), 'Montants':round(RV,2)-round(RVA,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Remboursement VAD AMEX','NB':len(Remboursement_VAD_AMEX), 'Montants':round(RVA,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "", 'Gestions': "", 'Libelles': '','NB':'', 'Montants':''}, ignore_index=True)
    debit = debit.append({'Comptes': "", 'Gestions': "", 'Libelles': '','NB':'', 'Montants':''}, ignore_index=True)
    debit = debit.append({'Comptes': "5812500", 'Gestions': "", 'Libelles': 'Versement CP chèque','NB':len(Cheque), 'Montants':round(C,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "5116000", 'Gestions': "", 'Libelles': 'Versement CP chèque vacances','NB':len(Cheque_vacance), 'Montants':round(CV,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "5113160", 'Gestions': "", 'Libelles': 'Encaissement CB CEPAC','NB':result[1]+len(exist)+len(exist2)+len(exist_sav)+len(exist_adv), 'Montants':result[0]+round(cvd_total,2)+round(sav_total,2)+round(adv_total,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "5113200", 'Gestions': "", 'Libelles': 'Encaissement  CB CEPAC AMEX','NB':len(Emission_VAD_AMEX)+len(Emission_INTERNET_Amex), 'Montants':round(EIA,2)+round(EVA,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "5113300", 'Gestions': "", 'Libelles': 'Encaissement CB PAYPAL','NB':len(existppal), 'Montants':round(ppal_total,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "5113140", 'Gestions': "", 'Libelles': 'Encaissement CB par TPE','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "5113190", 'Gestions': "", 'Libelles': 'Encaissement CEPAC par B to B','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "5116100", 'Gestions': "", 'Libelles': 'Encaissement par E.Chèque Vacances','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "5115000", 'Gestions': "", 'Libelles': 'P-cash','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Avoir Client','NB':len(avoir_client), 'Montants':round(AC,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4712100", 'Gestions': "", 'Libelles': 'Virement reçu','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "1812100", 'Gestions': "", 'Libelles': 'Avis comptable AJA','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "1813100", 'Gestions': "", 'Libelles': 'Avis comptable BIA','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "", 'Gestions': "", 'Libelles': 'Paiement Pe-cash','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "4786010", 'Gestions': "", 'Libelles': 'Coupons (encaissement dossier par)','NB':len(coupon), 'Montants':round(CPN,2)}, ignore_index=True)    
    debit = debit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': "Réquisition",'NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "7580000", 'Gestions': "BOF01", 'Libelles': 'Paiement par client bank < 5€','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "6580000", 'Gestions': "BOF01", 'Libelles': 'Write off (Ecart sur réservation non soldée < 5 euros)','NB':len(WriteOFF), 'Montants':round(WOFF,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4670160", 'Gestions': "", 'Libelles': 'Déficit de caisse','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "4670160", 'Gestions': "", 'Libelles': 'Régularisation Excédent caisse','NB':0, 'Montants':0}, ignore_index=True)
    total=round(RA,2)+round(RI,2)+round(RIP,2)+round(RIA,2)+(round(RV,2)-round(RVA,2))+round(RVA,2)+round(C,2)+round(CV,2)+result[0]+round(cvd_total,2)+round(EIA,2)+round(EVA,2)+round(ppal_total,2)+0+0+0+0+0+round(AC,2)+0+0+0+0+round(CPN,2)+0+0+round(WOFF,2)+0+0
    debit = debit.append({'Comptes': "", 'Gestions': "", 'Libelles': 'TOTAL','NB':'', 'Montants':round(total,2)}, ignore_index=True)

    return debit

def Journal_Debit_Non(df1,df2,df3,df4):

    Remboursement_ADMV = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") 
                      & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") &
                     ((df1['Office Location'].str.contains('SAV', na=False)) | (df1['Office Location'].str.contains('ADV', na=False)))]
    RA = Remboursement_ADMV["Montant init."].sum()

    Remboursement_INTERNET = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (~df1['Commentaires'].str.contains('AMEX', na=False)) &
                        (~df1['Commentaires'].str.contains('PPAL', na=False))]
    RI = Remboursement_INTERNET["Montant init."].sum()

    Remboursement_INTERNET_PAYPAL = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('PPAL', na=False))]
    RIP = Remboursement_INTERNET_PAYPAL["Montant init."].sum()

    Remboursement_INTERNET_Amex = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('AMEX', na=False))]
    RIA = Remboursement_INTERNET_Amex["Montant init."].sum()

    Remboursement_VAD_AMEX_rem = df2[(df2["Type"] == "Crédit") & (df2["Moyen de paiement"] == "AMEX") & (~df2["Info. compl."].str.contains('INT', na=False))]
    print(len(Remboursement_VAD_AMEX_rem))
    Remboursement_VAD_AMEX_rem['Transaction'] = Remboursement_VAD_AMEX_rem['Transaction'].astype('string')
    
    Remboursement_VAD_AMEX_sw = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Ent. Dest."] != "AGEN")  & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") & (df1['Office Location'].str.contains('CVD', na=False))]
    print(len(Remboursement_VAD_AMEX_sw))
    Remboursement_VAD_AMEX_sw['Id. Externe'] = Remboursement_VAD_AMEX_sw['Id. Externe'].astype('string')
    RV=Remboursement_VAD_AMEX_sw["Montant init."].sum()
    
    Remboursement_VAD_AMEX=Remboursement_VAD_AMEX_rem[Remboursement_VAD_AMEX_rem['Transaction'].isin(Remboursement_VAD_AMEX_sw["Id. Externe"].values)]
    print(len(Remboursement_VAD_AMEX))
    RVA=Remboursement_VAD_AMEX["Montant du paiement"].sum()

    Emission_VAD_AMEX_rem = df2[(df2["Type"] == "Débit") & (df2["Moyen de paiement"] == "AMEX") & (~df2["Info. compl."].str.contains('INT', na=False))]
    print(len(Emission_VAD_AMEX_rem))
    Emission_VAD_AMEX_rem['Transaction'] = Emission_VAD_AMEX_rem['Transaction'].astype('string')
    
    Emission_VAD_AMEX_sw = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") & (df1['Office Location'].str.contains('CVD', na=False))]
    print(len(Emission_VAD_AMEX_sw))
    Emission_VAD_AMEX_sw['Id. Externe'] = Emission_VAD_AMEX_sw['Id. Externe'].astype('string')
    EV=Emission_VAD_AMEX_sw["Montant init."].sum()
    
    Emission_VAD_AMEX=Emission_VAD_AMEX_rem[Emission_VAD_AMEX_rem['Transaction'].isin(Emission_VAD_AMEX_sw["Id. Externe"].values)]
    print(len(Emission_VAD_AMEX))
    EVA=Emission_VAD_AMEX["Montant du paiement"].sum()

    Marie_Do = df4[(df4["IS_VALID"]=="Y")]
    MD=Marie_Do["DON_AMOUNT"].sum()

    # encaiss cb ppal
    Emission_INTERNET_PAYPAL = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('PPAL', na=False))]
    Emission_INTERNET_PAYPAL['Id. Externe'] = Emission_INTERNET_PAYPAL['Id. Externe'].astype('string')
    print("ppal sw",len(Emission_INTERNET_PAYPAL))
    ppal_remis=df2[(df2["Type"] == "Débit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Moyen de paiement"] == "PAYPAL") & (df2["Info. compl."].str.contains('INT', na=False))]
    ppal_remis['Transaction'] = ppal_remis['Transaction'].astype('string')
    print("ppal_remis",len(ppal_remis))
    existppal=ppal_remis[ppal_remis['Transaction'].isin(Emission_INTERNET_PAYPAL["Id. Externe"].values)]
    print("existppal",len(existppal))
    ppal_total = existppal["Montant du paiement"].sum()

    Emission_INTERNET_Amex = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('AMEX', na=False))]
    EIA = Emission_INTERNET_Amex["Montant init."].sum()

    # Débit
    Cheque=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CHK")]
    C = Cheque["Montant init."].sum()

    Cheque_vacance=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CV")]
    CV = Cheque_vacance["Montant init."].sum()

    avoir_client=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & ((df1["Mode pmt"] == "AVOIR CLIENT") | (df1["Mode pmt"] == "AVOIRCLIENT"))]
    AC = avoir_client["Montant init."].sum()

    coupon=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CPN")]
    CPN = coupon["Montant init."].sum()

    WriteOFF=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "WRITEOFF")]
    WOFF = WriteOFF["Montant init."].sum()

    result=phrase(df1,df2,df3)
    Emission_ADMV = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") &
                     ((df1['Office Location'].str.contains('SAV', na=False)) | (df1['Office Location'].str.contains('ADV', na=False)))]
    EA = Emission_ADMV["Montant init."].sum()

    cvd=df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "B2C TPEV")
                    & (df1['Office Location'].str.contains('CVD', na=False))]
    cvd['Id. Externe'] = cvd['Id. Externe'].astype('string')
    cvd['Num. Dest.'] = cvd['Num. Dest.'].astype('string')
    print("cvd",len(cvd))
    cvd_remis=df2[(df2["Type"] == "Débit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Moyen de paiement"] != "PAYPAL") & (~df2["Info. compl."].str.contains('INT', na=False))]
    cvd_remis['Transaction'] = cvd_remis['Transaction'].astype('string')
    cvd_remis['Commande'] = cvd_remis['Commande'].astype('string')
    print("cvd_remis",len(cvd_remis))
    exist=cvd_remis[cvd_remis['Transaction'].isin(cvd["Id. Externe"].values)]
    print("exist",len(exist))
    df1_2=cvd[~cvd['Id. Externe'].isin(exist["Transaction"].values)]
    exist2=cvd_remis[cvd_remis['Commande'].isin(df1_2["Num. Dest."].values)]
    print("exist2",len(exist2))
    cvd_total = exist["Montant du paiement"].sum()+exist2["Montant du paiement"].sum()
    print("cvd",round(cvd_total,2))

    adv= df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") &
                     (df1['Office Location'].str.contains('ADV', na=False)) & (df1["Mode pmt"] == "B2C TPEV")]
    adv_remis=df2[(df2["Type"] == "Débit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Moyen de paiement"] != "PAYPAL")]
    adv_remis['Transaction'] = adv_remis['Transaction'].astype('string')
    adv_remis['Commande'] = adv_remis['Commande'].astype('string')
    print("adv_remis",len(adv_remis))
    exist_adv=adv_remis[adv_remis['Transaction'].isin(adv["Id. Externe"].values)]
    print("exist",len(exist_adv))
    adv_total = exist_adv["Montant du paiement"].sum()

    sav= df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") &
                     (df1['Office Location'].str.contains('SAV', na=False)) & (df1["Mode pmt"] == "CC")]
    sav_remis=df2[(df2["Type"] == "Débit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Moyen de paiement"] != "PAYPAL")]
    sav_remis['Transaction'] = sav_remis['Transaction'].astype('string')
    sav_remis['Commande'] = sav_remis['Commande'].astype('string')
    print("sav_remis",len(sav_remis))
    exist_sav=sav_remis[sav_remis['Transaction'].isin(sav["Id. Externe"].values)]
    print("exist",len(exist_sav))
    sav_total = exist_sav["Montant du paiement"].sum()



    debit=pd.DataFrame(columns=['Comptes', 'Gestions', 'Libelles', 'NB', 'Montants'])
    debit = debit.append({'Comptes': "Débit", 'Gestions': "", 'Libelles': '','NB':"", 'Montants':""}, ignore_index=True)
    debit = debit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Remboursement ADMV','NB':len(Remboursement_ADMV), 'Montants':round(RA,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Remboursement Internet','NB':len(Remboursement_INTERNET), 'Montants':round(RI,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Remboursement Internet PAYPAL','NB':len(Remboursement_INTERNET_PAYPAL), 'Montants':round(RIP,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Remboursement Internet AMEX','NB':len(Remboursement_INTERNET_Amex), 'Montants':round(RIA,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Remboursement VAD','NB':len(Remboursement_VAD_AMEX_sw)-len(Remboursement_VAD_AMEX), 'Montants':round(RV,2)-round(RVA,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Remboursement VAD AMEX','NB':len(Remboursement_VAD_AMEX), 'Montants':round(RVA,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "", 'Gestions': "", 'Libelles': '','NB':'', 'Montants':''}, ignore_index=True)
    debit = debit.append({'Comptes': "", 'Gestions': "", 'Libelles': '','NB':'', 'Montants':''}, ignore_index=True)
    debit = debit.append({'Comptes': "5812500", 'Gestions': "", 'Libelles': 'Versement CP chèque','NB':len(Cheque), 'Montants':round(C,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "5116000", 'Gestions': "", 'Libelles': 'Versement CP chèque vacances','NB':len(Cheque_vacance), 'Montants':round(CV,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "5113160", 'Gestions': "", 'Libelles': 'Encaissement CB CEPAC','NB':result[1]+len(exist)+len(exist2)+len(exist_sav)+len(exist_adv), 'Montants':result[0]+round(cvd_total,2)+round(sav_total,2)+round(adv_total,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "5113200", 'Gestions': "", 'Libelles': 'Encaissement  CB CEPAC AMEX','NB':len(Emission_VAD_AMEX)+len(Emission_INTERNET_Amex), 'Montants':round(EIA,2)+round(EVA,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "5113300", 'Gestions': "", 'Libelles': 'Encaissement CB PAYPAL','NB':len(existppal), 'Montants':round(ppal_total,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "5113140", 'Gestions': "", 'Libelles': 'Encaissement CB par TPE','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "5113190", 'Gestions': "", 'Libelles': 'Encaissement CEPAC par B to B','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "5116100", 'Gestions': "", 'Libelles': 'Encaissement par E.Chèque Vacances','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "5115000", 'Gestions': "", 'Libelles': 'P-cash','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Avoir Client','NB':len(avoir_client), 'Montants':round(AC,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4712100", 'Gestions': "", 'Libelles': 'Virement reçu','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "1812100", 'Gestions': "", 'Libelles': 'Avis comptable AJA','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "1813100", 'Gestions': "", 'Libelles': 'Avis comptable BIA','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "", 'Gestions': "", 'Libelles': 'Paiement Pe-cash','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "4786010", 'Gestions': "", 'Libelles': 'Coupons (encaissement dossier par)','NB':len(coupon), 'Montants':round(CPN,2)}, ignore_index=True)    
    debit = debit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': "Réquisition",'NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "7580000", 'Gestions': "BOF01", 'Libelles': 'Paiement par client bank < 5€','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "6580000", 'Gestions': "BOF01", 'Libelles': 'Write off (Ecart sur réservation non soldée < 5 euros)','NB':len(WriteOFF), 'Montants':round(WOFF,2)}, ignore_index=True)
    debit = debit.append({'Comptes': "4670160", 'Gestions': "", 'Libelles': 'Déficit de caisse','NB':0, 'Montants':0}, ignore_index=True)
    debit = debit.append({'Comptes': "4670160", 'Gestions': "", 'Libelles': 'Régularisation Excédent caisse','NB':0, 'Montants':0}, ignore_index=True)
    total=round(RA,2)+round(RI,2)+round(RIP,2)+round(RIA,2)+(round(RV,2)-round(RVA,2))+round(RVA,2)+round(C,2)+round(CV,2)+result[0]+round(cvd_total,2)+round(EIA,2)+round(EVA,2)+round(ppal_total,2)+0+0+0+0+0+round(AC,2)+0+0+0+0+round(CPN,2)+0+0+round(WOFF,2)+0+0
    debit = debit.append({'Comptes': "", 'Gestions': "", 'Libelles': 'TOTAL','NB':'', 'Montants':round(total,2)}, ignore_index=True)

    return debit

def debitOui(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        File2 = request.FILES["file2"]
        File3 = request.FILES["file3"]
        File4 = request.FILES["file4"]
        File5 = request.FILES["file5"]
        File6 = request.FILES["file6"]
        File7 = request.FILES["file7"]
        #annee = request.POST["annee"]
        
        internet = pd.read_excel(File1)
        adv = pd.read_excel(File2)
        sav = pd.read_excel(File3)
        cvd = pd.read_excel(File4)

        df2 = pd.read_excel(File5)
        df3 = pd.read_excel(File6)
        df4 = pd.read_excel(File7)

        seaware=pd.concat([internet,adv,sav,cvd])
        seaware.reset_index(inplace=True,drop=True)

        df1 = seaware.drop_duplicates(subset=['Num. Trans.'], keep='last')
        df1.reset_index(inplace=True,drop=True)
        print(len(df1))

        # Journal
        data = Journal_Debit_Oui(df1, df2, df3,df4)

        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))

def debitNon(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        File2 = request.FILES["file2"]
        File3 = request.FILES["file3"]
        File4 = request.FILES["file4"]
        File5 = request.FILES["file5"]
        File6 = request.FILES["file6"]
        File7 = request.FILES["file7"]
        #annee = request.POST["annee"]
        
        internet = pd.read_excel(File1)
        adv = pd.read_excel(File2)
        sav = pd.read_excel(File3)
        cvd = pd.read_excel(File4)

        df2 = pd.read_excel(File5)
        df3 = pd.read_excel(File6)
        df4 = pd.read_excel(File7)

        seaware=pd.concat([internet,adv,sav,cvd])
        seaware.reset_index(inplace=True,drop=True)

        df1 = seaware.drop_duplicates(subset=['Num. Trans.'], keep='last')
        df1.reset_index(inplace=True,drop=True)
        print(len(df1))

        # Journal
        data = Journal_Debit_Non(df1, df2, df3,df4)

        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))

def Journal_Credit_Oui(df1,df2,df3,df4):

    Emission_ADMV = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") &
                     ((df1['Office Location'].str.contains('SAV', na=False)) | (df1['Office Location'].str.contains('ADV', na=False)))]
    EA = Emission_ADMV["Montant init."].sum()

    Emission_INTERNET = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (~df1['Commentaires'].str.contains('AMEX', na=False)) &
                        (~df1['Commentaires'].str.contains('PPAL', na=False))]
    EI = Emission_INTERNET["Montant init."].sum()

    Emission_INTERNET_PAYPAL = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('PPAL', na=False))]
    EIP = Emission_INTERNET_PAYPAL["Montant init."].sum()

    Emission_INTERNET_Amex = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('AMEX', na=False))]
    EIA = Emission_INTERNET_Amex["Montant init."].sum()

    Emission_VAD_AMEX_rem = df3[(df3["Type"] == "Débit") & (df3["Moyen de paiement"] == "AMEX") & (~df3["Info. compl."].str.contains('INT', na=False))]
    print(len(Emission_VAD_AMEX_rem))
    Emission_VAD_AMEX_rem['Transaction'] = Emission_VAD_AMEX_rem['Transaction'].astype('string')
    
    Emission_VAD_AMEX_sw = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") & (df1['Office Location'].str.contains('CVD', na=False))]
    print(len(Emission_VAD_AMEX_sw))
    Emission_VAD_AMEX_sw['Id. Externe'] = Emission_VAD_AMEX_sw['Id. Externe'].astype('string')
    EV=Emission_VAD_AMEX_sw["Montant init."].sum()
    
    Emission_VAD_AMEX=Emission_VAD_AMEX_rem[Emission_VAD_AMEX_rem['Transaction'].isin(Emission_VAD_AMEX_sw["Id. Externe"].values)]
    print(len(Emission_VAD_AMEX))
    EVA=Emission_VAD_AMEX["Montant du paiement"].sum()

    Marie_Do = df4[(df4["IS_VALID"]=="Y")]
    MD=Marie_Do["DON_AMOUNT"].sum()

    Remboursement_VAD_AMEX_rem = df3[(df3["Type"] == "Crédit") & (df3["Moyen de paiement"] == "AMEX") & (~df3["Info. compl."].str.contains('INT', na=False))]
    print(len(Remboursement_VAD_AMEX_rem))
    Remboursement_VAD_AMEX_rem['Transaction'] = Remboursement_VAD_AMEX_rem['Transaction'].astype('string')
    
    Remboursement_VAD_AMEX_sw = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Ent. Dest."] != "AGEN")  & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") & (df1['Office Location'].str.contains('CVD', na=False))]
    print(len(Remboursement_VAD_AMEX_sw))
    Remboursement_VAD_AMEX_sw['Id. Externe'] = Remboursement_VAD_AMEX_sw['Id. Externe'].astype('string')
    RV=Remboursement_VAD_AMEX_sw["Montant init."].sum()
    
    Remboursement_VAD_AMEX=Remboursement_VAD_AMEX_rem[Remboursement_VAD_AMEX_rem['Transaction'].isin(Remboursement_VAD_AMEX_sw["Id. Externe"].values)]
    print(len(Remboursement_VAD_AMEX))
    RVA=Remboursement_VAD_AMEX["Montant du paiement"].sum()

    Remboursement_INTERNET_Amex = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('AMEX', na=False))]
    RIA = Remboursement_INTERNET_Amex["Montant init."].sum()

    Remboursement_Remise_Amex = df2[(df2["Type"] == "Crédit") & (df2["Moyen de paiement"] == "AMEX") ]
    RRA = Remboursement_Remise_Amex["Montant du paiement"].sum()
    
    # Credit
    Cheque_emettre=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CHK")]
    CE = Cheque_emettre["Montant init."].sum()

    Virement_emettre=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "VIREMENT")]
    VE = Virement_emettre["Montant init."].sum()

    avoir_client=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & ((df1["Mode pmt"] == "AVOIR CLIENT") | (df1["Mode pmt"] == "AVOIRCLIENT"))]
    AC = avoir_client["Montant init."].sum()

    coupon=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CPN")]
    CPN = coupon["Montant init."].sum()

    fraude=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "NON REMBOURSE")]
    FR = fraude["Montant init."].sum()

    WriteOFF=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "WRITEOFF")]
    WOFF = WriteOFF["Montant init."].sum()

    # B to C
    df2['Commande'].replace(regex=True, inplace=True, to_replace=r'[^0-9.\-]', value=r'')
    cvd=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") 
                    & (df1['Office Location'].str.contains('CVD', na=False))]
    cvd['Num. Orig.'] = cvd['Num. Orig.'].astype('string')
    print("cvd",len(cvd))
    
    cvd_remis=df2[(df2["Type"] == "Crédit") & (df2["Moyen de paiement"] != "AMEX") ]
    cvd_remis['Commande'] = cvd_remis['Commande'].astype('string')
    print("cvd_remis",len(cvd_remis))
    exist=cvd_remis[cvd_remis['Commande'].isin(cvd["Num. Orig."].values)]
    print("exist",len(exist))
    cvd_total = exist["Montant du paiement"].sum()
    print("total cvd",cvd_total)

    remb_Sav_Adv = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") 
                      & ((df1["Mode pmt"] == "CC") | ((df1["Mode pmt"] == "CC TPE"))) & ((df1['Office Location'].str.contains('SAV', na=False)) | (df1['Office Location'].str.contains('ADV', na=False)))]
    Rsa = remb_Sav_Adv["Montant init."].sum()
    print("-------SAV + ADV---------", Rsa)
    print(len(remb_Sav_Adv))

    Remboursement_ADMV = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") 
                      & (df1["Mode pmt"] == "CC") & (df1['Utilisateur'].str.contains('BLO', na=False)) & (~df1['Office Location'].str.contains('SAV', na=False)) & 
                      (~df1['Office Location'].str.contains('ADV', na=False)) & (~df1['Office Location'].str.contains('CVD', na=False))]
    Remboursement_ADMV['Num. Orig.'] = Remboursement_ADMV['Num. Orig.'].astype('string')
    RA_internet = Remboursement_ADMV["Montant init."].sum()
    internet_remise = df2[(df2["Type"] == "Crédit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Info. compl."].str.contains('INT', na=False))]
    internet_remise['Commande'] = internet_remise['Commande'].astype('string')
    exist_B_to_C=internet_remise[internet_remise['Commande'].isin(Remboursement_ADMV["Num. Orig."].values)]
    B_to_C = exist_B_to_C["Montant du paiement"].sum()
    print("---------internet-------", B_to_C)
    print("exist B to C",len(exist_B_to_C))

    #payal
    # remboursement cb ppal
    Remboursement_INTERNET_PAYPAL = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('PPAL', na=False))]
    Remboursement_INTERNET_PAYPAL['Id. Externe'] = Remboursement_INTERNET_PAYPAL['Id. Externe'].astype('string')
    print("ppal sw",len(Remboursement_INTERNET_PAYPAL))
    ppal_remis=df2[(df2["Type"] == "Crédit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Moyen de paiement"] == "PAYPAL") & (df2["Info. compl."].str.contains('INT', na=False))]
    ppal_remis['Transaction'] = ppal_remis['Transaction'].astype('string')
    print("ppal_remis",len(ppal_remis))
    existppal=ppal_remis[ppal_remis['Transaction'].isin(Remboursement_INTERNET_PAYPAL["Id. Externe"].values)]
    print("existppal",len(existppal))
    ppal_total = existppal["Montant du paiement"].sum()

    credit=pd.DataFrame(columns=['Comptes', 'Gestions', 'Libelles', 'NB', 'Montants'])
    credit = credit.append({'Comptes': "Crédit", 'Gestions': "", 'Libelles': '','NB':"", 'Montants':""}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Emission ADMV','NB':len(Emission_ADMV), 'Montants':round(EA,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Emission Internet','NB':len(Emission_INTERNET), 'Montants':round(EI,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Emission Internet PAYPAL','NB':len(Emission_INTERNET_PAYPAL), 'Montants':round(EIP,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Emission Internet AMEX','NB':len(Emission_INTERNET_Amex), 'Montants':round(EIA,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Emission VAD','NB':len(Emission_VAD_AMEX_sw)-len(Emission_VAD_AMEX), 'Montants':round(EV,2)-round(EVA,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Emission VAD AMEX','NB':len(Emission_VAD_AMEX), 'Montants':round(EVA,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4670800", 'Gestions': "", 'Libelles': 'Don La Marie Do','NB':len(Marie_Do), 'Montants':round(MD,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "", 'Gestions': "", 'Libelles': '','NB':'', 'Montants':''}, ignore_index=True)
    credit = credit.append({'Comptes': "4673410", 'Gestions': "", 'Libelles': 'Chèque à émettre','NB':len(Cheque_emettre), 'Montants':round(CE,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4673420", 'Gestions': "", 'Libelles': 'Virement à émettre','NB':len(Virement_emettre), 'Montants':round(VE,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "5113160", 'Gestions': "", 'Libelles': 'Remboursement CEPAC B to C','NB':len(exist)+len(remb_Sav_Adv)+len(exist_B_to_C), 'Montants':round(cvd_total,2)+round(Rsa,2)+round(B_to_C,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "5113200", 'Gestions': "", 'Libelles': 'Remboursement CEPAC AMEX','NB':len(Remboursement_Remise_Amex)+len(Remboursement_INTERNET_Amex)+len(Remboursement_VAD_AMEX), 'Montants':round(RRA,2)+round(RIA,2)+round(RVA,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "5113300", 'Gestions': "", 'Libelles': 'Remboursement CEPAC PAYPAL','NB':len(existppal), 'Montants':round(ppal_total,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "5113140", 'Gestions': "", 'Libelles': 'Remboursement TPE','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "5113190", 'Gestions': "", 'Libelles': 'Remboursement CEPAC B to B','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "", 'Gestions': "", 'Libelles': '','NB':'', 'Montants':''}, ignore_index=True)
    credit = credit.append({'Comptes': "4786010", 'Gestions': "", 'Libelles': 'Coupons (annulation/rembst)','NB':len(coupon), 'Montants':round(CPN,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Remboursement réquisitions','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "5113160", 'Gestions': "", 'Libelles': 'Annulation CB declarée en TO CAPTURE en J','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "4787400", 'Gestions': "", 'Libelles': 'Remboursement divers','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "1812100", 'Gestions': "", 'Libelles': 'Avis comptable AJA','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "1813100", 'Gestions': "", 'Libelles': 'Avis comptable BIA','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "4673710", 'Gestions': "", 'Libelles': 'CB Impayées à régulariser','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': "Fraude CB- Régul d'impayé",'NB':len(fraude), 'Montants':round(FR,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Avoir Client','NB':len(avoir_client), 'Montants':round(AC,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "7580000", 'Gestions': "BOF01", 'Libelles': 'Trop perçu < 5 euros / Chèque vacances non remboursés','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "7580000", 'Gestions': "BOF01", 'Libelles': 'Trop perçu/résa, transfert vers client bank (<5€)','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "6580000", 'Gestions': "BOF01", 'Libelles': 'Write off  non remboursable (<5€)','NB':len(WriteOFF), 'Montants':round(WOFF,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4670160", 'Gestions': "", 'Libelles': 'Excédent de caisse','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "4670160", 'Gestions': "", 'Libelles': 'Régularisation Déficit de caisse','NB':0, 'Montants':0}, ignore_index=True)
    total=round(EA,2)+round(EI,2)+round(EIP,2)+round(EIA,2)+(round(EV,2)-round(EVA,2))+round(EVA,2)+round(MD,2)+round(CE,2)+round(VE,2)+0+0+0+0+0+round(CPN,2)+0+0+0+0+0+0+round(FR,2)+round(AC,2)+0+0+0+0+0
    credit = credit.append({'Comptes': "", 'Gestions': "", 'Libelles': 'TOTAL','NB':'', 'Montants':round(total,2)}, ignore_index=True)
    

    return credit

def Journal_Credit_Non(df1,df2,df3,df4):

    Emission_ADMV = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") &
                     ((df1['Office Location'].str.contains('SAV', na=False)) | (df1['Office Location'].str.contains('ADV', na=False)))]
    EA = Emission_ADMV["Montant init."].sum()

    Emission_INTERNET = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (~df1['Commentaires'].str.contains('AMEX', na=False)) &
                        (~df1['Commentaires'].str.contains('PPAL', na=False))]
    EI = Emission_INTERNET["Montant init."].sum()

    Emission_INTERNET_PAYPAL = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('PPAL', na=False))]
    EIP = Emission_INTERNET_PAYPAL["Montant init."].sum()

    Emission_INTERNET_Amex = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('AMEX', na=False))]
    EIA = Emission_INTERNET_Amex["Montant init."].sum()

    Emission_VAD_AMEX_rem = df2[(df2["Type"] == "Débit") & (df2["Moyen de paiement"] == "AMEX") & (~df2["Info. compl."].str.contains('INT', na=False))]
    print(len(Emission_VAD_AMEX_rem))
    Emission_VAD_AMEX_rem['Transaction'] = Emission_VAD_AMEX_rem['Transaction'].astype('string')
    
    Emission_VAD_AMEX_sw = df1[(df1["Type Trans."] == "PMNT") & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") & (df1['Office Location'].str.contains('CVD', na=False))]
    print(len(Emission_VAD_AMEX_sw))
    Emission_VAD_AMEX_sw['Id. Externe'] = Emission_VAD_AMEX_sw['Id. Externe'].astype('string')
    EV=Emission_VAD_AMEX_sw["Montant init."].sum()
    
    Emission_VAD_AMEX=Emission_VAD_AMEX_rem[Emission_VAD_AMEX_rem['Transaction'].isin(Emission_VAD_AMEX_sw["Id. Externe"].values)]
    print(len(Emission_VAD_AMEX))
    EVA=Emission_VAD_AMEX["Montant du paiement"].sum()

    Marie_Do = df4[(df4["IS_VALID"]=="Y")]
    MD=Marie_Do["DON_AMOUNT"].sum()

    Remboursement_VAD_AMEX_rem = df3[(df3["Type"] == "Crédit") & (df3["Moyen de paiement"] == "AMEX") & (~df3["Info. compl."].str.contains('INT', na=False))]
    print(len(Remboursement_VAD_AMEX_rem))
    Remboursement_VAD_AMEX_rem['Transaction'] = Remboursement_VAD_AMEX_rem['Transaction'].astype('string')
    
    Remboursement_VAD_AMEX_sw = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Ent. Dest."] != "AGEN")  & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") & (df1['Office Location'].str.contains('CVD', na=False))]
    print(len(Remboursement_VAD_AMEX_sw))
    Remboursement_VAD_AMEX_sw['Id. Externe'] = Remboursement_VAD_AMEX_sw['Id. Externe'].astype('string')
    RV=Remboursement_VAD_AMEX_sw["Montant init."].sum()
    
    Remboursement_VAD_AMEX=Remboursement_VAD_AMEX_rem[Remboursement_VAD_AMEX_rem['Transaction'].isin(Remboursement_VAD_AMEX_sw["Id. Externe"].values)]
    print(len(Remboursement_VAD_AMEX))
    RVA=Remboursement_VAD_AMEX["Montant du paiement"].sum()

    Remboursement_INTERNET_Amex = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('AMEX', na=False))]
    RIA = Remboursement_INTERNET_Amex["Montant init."].sum()

    Remboursement_Remise_Amex = df2[(df2["Type"] == "Crédit") & (df2["Moyen de paiement"] == "AMEX") ]
    RRA = Remboursement_Remise_Amex["Montant du paiement"].sum()

    # Credit
    Cheque_emettre=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CHK")]
    CE = Cheque_emettre["Montant init."].sum()

    Virement_emettre=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "VIREMENT")]
    VE = Virement_emettre["Montant init."].sum()

    avoir_client=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & ((df1["Mode pmt"] == "AVOIR CLIENT") | (df1["Mode pmt"] == "AVOIRCLIENT"))]
    AC = avoir_client["Montant init."].sum()

    coupon=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CPN")]
    CPN = coupon["Montant init."].sum()

    fraude=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "NON REMBOURSE")]
    FR = fraude["Montant init."].sum()

    WriteOFF=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "WRITEOFF")]
    WOFF = WriteOFF["Montant init."].sum()

    # B to C
    df2['Commande'].replace(regex=True, inplace=True, to_replace=r'[^0-9.\-]', value=r'')
    cvd=df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] != "TERMS") & (df1["Mode pmt"] != "TO REFUND") 
                    & (df1['Office Location'].str.contains('CVD', na=False))]
    cvd['Num. Orig.'] = cvd['Num. Orig.'].astype('string')
    print("cvd",len(cvd))
    cvd_remis=df2[(df2["Type"] == "Crédit") & (df2["Moyen de paiement"] != "AMEX") ]
    cvd_remis['Commande'] = cvd_remis['Commande'].astype('string')
    print("cvd_remis",len(cvd_remis))
    exist=cvd_remis[cvd_remis['Commande'].isin(cvd["Num. Orig."].values)]
    print("exist",len(exist))
    cvd_total = exist["Montant du paiement"].sum()
    print("total cvd",cvd_total)

    remb_Sav_Adv = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") 
                      & ((df1["Mode pmt"] == "CC") | (df1["Mode pmt"] == "CC TPE")) & ((df1['Office Location'].str.contains('SAV', na=False)) | (df1['Office Location'].str.contains('ADV', na=False)))]
    Rsa = remb_Sav_Adv["Montant init."].sum()
    print("-------SAV + ADV---------", Rsa)
    print(len(remb_Sav_Adv))

    Remboursement_ADMV = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") 
                      & (df1["Mode pmt"] == "CC") & (df1['Utilisateur'].str.contains('BLO', na=False)) & (~df1['Office Location'].str.contains('SAV', na=False)) & 
                      (~df1['Office Location'].str.contains('ADV', na=False)) & (~df1['Office Location'].str.contains('CVD', na=False))]
    Remboursement_ADMV['Num. Orig.'] = Remboursement_ADMV['Num. Orig.'].astype('string')
    RA_internet = Remboursement_ADMV["Montant init."].sum()
    internet_remise = df2[(df2["Type"] == "Crédit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Info. compl."].str.contains('INT', na=False))]
    internet_remise['Commande'] = internet_remise['Commande'].astype('string')
    exist_B_to_C=internet_remise[internet_remise['Commande'].isin(Remboursement_ADMV["Num. Orig."].values)]
    B_to_C = exist_B_to_C["Montant du paiement"].sum()
    print("---------internet-------", B_to_C)
    print("exist B to C",len(exist_B_to_C))

    #payal
    # remboursement cb ppal
    Remboursement_INTERNET_PAYPAL = df1[((df1["Type Trans."] == "REFUND") | (df1["Type Trans."] == "MANRFND")) & (df1["Statut"] == "OK") & (df1["Mode pmt"] == "CC") &
                        (df1['Utilisateur'].str.contains('BLO', na=False)) & (df1['Commentaires'].str.contains('PPAL', na=False))]
    Remboursement_INTERNET_PAYPAL['Id. Externe'] = Remboursement_INTERNET_PAYPAL['Id. Externe'].astype('string')
    print("ppal sw",len(Remboursement_INTERNET_PAYPAL))
    ppal_remis=df2[(df2["Type"] == "Crédit") & (df2["Moyen de paiement"] != "AMEX") & (df2["Moyen de paiement"] == "PAYPAL") & (df2["Info. compl."].str.contains('INT', na=False))]
    ppal_remis['Transaction'] = ppal_remis['Transaction'].astype('string')
    print("ppal_remis",len(ppal_remis))
    existppal=ppal_remis[ppal_remis['Transaction'].isin(Remboursement_INTERNET_PAYPAL["Id. Externe"].values)]
    print("existppal",len(existppal))
    ppal_total = existppal["Montant du paiement"].sum()

    credit=pd.DataFrame(columns=['Comptes', 'Gestions', 'Libelles', 'NB', 'Montants'])
    credit = credit.append({'Comptes': "Crédit", 'Gestions': "", 'Libelles': '','NB':"", 'Montants':""}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Emission ADMV','NB':len(Emission_ADMV), 'Montants':round(EA,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Emission Internet','NB':len(Emission_INTERNET), 'Montants':round(EI,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Emission Internet PAYPAL','NB':len(Emission_INTERNET_PAYPAL), 'Montants':round(EIP,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4787100", 'Gestions': "", 'Libelles': 'Emission Internet AMEX','NB':len(Emission_INTERNET_Amex), 'Montants':round(EIA,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Emission VAD','NB':len(Emission_VAD_AMEX_sw)-len(Emission_VAD_AMEX), 'Montants':round(EV,2)-round(EVA,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Emission VAD AMEX','NB':len(Emission_VAD_AMEX), 'Montants':round(EVA,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4670800", 'Gestions': "", 'Libelles': 'Don La Marie Do','NB':len(Marie_Do), 'Montants':round(MD,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "", 'Gestions': "", 'Libelles': '','NB':'', 'Montants':''}, ignore_index=True)
    credit = credit.append({'Comptes': "4673410", 'Gestions': "", 'Libelles': 'Chèque à émettre','NB':len(Cheque_emettre), 'Montants':round(CE,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4673420", 'Gestions': "", 'Libelles': 'Virement à émettre','NB':len(Virement_emettre), 'Montants':round(VE,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "5113160", 'Gestions': "", 'Libelles': 'Remboursement CEPAC B to C','NB':len(exist)+len(remb_Sav_Adv)+len(exist_B_to_C), 'Montants':round(cvd_total,2)+round(Rsa,2)+round(B_to_C,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "5113200", 'Gestions': "", 'Libelles': 'Remboursement CEPAC AMEX','NB':len(Remboursement_Remise_Amex)+len(Remboursement_INTERNET_Amex)+len(Remboursement_VAD_AMEX), 'Montants':round(RRA,2)+round(RIA,2)+round(RVA,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "5113300", 'Gestions': "", 'Libelles': 'Remboursement CEPAC PAYPAL','NB':len(existppal), 'Montants':round(ppal_total,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "5113140", 'Gestions': "", 'Libelles': 'Remboursement TPE','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "5113190", 'Gestions': "", 'Libelles': 'Remboursement CEPAC B to B','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "", 'Gestions': "", 'Libelles': '','NB':'', 'Montants':''}, ignore_index=True)
    credit = credit.append({'Comptes': "4786010", 'Gestions': "", 'Libelles': 'Coupons (annulation/rembst)','NB':len(coupon), 'Montants':round(CPN,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Remboursement réquisitions','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "5113160", 'Gestions': "", 'Libelles': 'Annulation CB declarée en TO CAPTURE en J','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "4787400", 'Gestions': "", 'Libelles': 'Remboursement divers','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "1812100", 'Gestions': "", 'Libelles': 'Avis comptable AJA','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "1813100", 'Gestions': "", 'Libelles': 'Avis comptable BIA','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "4673710", 'Gestions': "", 'Libelles': 'CB Impayées à régulariser','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': "Fraude CB- Régul d'impayé",'NB':len(fraude), 'Montants':round(FR,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4781396", 'Gestions': "", 'Libelles': 'Avoir Client','NB':len(avoir_client), 'Montants':round(AC,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "7580000", 'Gestions': "BOF01", 'Libelles': 'Trop perçu < 5 euros / Chèque vacances non remboursés','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "7580000", 'Gestions': "BOF01", 'Libelles': 'Trop perçu/résa, transfert vers client bank (<5€)','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "6580000", 'Gestions': "BOF01", 'Libelles': 'Write off  non remboursable (<5€)','NB':len(WriteOFF), 'Montants':round(WOFF,2)}, ignore_index=True)
    credit = credit.append({'Comptes': "4670160", 'Gestions': "", 'Libelles': 'Excédent de caisse','NB':0, 'Montants':0}, ignore_index=True)
    credit = credit.append({'Comptes': "4670160", 'Gestions': "", 'Libelles': 'Régularisation Déficit de caisse','NB':0, 'Montants':0}, ignore_index=True)
    total=round(EA,2)+round(EI,2)+round(EIP,2)+round(EIA,2)+(round(EV,2)-round(EVA,2))+round(EVA,2)+round(MD,2)+round(CE,2)+round(VE,2)+0+0+0+0+0+round(CPN,2)+0+0+0+0+0+0+round(FR,2)+round(AC,2)+0+0+0+0+0
    credit = credit.append({'Comptes': "", 'Gestions': "", 'Libelles': 'TOTAL','NB':'', 'Montants':round(total,2)}, ignore_index=True)
    

    return credit

def phrase(df1,df2,df3):
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
    nbtotalr=len(df_cepac_remise["Montant du paiement"])
    totalAttente = round(attenteRemise_1["Montant du paiement"].sum(), 2)
    nbattente=len(attenteRemise_1["Montant du paiement"])
    total1 = round(totalRemise - totalAttente, 2)
    TotalAttenteJ = round(attenteRemiseJour["Montant du paiement"].sum(), 2)
    print('atttente-------------------',len(attenteRemiseJour["Montant du paiement"]))
    
    total = round(total1 + TotalAttenteJ, 2)
    nb=nbtotalr-nbattente+len(attenteRemiseJour["Montant du paiement"])

    #data = "Calcul montant CEPAC => Total remisé du jour (", totalRemise, ") - En attente de remise J-1 (", totalAttente, ") = ",total1," + En attente de remise du jour (", TotalAttenteJ, ") // Total CEPAC du ",datetime_object.day,"/",datetime_object.month,"  = ", total, ""
    return total,nb

def creditOui(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        File2 = request.FILES["file2"]
        File3 = request.FILES["file3"]
        File4 = request.FILES["file4"]
        File5 = request.FILES["file5"]
        File6 = request.FILES["file6"]
        File7 = request.FILES["file7"]
        #annee = request.POST["annee"]
        
        internet = pd.read_excel(File1)
        adv = pd.read_excel(File2)
        sav = pd.read_excel(File3)
        cvd = pd.read_excel(File4)

        df2 = pd.read_excel(File5)
        df3 = pd.read_excel(File6)
        df4 = pd.read_excel(File7)

        seaware=pd.concat([internet,adv,sav,cvd])
        seaware.reset_index(inplace=True,drop=True)
        
        df1 = seaware.drop_duplicates(subset=['Num. Trans.'], keep='last')
        df1.reset_index(inplace=True,drop=True)
        print(len(df1))
        # Stats
        data = Journal_Credit_Oui(df1, df2, df3,df4)

        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))

def creditNon(request):
    if request.method == 'POST':
        File1 = request.FILES["file1"]
        File2 = request.FILES["file2"]
        File3 = request.FILES["file3"]
        File4 = request.FILES["file4"]
        File5 = request.FILES["file5"]
        File6 = request.FILES["file6"]
        File7 = request.FILES["file7"]
        #annee = request.POST["annee"]
        
        internet = pd.read_excel(File1)
        adv = pd.read_excel(File2)
        sav = pd.read_excel(File3)
        cvd = pd.read_excel(File4)

        df2 = pd.read_excel(File5)
        df3 = pd.read_excel(File6)
        df4 = pd.read_excel(File7)

        seaware=pd.concat([internet,adv,sav,cvd])
        seaware.reset_index(inplace=True,drop=True)
        
        df1 = seaware.drop_duplicates(subset=['Num. Trans.'], keep='last')
        df1.reset_index(inplace=True,drop=True)
        print(len(df1))
        # Stats
        data = Journal_Credit_Non(df1, df2, df3,df4)

        print('data : ', data)

    return HttpResponse(data.to_json(orient='records'))