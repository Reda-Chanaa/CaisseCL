from Caisseapp import viewsInternet
from Caisseapp import viewsADV
from Caisseapp import viewsSAV

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
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
    url(r'adv-phrase/', csrf_exempt(viewsADV.AdvPhrase), name='file'),

    #SAV
    url(r'sav-credit/', csrf_exempt(viewsSAV.SavCredit), name='file'),
    url(r'sav-debit/', csrf_exempt(viewsSAV.SavDebit), name='file'),
    url(r'sav-phrase/', csrf_exempt(viewsSAV.SavPhrase), name='file'),

    #CVD
    url(r'cvd-credit/', csrf_exempt(viewsADV.AdvCredit), name='file'),
    url(r'cvd-debit/', csrf_exempt(viewsADV.AdvDebit), name='file'),
    url(r'cvd-phrase/', csrf_exempt(viewsADV.AdvPhrase), name='file'),
]
