from django.forms import ModelForm, ValidationError, CharField
from main.models import *


class ReferenceCreateForm(ModelForm):
    next_date = CharField()

    class Meta:
        model = Reference
        fields = ('text', 'patient', 'next_doctor', 'next_date', 'all_day')
        
    def clean_next_date(self):
        date, time = self.cleaned_data['next_date'].split()[0], self.cleaned_data['next_date'].split()[1]
        date = '-'.join(date.split('-')[::-1])
        return f'{date} {time}'

    def clean(self):
        return self.cleaned_data
    


        
