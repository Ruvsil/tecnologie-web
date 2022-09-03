from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from .models import Canzone,User
from .templatetags import tags_gestione
import datetime
import os
# Create your tests here.

client = Client()

class ListaCanzoniViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        artista1 = User.objects.create(username='artista1',password='artpassword')
        with open('file','w') as f:
            f.write('7/2022,1')

        with open('file2','w') as f2:
            f2.write(' ')


        canzone1 = Canzone.objects.create(titolo='titolo',autore=artista1,data_pub='2022-02-02',durata=datetime.timedelta(0,30,0,0,2,0,0),file_visite=os.path.join(os.getcwd(),'file'),titolo_autore='titolo_artista1',visite=1)
        canzone2 = Canzone.objects.create(titolo='titolo2',autore=artista1,data_pub='2022-02-02',durata=datetime.timedelta(0,30,0,0,2,0,0),file_visite=os.path.join(os.getcwd(),'file2'),titolo_autore='titolo2_artista1',visite=0)


    def test_response_code(self):
        response = client.get(reverse('gestione:listacanzoni'))
        assert response.status_code == 200
    def test_aggiungi_canzone_non_in_menu(self):
        response = client.get(reverse('gestione:listacanzoni'))
        assert 'Aggiungi Canzone'.encode() not in response.content
    def test_login_in_menu(self):
        response = client.get(reverse('gestione:listacanzoni'))
        assert 'Login'.encode() in response.content
    def test_Canzoni_in_response(self):
        response = client.get(reverse('gestione:listacanzoni'))
        assert 'titolo'.encode() in response.content and 'titolo2'.encode() in response.content
    def test_Eliminato(self):
        response = client.get(reverse('gestione:listacanzoni')+'?canzoneeliminato=titolo')
        print(response.content)
        assert f' La procedura di eliminazione della canzone titolo è andata a buon fine'.encode() in response.content


class popolarità(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        artista1 = User.objects.create(username='artista1')
        with open('file','w') as f:
            f.write('9/2022,1')

        with open('file2','w') as f2:
            f2.write('')


        canzone1 = Canzone.objects.create(titolo='titolo',autore=artista1,data_pub='2022-02-02',durata=datetime.timedelta(0,30,0,0,2,0,0),file_visite=os.path.join(os.getcwd(),'file'),titolo_autore='titoloartista1',visite=1)
        canzone2 = Canzone.objects.create(titolo='titolo2',autore=artista1,data_pub='2022-02-02',durata=datetime.timedelta(0,30,0,0,2,0,0),file_visite=os.path.join(os.getcwd(),'file2'),titolo_autore='titolo2artista1',visite=0)


    def test_canzone_massime_visite(self):
        c = Canzone.objects.filter(pk='titoloartista1')[0]
        pop = c.pop()
        print(f'test_canzone_massime_visite:{pop}')
        assert pop == (1.0, 1)


    def test_canzone2_file_visite_vuoto(self):
        c = Canzone.objects.filter(pk='titolo2artista1')[0]
        pop = c.pop()
        print(f'test_canzone_file_visite_vuoto:{pop}')
        assert pop == 0