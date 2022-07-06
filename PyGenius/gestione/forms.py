from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from .models import *

class CreaCanzoneForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id='creacanzone_crispy_form'
    helper.form_method = 'POST'
    style_string = 'background-color:#3C1B37;border-top:10px;border-left:10px;border-color:#1A1018;color:#E4DFE2'
    helper.add_input(Submit('submit', 'Aggiungi Canzone', style=style_string))
    helper.layout = Layout(
        Field('titolo', css_class='text-center', style=style_string),
        HTML("<br>"),
        Field('durata', placeholder='00:00', css_class='text-center',style=style_string),
        HTML("<br>"),
        Field('data_pub', css_class='text-center',style=style_string),
        HTML("<br>"),
        Field('testo', css_class='text-center',style=style_string),
        HTML("<br>"),
        Field('cover', css_class='text-center',style='background-color:#000000'),
        HTML("<div style='color:#BBBBBB'>Immagine di copertina non obbligatoria(500x500) </div> <br>"),
        Field('album', css_class='text-center', style=style_string),
        HTML("<br>")
            )

    class Meta:
        model = Canzone
        fields =['titolo','durata','data_pub','testo','cover','album']
        widgets = {
            'data_pub' : forms.DateInput(attrs={'type':'date'}),
            'cover' : forms.FileInput(attrs={'style':'background-color:#3C1B37;border-top:10px;border-left:10px;border-color:#1A1018;color:#E4DFE2'}),

        }

class CreaContributoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id='creacontributo_crispy_form'
    helper.form_method = 'POST'
    style_string = 'background-color:#3C1B37;border-top:10px;border-left:10px;border-color:#1A1018;color:#E4DFE2'
    helper.add_input(Submit('submit', 'Aggiungi Contributo', style=style_string))
    helper.layout = Layout(
        Field('testo', css_class='text-center', style=style_string),
        HTML("<br>"),
            )
    class Meta:
        model = Contributo
        fields =['testo']

class CreaAlbumForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id='creaalbum_crispy_form'
    helper.form_method = 'POST'
    style_string = 'background-color:#3C1B37;border-top:10px;border-left:10px;border-color:#1A1018;color:#E4DFE2'
    helper.add_input(Submit('submit', 'Aggiungi Album', style=style_string))
    helper.layout = Layout(
        Field('titolo', css_class='text-center', style=style_string),
        HTML("<br>"),
        Field('data_pub', css_class='text-center', style=style_string),
        HTML("<br>"),
        Field('cover', css_class='text-center', style=style_string),
        HTML("<br>"),
            )

    class Meta:
        model = Album
        fields = ['titolo', 'data_pub', 'cover',]
        widgets = {
            'data_pub': forms.DateInput(attrs={'type': 'date'}),
            'cover': forms.FileInput(attrs={
                'style': 'background-color:#3C1B37;border-top:10px;border-left:10px;border-color:#1A1018;color:#E4DFE2'}),
        }
