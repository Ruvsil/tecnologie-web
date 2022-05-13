from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.views.generic.edit import CreateView
# Create your views here.

class CreaUtenteEditor(CreateView):
    form_class = CreaEditorForm
    template_name = 'accounts/crea_editor.html'
    success_url = reverse_lazy('accounts:login')

class CreaUtenteArtista(CreateView):
    form_class = CreaArtistaForm
    template_name = 'accounts/crea_artista.html'
    success_url = reverse_lazy('accounts:login')