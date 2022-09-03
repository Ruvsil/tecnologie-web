import os
from pathlib import Path
from django.db.models import Sum
import numpy as np
import datetime
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404

# Create your models here.

BASE = Path(__file__).resolve().parent.parent


def file_cleanup( **kwargs):
    if type(kwargs['instance']) is Canzone:
        percorso_log =kwargs['instance'].file_visite
        os.remove(percorso_log)
    if type(kwargs['instance']) is (Canzone or Album):
        percorso_cover = kwargs['instance'].cover
        percorso_cover = os.path.join(BASE,'static','media',*str(percorso_cover).split(sep='/'))

        if 'imgs' not in percorso_cover:
            os.remove(percorso_cover)



def logs_path():
    return os.path.join(BASE,'static/media/', 'logs')

class Album(models.Model):
    titolo = models.CharField(max_length=200)
    autore = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    data_pub = models.DateField(default=None)
    cover = models.ImageField(upload_to='covers/',default='/imgs/missing_album.jpg')
    titolo_autore = models.CharField(primary_key= True, max_length=500,error_messages={'invalid':'Esiste già'})
    popolarità = models.DecimalField(max_digits=4, decimal_places=3, default=1)

    post_delete.connect(
        file_cleanup)

    def p(album):
        alb = get_object_or_404(Album, pk=album.pk)
        canzoni = album.canzoni.all()
        popolarità = [x.popolarità for x in canzoni]
        p = sum(popolarità)/(len(popolarità)+1)
        try:
            alb.popolarità = p
            alb.save()
        except Exception as e:
            print(e)
        return p



class Canzone(models.Model):
    titolo = models.CharField(max_length=200)
    durata = models.DurationField(null=False, blank=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='canzoni',blank=True,default=None,null=True)
    autore = models.ForeignKey(User, on_delete=models.CASCADE, related_name='canzoni')
    data_pub = models.DateField(default=None)
    visite = models.IntegerField(default=0)
    testo = models.TextField(max_length=100000)
    cover = models.ImageField(upload_to='covers/',default='/imgs/missing.png', null=True,blank=True)
    file_visite = models.FilePathField(path=logs_path(),default=None)
    popolarità = models.DecimalField(max_digits=4,decimal_places=3,default=1)
    titolo_autore = models.CharField(primary_key= True, max_length=600,error_messages={'invalid':'Esiste già'})

    post_delete.connect(
        file_cleanup)
    def pop(self):

        def _distanza(periodo):
            mese = datetime.date.today().month
            anno = datetime.date.today().year
            periodo = list(map(int, periodo.split(sep='/')))
            return abs(mese - periodo[0]) + abs(anno - periodo[1]) * 12
        visite_tot = Canzone.objects.aggregate(Sum('visite'))['visite__sum']
        print(visite_tot)
        c = get_object_or_404(Canzone, pk=self.pk)
        l = []

        with open(c.file_visite, 'r') as file:
            for line in file:
                l.append(np.array(line.split(sep=',')))

        matrice = np.row_stack(l) #matrice con le visite per riga [['m/aaaa' 'user.pk' '\n']...] sostanzialmente il file delle visite come lista
        mesi_unici = (np.unique(matrice[:, :1]).tolist())# estraggo le coppie mese/anno uniche
        counts = []
        for el in mesi_unici:
            counts.append((el, (matrice[:, 0] == el).sum()))# a ciascuna delle coppie mese/anno assegno il conto delle visite in quel periodo

        p = sum(list(map(lambda x: (int(x[1]) / (_distanza(x[0]) + 1)) / (visite_tot), counts))) #calcolo la popolarità convertendo prima i valori in interi
        try:
            c.popolarità = p
            c.save()
        except Exception as e:
            print(e)
        return p, visite_tot





    # def visita(self, user):
    #     c = get_object_or_404(Canzone, pk=self.pk)
    #     try:
    #         c.visite += 1
    #         c.save()
    #     except Exception as e:
    #         print(f'Errore nel aumentare le visite: {e}')

    def __str__(self):
        return f'{self.titolo} di {self.autore} {self.durata}'

    class Meta:
        verbose_name_plural = 'Canzoni'



class Contributo(models.Model):
    testo = models.TextField(default=None)
    data_post = models.DateField(default=None)
    canzone = models.ForeignKey(Canzone, on_delete=models.CASCADE, related_name='note')
    editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributi')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    ha_star = models.BooleanField(default=False)


    def upvote(self):
        contrib = get_object_or_404(Contributo, pk=self.pk)
        try:
            contrib.upvotes += 1
            contrib.save()
        except Exception as e:
            print(e)


    def downvote(self):
        contrib = get_object_or_404(Contributo, pk=self.pk)
        try:
            contrib.upvotes -= 1
            contrib.save()
        except Exception as e:
            print(e)


    def star(self):
        contrib = get_object_or_404(Contributo, pk=self.pk)
        try:
            contrib.ha_star = not contrib.ha_star
            contrib.save()
        except Exception as e:
            print(e)

    class Meta:
        verbose_name_plural = 'Contributi'
