Progetto tecnologie web PyGenius 
Francesco Rigoni

Per la gestione dei pacchetti python del progetto è stato utilizzato pipenv
fare quindi riferimento al pipfile presente nella cartella del progetto per ottenere i requirements
passaggi per installazione:

-estrarre la cartella del progetto
-creare un ambiente virtuale con il comando 'pipenv shell'
-importare i pacchetti dal pipfile con il comando 'pipenv update'
-spostarsi nella cartella pygenius
-opzionalmente creare un superuser con il comando 'python manage.py createsuperuser'
-eseguire il comando 'python manage.py runserver'