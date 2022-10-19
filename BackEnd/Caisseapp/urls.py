from Caisseapp import viewsJournal
from Caisseapp import viewsInternet
from Caisseapp import viewsADV
from Caisseapp import viewsSAV

from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #Journal Débit
    re_path(r'journal-debit-non/', csrf_exempt(viewsJournal.debitNon), name='file'),
    re_path(r'journal-debit-oui/', csrf_exempt(viewsJournal.debitOui), name='file'),
    
    #Journal Crédit
    re_path(r'journal-credit-non/', csrf_exempt(viewsJournal.creditNon), name='file'),
    re_path(r'journal-credit-oui/', csrf_exempt(viewsJournal.creditOui), name='file'),

    #Internet Débit
    re_path(r'internet-amex-debit/', csrf_exempt(viewsInternet.InternetAmexDebit), name='file'),
    re_path(r'internet-cc-debit/', csrf_exempt(viewsInternet.InternetCcDebit), name='file'),
    re_path(r'internet-paypal-debit/', csrf_exempt(viewsInternet.InternetPaypalDebit), name='file'),
    
    #Internet Crédit
    re_path(r'internet-amex-credit/', csrf_exempt(viewsInternet.InternetAmexCredit), name='file'),
    re_path(r'internet-cc-credit/', csrf_exempt(viewsInternet.InternetCcCredit), name='file'),
    re_path(r'internet-paypal-credit/', csrf_exempt(viewsInternet.InternetPaypalCredit), name='file'),
    
    #Internet phrase
    re_path(r'internet-phrase/', csrf_exempt(viewsInternet.InternetPhrase), name='file'),

    #ADV
    re_path(r'adv-credit/', csrf_exempt(viewsADV.AdvCredit), name='file'),
    re_path(r'adv-debit/', csrf_exempt(viewsADV.AdvDebit), name='file'),
    re_path(r'adv-sum-debit/', csrf_exempt(viewsADV.AdvSumDebit), name='file'),
    re_path(r'adv-sum-credit/', csrf_exempt(viewsADV.AdvSumCredit), name='file'),

    #SAV
    re_path(r'sav-credit/', csrf_exempt(viewsSAV.SavCredit), name='file'),
    re_path(r'sav-debit/', csrf_exempt(viewsSAV.SavDebit), name='file'),
    re_path(r'sav-sum-debit/', csrf_exempt(viewsSAV.SavSumDebit), name='file'),
    re_path(r'sav-sum-credit/', csrf_exempt(viewsSAV.SavSumCredit), name='file'),

    #CVD
    re_path(r'cvd-credit/', csrf_exempt(viewsSAV.SavCredit), name='file'),
    re_path(r'cvd-debit/', csrf_exempt(viewsSAV.SavDebit), name='file'),
    re_path(r'cvd-sum-debit/', csrf_exempt(viewsSAV.SavSumDebit), name='file'),
    re_path(r'cvd-sum-credit/', csrf_exempt(viewsSAV.SavSumCredit), name='file'),
]
