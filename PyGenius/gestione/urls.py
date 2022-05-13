from django.urls import path, include, re_path
from .views import *

app_name='gestione'

urlpatterns = [
    path('creacanzone/', CreaCanzone.as_view(), name='creacanzone'),
    path('listacanzoni/', ListaCanzoni.as_view(), name='listacanzoni'),
]