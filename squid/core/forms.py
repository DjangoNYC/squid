from django import forms
from .models import MemberRSVP


class EventAttendeeForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)
    worked_on = forms.CharField(widget=forms.Textarea(attrs={
        'cols': '35',
        'rows': '5'
        }))

    class Meta:
        model = MemberRSVP
        fields = ('id', 'worked_on',)
