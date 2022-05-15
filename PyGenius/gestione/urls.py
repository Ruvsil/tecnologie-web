from django.urls import path, include, re_path
from .views import *

app_name='gestione'

urlpatterns = [
    path('creacanzone/', CreaCanzone.as_view(), name='creacanzone'),
    path('listacanzoni/', ListaCanzoni.as_view(), name='listacanzoni'),
    path('listacanzoni/<pk>/', ListaCanzoniArtista.as_view(), name='listacanzoni'),
    path('dettagliacanzone/<pk>/', DettagliaCanzone.as_view(), name='dettagliacanzone'),
    path('eliminacanzone/<pk>/', EliminaCanzone.as_view(), name='eliminacanzone'),
]