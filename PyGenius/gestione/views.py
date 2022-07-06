import datetime
import os
from pathlib import Path

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
from django.core.files import File
BASE = Path(__file__).resolve().parent.parent




class CreaCanzone(GroupRequiredMixin,CreateView):
    group_required = ["Artisti"]
    title = "Aggiungi una canzone alle tue pubblicazioni"
    form_class = CreaCanzoneForm
    template_name = "gestione/creacanzone.html"

    def get_success_url(self):
        return reverse_lazy('gestione:dettagliacanzone', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        artista = self.request.user
        form.instance.autore = artista
        log_path = os.path.join(BASE, 'static','media','logs')
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
        with open(os.path.join(BASE, 'static','media','logs', f'file_{form.instance.titolo.replace(" ","_")}'),'ab'):
            pass
        form.instance.file_visite = os.path.join(log_path, f'file_{form.instance.titolo.replace(" ","_")}')
        form.instance.titolo_autore = form.instance.titolo + artista.username

        q = Canzone.objects.filter(titolo_autore = form.instance.titolo_autore)
        if len(q)>0:
            raise forms.ValidationError('Esiste già una canzone con questo titolo e artista', code='invalid')

        return super(CreaCanzone, self).form_valid(form)


class CreaContributo(GroupRequiredMixin,CreateView):
    group_required = ["Editor"]
    title = "Aggiungi un contributo"
    form_class = CreaContributoForm
    template_name = "gestione/creacontributo.html"

    def get_success_url(self):
        return reverse_lazy('gestione:dettagliacanzone',kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        editor = self.request.user
        canzone = Canzone.objects.filter(titolo_autore=self.kwargs['pk'])[0]
        data_post = datetime.date.today()
        form.instance.canzone = canzone
        form.instance.data_post = data_post
        form.instance.editor = editor

        return super(CreaContributo, self).form_valid(form)



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Creaeeeee'
        context['editor'] = self.kwargs['pk']
        return context

class ListaCanzoni(ListView):
    model = Canzone
    template_name = 'gestione/listacanzoni.html'
    queryset = Canzone.objects.order_by('-popolarità')[:15]

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data()
        context['lista_contributi_star'] = Contributo.objects.filter(canzone=self.kwargs['pk']).filter(ha_star=True)
        context['lista_contributi_non_star'] = Contributo.objects.filter(canzone=self.kwargs['pk']).filter(ha_star=False).order_by('-upvotes')



        context['guest'] = sum(list(map(int,self.request.META['REMOTE_ADDR'].split(sep='.'))))


        #print(context['lista_contributi'])
        #print(context['lista_contributi'][0].downvote)
        return context

class EliminaCanzone(GroupRequiredMixin,DeleteView):
    group_required = ["Artisti"]
    model = Canzone

    def get_success_url(self):
        return reverse_lazy('gestione:listacanzoni')+f'?eliminato={self.object.pk}'


class CreaAlbum(GroupRequiredMixin,CreateView):
    group_required = ["Editor"]
    model = Album
    form_class = CreaAlbumForm
    template_name = 'gestione/creaalbum.html'

    def get_success_url(self):
        return reverse_lazy('gestione:dettagliaalbum',kwargs={'pk':self.object.pk})

    def form_valid(self, form):
        artista = self.request.user
        form.instance.autore = artista
        form.instance.titolo_autore = form.instance.titolo + artista.username
        q = Album.objects.filter(titolo_autore=form.instance.titolo_autore)
        if len(q) > 0:
            raise forms.ValidationError('Esiste già un album con questo titolo e artista', code='invalid')
        return super(CreaAlbum, self).form_valid(form)


class ListaAlbum(ListView):
    model = Album
    template_name = 'gestione/listaalbum.html'
    queryset = Album.objects.all()[:15]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Albums'
        return context


class DettagliaAlbum(DetailView):
    model = Album
    template_name = 'gestione/dettagliaalbum.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data()
        context['lista_canzoni'] = Canzone.objects.filter(album=self.kwargs['pk'])

        return context


class EliminaAlbum(GroupRequiredMixin,DeleteView):
    group_required = ["Artisti"]
    model = Album

    def get_success_url(self):
        return reverse_lazy('gestione:listaalbum') + f'?eliminato={self.object.pk}'

def RisultatiRicerca(request):
        search = request.GET['q']
        model = request.GET['model']

        if model=='Artisti':
            artista = User.objects.filter(username=search)

            if len(artista) == 1:

                return HttpResponseRedirect(f"{reverse_lazy('gestione:listacanzoni')}{artista[0].pk}")
            else :
                return HttpResponseRedirect(reverse_lazy('gestione:listacanzoni')+'?search=notok')
        if model == 'Canzoni':
            canzone = Canzone.objects.filter(titolo=search)


            if len(canzone) > 0 :

                return HttpResponse(render_to_string("gestione/listacanzoni.html",context={'object_list': canzone}))
            else:
                return HttpResponseRedirect(reverse_lazy('gestione:listacanzoni') + '?search=none')
        if model == 'Album':
            album = Album.objects.filter(titolo=search)


            if len(album) > 0:

                return HttpResponse(render_to_string("gestione/listacanzoni.html", context={'object_list': album}))
            else:
                return HttpResponseRedirect(reverse_lazy('gestione:listacanzoni') + '?search=none')
