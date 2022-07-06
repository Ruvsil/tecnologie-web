from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


class CreaEditorForm(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Editor")
        g.user_set.add(user)
        return user

class CreaArtistaForm(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Artisti")
        g.user_set.add(user)
        g = Group.objects.get(name="Editor")
        g.user_set.add(user)
        return user
