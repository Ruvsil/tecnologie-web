from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

app_name='accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', CreaUtenteEditor.as_view(), name='register'),
    path('register-artist/', CreaUtenteArtista.as_view(), name='register-artist')
]
