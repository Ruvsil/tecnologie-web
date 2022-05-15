from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
# Create your models here.


class Canzone(models.Model):
    titolo = models.CharField(max_length=200)
    durata = models.DurationField(null=False, blank=False)
    autore = models.ForeignKey(User, on_delete=models.CASCADE, related_name='canzoni')
    data_pub = models.DateField(default=None)
    visite = models.IntegerField(default=0)
    testo = models.TextField(max_length=10000) ##????????
    cover = models.ImageField(upload_to='covers',default='/imgs/missing.png', null=True,blank=True)

    def visita(self):
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


class Album(models.Model):
    titolo = models.CharField(max_length=200)
    durata = models.FloatField(null=False, blank=False)
    data_pub = models.DateField(default=None)
    cover = models.ImageField(default=None)

# class Voto(models.Model):
#     oggetto = models.ForeignKey()


class Contributo(models.Model):
    data_post = models.DateField(default=None)
    canzone = models.ForeignKey(Canzone, on_delete=models.CASCADE, related_name='note')
    posizione = models.IntegerField(default=0)
    editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributi')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def vota(self, is_upvote):
        contrib = get_object_or_404(Contributo, pk=self.pk)
        try:
            if is_upvote:
                contrib.upvotes += 1
            else:
                contrib.downvotes += 1
            contrib.save()
        except Exception as e:
            print(f'Errore nel votare: {e}')

    class Meta:
        verbose_name_plural = 'Contributi'
