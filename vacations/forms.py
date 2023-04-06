from django import forms
from .models import Vacations


class TakeVacationForm(forms.ModelForm):
    date_of_begin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'id': 'start-date'}))
    date_of_end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'id': 'end-date'}))
    send_to_all = forms.BooleanField(required=False,
                                     widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'input'}))
    comments = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Some comments...'}))

    class Meta:
        model = Vacations
        fields = ('date_of_begin', 'date_of_end', 'comments', 'send_to_all',)
