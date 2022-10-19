
from django.contrib import admin
from django.urls import path, re_path
from Caisseapp import viewsInternet
from django.conf.urls import include
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^',include("Caisseapp.urls")),
]
