from django.urls import path, include, re_path
from .views import *

app_name='gestione'

urlpatterns = [
    path('creacanzone/', CreaCanzone.as_view(), name='creacanzone'),
    path('listacanzoni/', ListaCanzoni.as_view(), name='listacanzoni'),
    path('listacanzoni/<pk>/', ListaCanzoniArtista.as_view(), name='listacanzoni'),
    path('dettagliacanzone/<pk>/', DettagliaCanzone.as_view(), name='dettagliacanzone'),
    path('eliminacanzone/<pk>/', EliminaCanzone.as_view(), name='eliminacanzone'),
    path('creacontributo/<pk>/', CreaContributo.as_view(), name='creacontributo'),
    path('creaalbum/', CreaAlbum.as_view(), name='creaalbum'),
    path('listaalbum/', ListaAlbum.as_view(), name='listaalbum'),
    path('dettaglialbum/<pk>/', DettagliaAlbum.as_view(), name='dettagliaalbum'),
    path('eliminaalbum/<pk>/', EliminaAlbum.as_view(), name='eliminaalbum'),
    path('ricerca/', RisultatiRicerca, name='ricerca'),
]