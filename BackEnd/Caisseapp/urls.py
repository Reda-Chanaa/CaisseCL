from Caisseapp import viewsJournal
from Caisseapp import viewsInternet
from Caisseapp import viewsADV
from Caisseapp import viewsSAV

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #Journal Débit
    url(r'journal-debit-non/', csrf_exempt(viewsJournal.debitNon), name='file'),
    url(r'journal-debit-oui/', csrf_exempt(viewsJournal.debitOui), name='file'),
    
    #Journal Crédit
    url(r'journal-credit-non/', csrf_exempt(viewsJournal.creditNon), name='file'),
    url(r'journal-credit-oui/', csrf_exempt(viewsJournal.creditOui), name='file'),

    #Internet Débit
    url(r'internet-amex-debit/', csrf_exempt(viewsInternet.InternetAmexDebit), name='file'),
    url(r'internet-cc-debit/', csrf_exempt(viewsInternet.InternetCcDebit), name='file'),
    url(r'internet-paypal-debit/', csrf_exempt(viewsInternet.InternetPaypalDebit), name='file'),
    
    #Internet Crédit
    url(r'internet-amex-credit/', csrf_exempt(viewsInternet.InternetAmexCredit), name='file'),
    url(r'internet-cc-credit/', csrf_exempt(viewsInternet.InternetCcCredit), name='file'),
    url(r'internet-paypal-credit/', csrf_exempt(viewsInternet.InternetPaypalCredit), name='file'),
    
    #Internet phrase
    url(r'internet-phrase/', csrf_exempt(viewsInternet.InternetPhrase), name='file'),

    #ADV
    url(r'adv-credit/', csrf_exempt(viewsADV.AdvCredit), name='file'),
    url(r'adv-debit/', csrf_exempt(viewsADV.AdvDebit), name='file'),
    url(r'adv-sum-debit/', csrf_exempt(viewsADV.AdvSumDebit), name='file'),
    url(r'adv-sum-credit/', csrf_exempt(viewsADV.AdvSumCredit), name='file'),

    #SAV
    url(r'sav-credit/', csrf_exempt(viewsSAV.SavCredit), name='file'),
    url(r'sav-debit/', csrf_exempt(viewsSAV.SavDebit), name='file'),
    url(r'sav-sum-debit/', csrf_exempt(viewsSAV.SavSumDebit), name='file'),
    url(r'sav-sum-credit/', csrf_exempt(viewsSAV.SavSumCredit), name='file'),

    #CVD
    url(r'cvd-credit/', csrf_exempt(viewsSAV.SavCredit), name='file'),
    url(r'cvd-debit/', csrf_exempt(viewsSAV.SavDebit), name='file'),
    url(r'cvd-sum-debit/', csrf_exempt(viewsSAV.SavSumDebit), name='file'),
    url(r'cvd-sum-credit/', csrf_exempt(viewsSAV.SavSumCredit), name='file'),
]
