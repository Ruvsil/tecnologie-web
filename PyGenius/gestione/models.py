from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import os
from pathlib import Path
# Create your models here.

BASE = Path(__file__).resolve().parent.parent



def logs_path():
    return os.path.join(BASE,'static/media/', 'logs')

class Album(models.Model):
    titolo = models.CharField(max_length=200)
    autore = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    data_pub = models.DateField(default=None)
    cover = models.ImageField(upload_to='covers/',default='/imgs/missing_album.jpg')
    titolo_autore = models.CharField(primary_key= True, max_length=600,error_messages={'invalid':'Esiste già'})

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


    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['titolo', 'autore'], name='titolo_autore'
    #         )
    #     ]


    def visita(self, user):
        c = get_object_or_404(Canzone, pk=self.pk)
        try:
            c.visite += 1
            c.save()
        except Exception as e:
            print(f'Errore nel aumentare le visite: {e}')

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
            contrib.downvotes += 1
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
