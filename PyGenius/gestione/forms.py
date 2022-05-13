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
        Field('data_pub',show_label='false', css_class='text-center',style=style_string),
        HTML("<br>"),
        Field('testo', css_class='text-center',style=style_string)
    )
    class Meta:
        model = Canzone
        fields = '__all__'
        widgets = {
            'data_pub' : forms.DateInput(attrs={'type':'date'})
        }

