import datetime
import lyricsgenius as genius
import requests
import shutil
from gestione.models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

#
BASE_DIR = Path(__file__).resolve().parent.parent

def download_data():
    def rem_wsp(s):
        return s.replace('\u200b','')
    n=5
    path = os.path.join(BASE_DIR,'static','data')
    os.mkdir(path)
    at = '1l0WedY7vXMyF8xRiQXv8k9n6ZfsTB-6Y9edBqex6XThrjPSEM_1ojkiBcMPgWDZ'
    api = genius.Genius(at)
    keshi_songs = api.search_artist('keshi', max_songs=n)
    jeremy_zucker_songs = api.search_artist('jeremy_zucker', max_songs=n)
    lyn_lapyd_songs = api.search_artist('lyn_lapid', max_songs=n)
    songs = keshi_songs.songs + jeremy_zucker_songs.songs + lyn_lapyd_songs.songs
    songs = [song.to_dict() for song in songs]
    songs2 = []
    albums = []
    artists = []
    for song in songs:
        art = rem_wsp(song['artist'])
        if art not in artists:
            artists.append(rem_wsp(song['artist']))
        print('album',song['album'])
        if song['album']:
            al = {'title': rem_wsp(song['album']['name']), 'artist': rem_wsp(song['album']['artist']['name']),
                  'date': datetime.date.today(), 'cover': song['album']['cover_art_url']}
            s = {'title': rem_wsp(song['title']), 'artist': rem_wsp(song['artist']), 'album': rem_wsp(song['album']['name']),
                 'lyrics': song['lyrics'], 'date': song['release_date'],'cover': song['header_image_url']}
            if al not in albums:
                albums.append(al)
            songs2.append(s)
        else:
            songs2.append(
                    {'title': rem_wsp(song['title']), 'artist': rem_wsp(song['artist']), 'album': None, 'lyrics': song['lyrics'],
                     'date': song['release_date'], 'cover': song['header_image_url']})

    with open(os.path.join(path, 'albums'), 'wb') as f:
        print(f'albums:{albums}---------------')
        f.write(repr(albums).encode())
    with open(os.path.join(path, 'artists'), 'wb') as f:
        print(f'artists:{artists}-------------')
        f.write(repr(artists).encode())
    with open(os.path.join(path, 'songs'), 'wb') as f:
        print(f'songs2:{songs2}---------')
        f.write(repr(songs2).encode())

def init_db():
    if not os.path.isdir(os.path.join(BASE_DIR,'static','data')):
        download_data()
    print('inizio init_db')
    print(BASE_DIR)
    if not os.path.isdir(os.path.join(BASE_DIR,'static')):
        os.mkdir(os.path.join(BASE_DIR,'static'))
    if not os.path.isdir(os.path.join(BASE_DIR,'static','media')):
        os.mkdir(os.path.join(BASE_DIR,'static','media'))
    if not os.path.isdir(os.path.join(BASE_DIR, 'static', 'media','covers')):
        os.mkdir(os.path.join(BASE_DIR, 'static', 'media', 'covers'))
    if not os.path.isdir(os.path.join(BASE_DIR, 'static', 'media', 'logs')):
        os.mkdir(os.path.join(BASE_DIR, 'static', 'media', 'logs'))

    Artisti, created = Group.objects.get_or_create(name='Artisti')
    Editor, created = Group.objects.get_or_create(name='Editor')
    proj_add_perm = Permission.objects.get(name='Can add canzone')
    Artisti.permissions.add(proj_add_perm)
    proj_add_perm = Permission.objects.get(name='Can delete canzone')
    Artisti.permissions.add(proj_add_perm)
    proj_add_perm = Permission.objects.get(name='Can change canzone')
    Artisti.permissions.add(proj_add_perm)
    proj_add_perm = Permission.objects.get(name='Can add album')
    Artisti.permissions.add(proj_add_perm)
    proj_add_perm = Permission.objects.get(name='Can delete album')
    Artisti.permissions.add(proj_add_perm)
    proj_add_perm = Permission.objects.get(name='Can change album')
    Artisti.permissions.add(proj_add_perm)
    proj_add_perm = Permission.objects.get(name='Can add contributo')
    Artisti.permissions.add(proj_add_perm)
    Editor.permissions.add(proj_add_perm)
    proj_add_perm = Permission.objects.get(name='Can change contributo')
    Artisti.permissions.add(proj_add_perm)
    Editor.permissions.add(proj_add_perm)
    proj_add_perm = Permission.objects.get(name='Can delete contributo')
    Artisti.permissions.add(proj_add_perm)
    Editor.permissions.add(proj_add_perm)

    # u=User(username='artista1',password='artista1')
    #
    # u.save()
    # Artisti.user_set.add(u)
    data =[]
    for file in os.listdir(os.path.join(BASE_DIR,'static','data')):
        f = open(os.path.join(BASE_DIR,'static','data',file))
        data.append(eval(f.read()))
    print(f'-------------------\ndata:\n{data}\n----------------------\n')
    for artist in data[1]:
        try:
            art = User(username=artist,password=artist)
            print(f'--------------\nart:\n{art}\n----------------\n')
            art.save()
            Artisti.user_set.add(art)
            Editor.uer_set.add(art)
        except:
            pass

    for album in data[0]:
        try:
            print(get_object_or_404(User, username=album['artist']))
            file_name = os.path.join(BASE_DIR,'static','media','covers',album['title'].replace(' ','_')+album['artist'].replace(' ','_')+'.png')
            cov = os.path.join('covers',album['title'].replace(' ','_')+album['artist'].replace(' ','_')+'.png')
            url = album['cover']
            res = requests.get(url, stream=True)
            if res.status_code == 200:
                with open(file_name,'wb') as f:
                    shutil.copyfileobj(res.raw, f)
                    print('Image sucessfully Downloaded: ',file_name)
            else:
                print('Image Couldn\'t be retrieved')
            a = Album(titolo=album['title'], autore=get_object_or_404(User, username=album['artist']), data_pub=album['date'],cover=cov, titolo_autore=album['title']+album['artist'])
            print(album)
            a.save()
        except:
            pass
    for song in data[2]:
        try:
            file_path = os.path.join(BASE_DIR,'static','media','logs',f"file_{song['title'].replace(' ','_')+song['artist'].replace(' ','_')}")
            f = open(file_path,'w')
            file_name = os.path.join(BASE_DIR, 'static', 'media', 'covers', song['title'].replace(' ','_')+song['artist'].replace(' ','_')+ '.png')
            cov = os.path.join('covers', song['title'].replace(' ','_')+song['artist'].replace(' ','_') + '.png')
            url = song['cover']
            res = requests.get(url, stream=True)
            if res.status_code == 200:
                with open(file_name, 'wb') as f:
                    shutil.copyfileobj(res.raw, f)
                    print('Image sucessfully Downloaded: ', file_name)
            else:
                print('Image Couldn\'t be retrieved')
            if song['album']:
                s = Canzone(titolo=song['title'], durata= datetime.timedelta(0,1,0),album=get_object_or_404(Album, titolo=song['album']),autore=get_object_or_404(User, username=song['artist'])\
                        ,data_pub=song['date'],visite=0,testo=song['lyrics'],file_visite=file_path, cover = cov,titolo_autore=song['title']+song['artist'])
            else:
                s = Canzone(titolo=song['title'], durata=datetime.timedelta(0, 1, 0),
                            autore=get_object_or_404(User, username=song['artist']) \
                            , data_pub=song['date'], visite=0, testo=song['lyrics'], file_visite=file_path, cover=cov,
                            titolo_autore=song['title'] + song['artist'])
            s.save()


        except Exception as e:
            print(e)