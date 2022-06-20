from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from braces.views import GroupRequiredMixin



class CreaCanzone(GroupRequiredMixin,CreateView):
    group_required = ["Artisti"]
    title = "Aggiungi una canzone alle tue pubblicazioni"
    form_class = CreaCanzoneForm
    template_name = "gestione/creacanzone.html"
    success_url = reverse_lazy('gestione:listacanzoni')

    def form_valid(self, form):
        artista = self.request.user
        print(artista)
        form.instance.autore = artista
        print(form)
        return super(CreaCanzone, self).form_valid(form)

class ListaCanzoni(ListView):
    model = Canzone
    template_name = 'gestione/listacanzoni.html'
    ordering = ['-visite']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Pubblicazioni'
        return context

class ListaCanzoniArtista(ListView):
    model = Canzone
    template_name = 'gestione/listacanzoni.html'
    ordering = ['-visite']

    def get_queryset(self):
        arg = self.kwargs['pk']
        qs=self.model.objects.filter(autore=arg)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data()
        context['title'] = 'Pubblicazioni'
        return context

class DettagliaCanzone(DetailView):
    model = Canzone
    template_name = 'gestione/dettagliacanzone.html'

class EliminaCanzone(DeleteView):
    model = Canzone
    success_url = reverse_lazy('gestione:listacanzoni')


def RisultatiRicerca(request):
        search = request.GET['q']
        artista = User.objects.filter(username=search)
        print(artista)
        if len(artista) == 1:

            return HttpResponseRedirect(f"{reverse_lazy('gestione:listacanzoni')}{artista[0].pk}")
        else :
            return HttpResponseRedirect(reverse_lazy('gestione:listacanzoni')+'?search=notok')
